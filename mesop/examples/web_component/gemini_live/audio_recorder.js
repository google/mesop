import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

// TODO: Update to use Audio Worklet instead createScriptProcessor which is deprecated.
class AudioRecorder extends LitElement {
  static properties = {
    dataEvent: {type: String},
    stateChangeEvent: {type: String},
    state: {type: String},
    isRecording: {type: Boolean},
    debugBuffer: {state: true},
    debug: {type: Boolean},
    voiceDetectionEnabled: {type: Boolean},
    voiceThreshold: {type: Number},
    voiceHoldTime: {type: Number},
  };

  constructor() {
    super();
    this.debug = false;
    this.mediaStream = null;
    this.audioContext = null;
    this.processor = null;
    this.isStreaming = false;
    this.isRecording = false;
    this.isInitializing = false;
    this.sequenceNumber = 0;
    this.debugBuffer = [];
    this.debugBufferSize = 50;
    this.targetSampleRate = 16000;

    // Voice detection parameters
    //
    // The Gemini Live API has voice activity detection (VAD), but this will waste quota
    // to the API, so it's more efficient implement VAD on the client as well.
    this.voiceDetectionEnabled = true; // Enable by default
    this.voiceThreshold = 0.01; // RMS threshold for voice detection
    this.voiceHoldTime = 500; // Time to hold voice detection state in ms
    this.lastVoiceDetectedTime = 0; // Last time voice was detected
    this.isVoiceDetected = false; // Current voice detection state
    this.consecutiveSilentFrames = 0; // Counter for silent frames
    this.silenceThreshold = 10; // Number of silent frames before cutting off

    this.onGeminiLiveStarted = (e) => {
      if (this.isRecording) {
        this.startStreaming();
      }
    };

    this.onGeminiLiveStopped = (e) => {
      this.stop();
    };
  }

  connectedCallback() {
    super.connectedCallback();
    window.addEventListener(
      'gemini-live-api-started',
      this.onGeminiLiveStarted,
    );
    window.addEventListener(
      'gemini-live-api-stopped',
      this.onGeminiLiveStopped,
    );
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this.stop();
    window.removeEventListener(
      'gemini-live-api-started',
      this.onAudioInputReceived,
    );
    window.removeEventListener(
      'gemini-live-api-stopped',
      this.onGeminiLiveStopped,
    );
  }

  firstUpdated() {
    if (this.state !== 'disabled') {
      this.startStreaming();
    }
  }

  isVoiceFrame(audioData) {
    // Calculate RMS of the audio frame
    let sumSquares = 0;
    for (let i = 0; i < audioData.length; i++) {
      sumSquares += audioData[i] * audioData[i];
    }
    const rms = Math.sqrt(sumSquares / audioData.length);

    const now = Date.now();

    // Check if we detect voice in this frame
    if (rms > this.voiceThreshold) {
      this.lastVoiceDetectedTime = now;
      this.consecutiveSilentFrames = 0;
      this.isVoiceDetected = true;
      return true;
    }

    // Check if we're still within the hold time
    if (now - this.lastVoiceDetectedTime < this.voiceHoldTime) {
      return true;
    }

    // Increment silent frames counter
    this.consecutiveSilentFrames++;

    // If we've seen enough silent frames, mark as silent
    if (this.consecutiveSilentFrames > this.silenceThreshold) {
      this.isVoiceDetected = false;
    }

    return this.isVoiceDetected;
  }

  async startStreaming() {
    if (this.state === 'disabled') {
      this.dispatchEvent(new MesopEvent(this.stateChangeEvent, 'initializing'));
    }
    this.isInitializing = true;
    const initialized = await this.initialize();
    this.isInitializing = false;
    if (initialized) {
      this.isRecording = true;
      this.dispatchEvent(new MesopEvent(this.stateChangeEvent, 'recording'));
      this.start();
    }
  }

  async initialize() {
    try {
      // First check what sample rates are supported with echo cancellation
      const testStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
        video: false,
      });

      // Get the actual sample rate from the system
      const systemTrack = testStream.getAudioTracks()[0];
      const settings = systemTrack.getSettings();
      this.log('System audio settings:', settings);

      // Clean up the test stream
      testStream.getTracks().forEach((track) => track.stop());

