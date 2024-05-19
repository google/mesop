import {Component, Input, NgZone} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {
  AudioChunk,
  MicType,
} from 'mesop/mesop/components/mic/mic_jspb_proto_pb/mesop/components/mic/mic_pb';
import {Channel} from '../../web/src/services/channel';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';

interface ExtendedWindow extends Window {
  // Exists on Chromium browsers.
  webkitSpeechRecognition: any;
}

enum MicState {
  NOT_STARTED = 0,
  WAITING = 1,
  LISTENING = 2,
}

@Component({
  selector: 'mesop-mic',
  templateUrl: 'mic.ng.html',
  standalone: true,
  imports: [MatButtonModule, MatIconModule],
})
export class MicComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: MicType;
  isChecked = false;
  recognition: any;
  finalTranscript = '';
  interimTranscript = '';
  mediaRecorder!: MediaRecorder;
  chunks: Blob[] = [];
  state: MicState = MicState.NOT_STARTED;

  constructor(
    private readonly channel: Channel,
    private ngZone: NgZone,
  ) {}

  ngOnChanges() {
    this._config = MicType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): MicType {
    return this._config;
  }

  getIcon(): string {
    switch (this.state) {
      case MicState.NOT_STARTED:
        return 'mic';
      case MicState.LISTENING:
        return 'graphic_eq';
      case MicState.WAITING:
        return 'pause_circle';
    }
  }

  async emitChunk(chunks: Blob[]) {
    if (!this.finalTranscript) {
      // Could just be a random sound like clearing a throat
      // so don't bother sending it.
      return;
    }
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnChunkEventHandlerId()!);
    userEvent.setKey(this.key);
    const chunk = new AudioChunk();
    chunk.setTranscript(this.finalTranscript);
    const dataUint8Array = await blobsToUint8Array(chunks);
    chunk.setData(dataUint8Array);
    userEvent.setBytesValue(chunk.serializeBinary());
    this.channel.dispatch(userEvent);
  }

  onClick(event: Event) {
    this.startRecognitionAndRecording();
  }

  startRecognitionAndRecording() {
    this.state = MicState.WAITING;
    const extendedWindow = window as unknown as ExtendedWindow;
    this.recognition = new extendedWindow.webkitSpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-US';
    this.recognition.onresult = (event: any) => {
      this.ngZone.run(() => {
        this.state = MicState.LISTENING;
        console.log('listening');
        this.interimTranscript = '';
        this.finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            this.finalTranscript += `${transcript} `;
          } else {
            this.interimTranscript += transcript;
          }
        }
      });
    };

    this.recognition.onend = () => {
      console.log('Speech recognition ended');
      this.stopRecognitionAndRecording();
    };

    navigator.mediaDevices
      .getUserMedia({audio: true})
      .then((stream) => {
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.start();

        this.mediaRecorder.addEventListener('dataavailable', (event) => {
          this.chunks.push(event.data);
        });

        this.recognition.start();
        console.log('Speech recognition and recording started');
      })
      .catch((err) => {
        console.error('Error accessing the microphone:', err);
      });
  }

  stopRecognitionAndRecording() {
    this.recognition.stop();
    this.mediaRecorder.stop();

    this.mediaRecorder.addEventListener('stop', () => {
      this.emitChunk(this.chunks);
      this.chunks = [];
      this.startRecognitionAndRecording();
    });
  }
}

async function blobsToUint8Array(blobs: Blob[]): Promise<Uint8Array> {
  // Combine all blobs into one
  const combinedBlob = new Blob(blobs);

  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      // Convert the array buffer to Uint8Array
      resolve(new Uint8Array(reader.result as ArrayBuffer));
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(combinedBlob);
  });
}
