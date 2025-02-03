import {
  LitElement,
  html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';
import {GeminiLiveApi} from './gemini_live_api.js';

class GeminiLive extends LitElement {
  static properties = {
    api_config: {type: String},
    enabled: {type: Boolean},
    endpoint: {type: String},
    startEvent: {type: String},
    stopEvent: {type: String},
    input_prompt: {type: String},
    toolCallEvent: {type: String},
    tool_call_responses: {type: String},
  };

  constructor() {
    super();
    this.onAudioInputReceived = (e) => {
      if (!this.api) {
        return;
      }
      this.api.sendAudioChunk(e.detail.data);
    };

    this.onVideoInputReceived = (e) => {
      if (!this.api) {
        return;
      }
      this.sendVideoChunk(e.detail.data);
    };
  }

  connectedCallback() {
    super.connectedCallback();
    window.addEventListener('audio-input-received', this.onAudioInputReceived);
    window.addEventListener('video-input-received', this.onVideoInputReceived);
  }

  disconnectedCallback() {
    super.disconnectedCallback();

    window.removeEventListener(
      'audio-input-received',
      this.onAudioInputReceived,
    );

    window.removeEventListener(
      'video-input-received',
      this.onVideoInputReceived,
    );

    if (this.api) {
      this.api.ws.close();
    }
  }

  firstUpdated() {
    if (this.enabled) {
      this.setupWebSocket();
    }
  }

  setupWebSocket() {
    if (this.api) {
      return;
    }

    this.api = new GeminiLiveApi(
      this.endpoint,
      true,
      JSON.parse(this.api_config),
    );

    this.api.onSetupComplete = () => {
      console.log('Setup complete...');
    };

    this.api.onAudioData = (base64Data) => {
      this.dispatchEvent(
        new CustomEvent('audio-output-received', {
          detail: {data: base64Data},
          // Allow event to cross shadow DOM boundaries (both need to be true)
          bubbles: true,
          composed: true,
        }),
      );
    };

    this.api.onClose = () => {
      console.log('Web socket closed...');
    };

    this.api.onToolCall = (toolCalls) => {
      this.dispatchEvent(
        new MesopEvent(this.toolCallEvent, {
          toolCalls: JSON.stringify(toolCalls.functionCalls),
        }),
      );
    };
  }

  updated(changedProperties) {
    if (
      changedProperties.has('tool_call_responses') &&
      this.tool_call_responses.length > 0
    ) {
      this.api.sendToolResponse(JSON.parse(this.tool_call_responses));
    }
    if (changedProperties.has('input_prompt') && this.input_prompt.length > 0) {
      this.sendTextMessage(this.input_prompt);
    }
  }

  start() {
    if (!this.enabled) {
      this.dispatchEvent(new MesopEvent(this.startEvent, {}));
      this.dispatchEvent(
        new CustomEvent('gemini-live-api-started', {
          detail: {},
          // Allow event to cross shadow DOM boundaries (both need to be true)
          bubbles: true,
          composed: true,
        }),
      );
    }
    this.setupWebSocket();
  }

  stop() {
    this.dispatchEvent(new MesopEvent(this.stopEvent, {}));
    this.dispatchEvent(
      new CustomEvent('gemini-live-api-stopped', {
        detail: {},
        // Allow event to cross shadow DOM boundaries (both need to be true)
        bubbles: true,
        composed: true,
      }),
    );
    if (this.api.ws) {
      this.api.ws.close();
    }
  }

  sendTextMessage(text) {
    this.api.sendMessage({
      client_content: {
        turn_complete: true,
        turns: [{role: 'user', parts: [{text: text}]}],
      },
    });
  }

  sendVideoChunk(base64Image) {
    this.api.sendMessage({
      realtimeInput: {
        mediaChunks: [
          {
            mime_type: 'image/jpeg',
            data: base64Image,
          },
        ],
      },
    });
  }

  render() {
    if (this.enabled) {
      return html`<span @click="${this.stop}"><slot></slot></span>`;
    }
    return html`<span @click="${this.start}"><slot></slot></span>`;
  }
}

customElements.define('gemini-live', GeminiLive);
