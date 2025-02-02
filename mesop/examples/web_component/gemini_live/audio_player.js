import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class AudioPlayer extends LitElement {
  static properties = {
    playEvent: {type: String},
    stopEvent: {type: String},
    enabled: {type: Boolean},
    data: {type: String},
  };

  constructor() {
    super();
    this.enabled = false;
    this.audioContext = null; // Initialize audio context
    this.sampleRate = 24000; // Gemini Live API sends data in 24000hz
    this.channels = 1;
    this.queue = [];
    this.isPlaying = false;

    this.onGeminiLiveStarted = (e) => {
      if (!this.enabled) {
        this.playAudio();
      }
    };

    this.onGeminiLiveStopped = (e) => {
      this.dispatchEvent(new MesopEvent(this.stopEvent, {}));
    };

    this.onAudioOutputReceived = (e) => {
      this.addToQueue(e.detail.data);
    };
  }

  connectedCallback() {
    super.connectedCallback();
    window.addEventListener(
      'audio-output-received',
      this.onAudioOutputReceived,
    );
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
    if (this.audioContext) {
      this.audioContext.close();
    }
    window.removeEventListener(
      'audio-output-received',
      this.onAudioInputReceived,
    );
    window.removeEventListener(
      'gemini-live-api-started',
      this.onGeminiLiveStarted,
    );
    window.removeEventListener(
      'gemini-live-api-stopped',
      this.onGeminiLiveStopped,
    );
  }

  firstUpdated() {
    if (this.enabled) {
      this.playAudio();
    }
  }

  updated(changedProperties) {
    // Add audio chunks to queue to play.
    if (changedProperties.has('data') && this.data.length > 0) {
      this.addToQueue(this.data);
    }

    // Clear the queue if the audio player is disabled.
    if (changedProperties.has('enabled') && !this.enabled) {
      this.queue = [];
    }
  }

  addToQueue(base64Data) {
    if (!this.enabled) {
      return;
    }
    this.queue.push(base64Data);
    if (!this.isPlaying) {
      this.playNext();
    }
  }

  playAudio() {
    if (!this.enabled) {
      this.dispatchEvent(new MesopEvent(this.playEvent, {}));
    }
    if (!this.audioContext) {
      this.audioContext = new AudioContext();
    }
    this.playNext();
  }

  playNext() {
    if (!this.enabled || !this.audioContext || this.queue.length === 0) {
      this.isPlaying = false;
      return;
    }

    this.isPlaying = true;
    const data = this.queue.shift();
    const source = this.playPCM(data);

    source.onended = () => {
      this.playNext();
    };
  }

  playPCM(data) {
    // Convert base64 to binary.
    const binaryAudio = atob(data);

    // Convert binary string to ArrayBuffer.
    const audioBuffer = new ArrayBuffer(binaryAudio.length);
    const bufferView = new Uint8Array(audioBuffer);
    for (let i = 0; i < binaryAudio.length; i++) {
      bufferView[i] = binaryAudio.charCodeAt(i);
    }

    // Convert to 16-bit PCM data.
    const pcmData = new Int16Array(audioBuffer);

    // Create audio buffer.
    const frameCount = pcmData.length;
    const audioBufferData = this.audioContext.createBuffer(
      this.channels,
      frameCount,
      this.sampleRate,
    );

    // Get channel data and convert PCM to float32.
    const channelData = audioBufferData.getChannelData(0);
    for (let i = 0; i < frameCount; i++) {
      // Convert 16-bit PCM (-32768 to 32767) to float32 (-1.0 to 1.0)
      channelData[i] = pcmData[i] / 32768.0;
    }

    // Create and play the source.
    const source = this.audioContext.createBufferSource();
    source.buffer = audioBufferData;
    source.connect(this.audioContext.destination);
    source.start();

    return source;
  }

  render() {
    if (this.enabled) {
      return html`<span><slot></slot></span>`;
    }
    return html`<span @click="${this.playAudio}"><slot></slot></span>`;
  }
}

customElements.define('audio-player', AudioPlayer);