      // Now create the real stream using the system's capabilities
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: settings.sampleRate,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          echoCancellationType: 'system',
          latency: 0,
        },
        video: false,
      });

      // Log the actual constraints that were applied
      const audioTrack = this.mediaStream.getAudioTracks()[0];
      const actualConstraints = audioTrack.getSettings();
      this.log('Applied audio constraints:', actualConstraints);

      // Set up audio context matching the system rate
      this.audioContext = new AudioContext({
        sampleRate: settings.sampleRate,
      });
      this.log(
        'AudioContext created with sample rate:',
        this.audioContext.sampleRate,
      );

      const micSource = this.audioContext.createMediaStreamSource(
        this.mediaStream,
      );

      this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);

      // Connect the audio nodes
      micSource.connect(this.processor);
      this.processor.connect(this.audioContext.destination);

      return true;
    } catch (error) {
      this.error('Error initializing audio streamer:', error);
      return false;
    }
  }

  downsampleBuffer(buffer, originalSampleRate) {
    if (originalSampleRate === this.targetSampleRate) {
      return buffer;
    }

    const ratio = originalSampleRate / this.targetSampleRate;
    const newLength = Math.floor(buffer.length / ratio);
    const result = new Float32Array(newLength);

    for (let i = 0; i < newLength; i++) {
      const startIndex = Math.floor(i * ratio);
      const endIndex = Math.floor((i + 1) * ratio);
      let sum = 0;
      let count = 0;

      for (let j = startIndex; j < endIndex && j < buffer.length; j++) {
        sum += buffer[j];
        count++;
      }

      result[i] = count > 0 ? sum / count : 0;
    }

    this.log('Downsampling details:', {
      originalRate: originalSampleRate,
      targetRate: this.targetSampleRate,
      originalLength: buffer.length,
      newLength: result.length,
      actualRatio: buffer.length / result.length,
    });

    return result;
  }

  addAudioDebugger(sourceNode, label) {
    if (!this.debug) return;

    const analyser = this.audioContext.createAnalyser();
    analyser.fftSize = 2048;
    sourceNode.connect(analyser);

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Float32Array(bufferLength);

    this.debugInterval = setInterval(() => {
      if (!this.isStreaming) return;

      analyser.getFloatTimeDomainData(dataArray);
      let rms = 0;
      for (let i = 0; i < bufferLength; i++) {
        rms += dataArray[i] * dataArray[i];
      }
      rms = Math.sqrt(rms / bufferLength);
      this.log(`${label} RMS Level: ${rms.toFixed(6)}`);
    }, 1000);
  }

  start() {
    this.isStreaming = true;
    this.debugBuffer = [];
    this.lastVoiceDetectedTime = 0;
    this.isVoiceDetected = false;
    this.consecutiveSilentFrames = 0;

    this.processor.onaudioprocess = (event) => {
      if (!this.isStreaming) return;

      const inputData = event.inputBuffer.getChannelData(0);
      const originalSampleRate = event.inputBuffer.sampleRate;

      // Log initial processing details if needed
      if (this.sequenceNumber === 0) {
        this.log('Audio Processing Details:', {
          bufferSize: this.processor.bufferSize,
          inputChannels: this.processor.numberOfInputs,
          outputChannels: this.processor.numberOfOutputs,
          originalSampleRate: originalSampleRate,
          targetSampleRate: this.targetSampleRate,
          length: inputData.length,
          timestamp: event.timeStamp,
        });
      }

      // Check for voice activity if enabled
      if (this.voiceDetectionEnabled && !this.isVoiceFrame(inputData)) {
        // Skip this frame if no voice is detected
        this.sequenceNumber++; // Still increment to maintain sequence
        return;
      }

      const downsampledData = this.downsampleBuffer(
        inputData,
        originalSampleRate,
      );

      const processedData = new Float32Array(downsampledData.length);
      const gain = 5.0;
      for (let i = 0; i < downsampledData.length; i++) {
        processedData[i] = downsampledData[i] * gain;
      }

      // Debug logging
      if (this.sequenceNumber % 50 === 0 && this.debug) {
        const stats = {
          originalLength: inputData.length,
          downsampledLength: downsampledData.length,
          maxValue: Math.max(...processedData),
          minValue: Math.min(...processedData),
          originalSampleRate,
          targetSampleRate: this.targetSampleRate,
          isVoiceDetected: this.isVoiceDetected,
        };
        this.log('Audio buffer stats:', stats);
      }

      // Store in debug buffer
      this.debugBuffer.push(processedData);
      if (this.debugBuffer.length > this.debugBufferSize) {
        this.debugBuffer.shift();
      }

      // Audio level monitoring
      let rms = 0;
      for (let i = 0; i < processedData.length; i++) {
        rms += processedData[i] * processedData[i];
      }
      rms = Math.sqrt(rms / processedData.length);

      if (this.sequenceNumber % 10 === 0 && this.debug) {
        this.log(
          `Audio Level (RMS): ${rms.toFixed(4)}, Voice Detected: ${
            this.isVoiceDetected
          }`,
        );
        if (rms < 0.0001) {
          this.warn(
            'Warning: Very low audio level detected. Check if microphone is working.',
          );
        }
      }

      // Convert to Int16Array for transmission
      const intData = new Int16Array(processedData.length);
      for (let i = 0; i < processedData.length; i++) {
        intData[i] = Math.max(
          -32768,
          Math.min(32767, processedData[i] * 32768),
        );

        if (this.sequenceNumber % 100 === 0 && i < 10 && this.debug) {
          this.log(
            `Sample ${i}: Float=${processedData[i].toFixed(4)}, Int16=${
              intData[i]
            }`,
          );
        }
      }

      // Convert to base64 and dispatch
      const bytes = new Uint8Array(intData.buffer);
      const base64Data = btoa(
        Array.from(bytes)
          .map((byte) => String.fromCharCode(byte))
          .join(''),
      );

      this.dispatchEvent(
        new MesopEvent(this.dataEvent, {
          sequence: this.sequenceNumber++,
          sampleRate: this.targetSampleRate,
          data: base64Data,
          isVoice: this.isVoiceDetected,
        }),
      );

      this.dispatchEvent(
        new CustomEvent('audio-input-received', {
          detail: {data: base64Data},
          // Allow event to cross shadow DOM boundaries (both need to be true)
          bubbles: true,
          composed: true,
        }),
      );
    };

    return true;
  }

  stop() {
    this.isStreaming = false;
    this.isRecording = false;

    this.dispatchEvent(new MesopEvent(this.stateChangeEvent, 'disabled'));

    if (this.debugInterval) {
      clearInterval(this.debugInterval);
    }

    if (this.processor) {
      this.processor.onaudioprocess = null;
    }

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach((track) => track.stop());
    }

    if (this.audioContext) {
      this.audioContext.close();
    }
  }

  async playbackDebug() {
    if (!this.debugBuffer.length) {
      this.log('No audio data available for playback');
      return;
    }

    const playbackContext = new AudioContext();
    const systemSampleRate = playbackContext.sampleRate;

    const totalSamples16k =
      this.debugBuffer.length * this.debugBuffer[0].length;

    const upsampledLength = Math.round(
      totalSamples16k * (systemSampleRate / this.targetSampleRate),
    );

    const audioBuffer = playbackContext.createBuffer(
      1,
      upsampledLength,
      systemSampleRate,
    );

    const channelData = audioBuffer.getChannelData(0);

    const combined16kBuffer = new Float32Array(totalSamples16k);
    let offset = 0;
    for (let i = 0; i < this.debugBuffer.length; i++) {
      combined16kBuffer.set(this.debugBuffer[i], offset);
      offset += this.debugBuffer[i].length;
    }

    const ratio = this.targetSampleRate / systemSampleRate;
    for (let i = 0; i < upsampledLength; i++) {
      const position = i * ratio;
      const index = Math.floor(position);
      const decimal = position - index;

      const sample1 = combined16kBuffer[index] || 0;
      const sample2 = combined16kBuffer[index + 1] || sample1;
      channelData[i] = sample1 + decimal * (sample2 - sample1);
    }

    const source = playbackContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(playbackContext.destination);
    source.start();
    this.log('Playing debug audio at system rate...', {
      systemSampleRate,
      originalLength: totalSamples16k,
      upsampledLength,
    });

    source.onended = () => {
      this.log('Debug playback finished');
      playbackContext.close();
    };
  }

  render() {
    if (this.isInitializing) {
      return html`<span><slot></slot></span>`;
    }

    if (this.isRecording) {
      return html`<span @click="${this.stop}"><slot></slot></span> `;
    }

    return html`<span @click="${this.startStreaming}"><slot></slot></span>`;
  }

  log(...args) {
    if (this.debug) {
      console.log(...args);
    }
  }

  warn(...args) {
    if (this.debug) {
      console.warn(...args);
    }
  }

  error(...args) {
    if (this.debug) {
      console.error(...args);
    }
  }
}

customElements.define('audio-recorder', AudioRecorder);
