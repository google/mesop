/* Forked from: https://github.com/heiko-hotz/gemini-multimodal-live-dev-guide/blob/507f87f99bce15fc0c4513c54d9873118e5aef6c/shared/gemini-live-api.js

/*
 Copyright 2024 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
export class GeminiLiveApi {
  constructor(endpoint, autoSetup = true, setupConfig = null) {
    this.ws = new WebSocket(endpoint);
    this.onSetupComplete = () => {};
    this.onAudioData = () => {};
    this.onInterrupted = () => {};
    this.onTurnComplete = () => {};
    this.onError = () => {};
    this.onClose = () => {};
    this.onToolCall = () => {};
    this.pendingSetupMessage = null;
    this.autoSetup = autoSetup;
    this.setupConfig = setupConfig;

    this.setupWebSocket();
  }

  setupWebSocket() {
    this.ws.onopen = () => {
      console.log('WebSocket connection is opening...');
      if (this.autoSetup) {
        this.sendDefaultSetup();
      } else if (this.pendingSetupMessage) {
        console.log('Sending pending setup message:', this.pendingSetupMessage);
        this.ws.send(JSON.stringify(this.pendingSetupMessage));
        this.pendingSetupMessage = null;
      }
    };

    this.ws.onmessage = async (event) => {
      try {
        let wsResponse;
        if (event.data instanceof Blob) {
          const responseText = await event.data.text();
          wsResponse = JSON.parse(responseText);
        } else {
          wsResponse = JSON.parse(event.data);
        }

        console.log('WebSocket Response:', wsResponse);

        if (wsResponse.setupComplete) {
          this.onSetupComplete();
        } else if (wsResponse.toolCall) {
          this.onToolCall(wsResponse.toolCall);
        } else if (wsResponse.serverContent) {
          if (wsResponse.serverContent.interrupted) {
            this.onInterrupted();
            return;
          }

          if (wsResponse.serverContent.modelTurn?.parts?.[0]?.inlineData) {
            const audioData =
              wsResponse.serverContent.modelTurn.parts[0].inlineData.data;
            this.onAudioData(audioData);

            if (!wsResponse.serverContent.turnComplete) {
              this.sendContinueSignal();
            }
          }

          if (wsResponse.serverContent.turnComplete) {
            this.onTurnComplete();
          }
        }
      } catch (error) {
        console.error('Error parsing response:', error);
        this.onError('Error parsing response: ' + error.message);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket Error:', error);
      this.onError('WebSocket Error: ' + error.message);
    };

    this.ws.onclose = (event) => {
      console.log('Connection closed:', event);
      this.onClose(event);
    };
  }

  sendMessage(message) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.error(
        'WebSocket is not open. Current state:',
        this.ws.readyState,
      );
      this.onError('WebSocket is not ready. Please try again.');
    }
  }

  sendSetupMessage(setupMessage) {
    if (this.ws.readyState === WebSocket.OPEN) {
      console.log('Sending setup message:', setupMessage);
      this.ws.send(JSON.stringify(setupMessage));
    } else {
      console.log('Connection not ready, queuing setup message');
      this.pendingSetupMessage = setupMessage;
    }
  }

  sendDefaultSetup() {
    const defaultConfig = {
      model: 'models/gemini-2.0-flash-exp',
      generation_config: {
        response_modalities: ['audio'],
        speech_config: {
          voice_config: {
            prebuilt_voice_config: {
              voice_name: 'Puck',
            },
          },
        },
      },
    };

    const setupMessage = {
      setup: this.setupConfig || defaultConfig,
    };

    this.sendSetupMessage(setupMessage);
  }

  sendAudioChunk(base64Audio) {
    const message = {
      realtime_input: {
        media_chunks: [
          {
            mime_type: 'audio/pcm',
            data: base64Audio,
          },
        ],
      },
    };
    console.log('Sending audio message: ', message);
    this.sendMessage(message);
  }

  sendEndMessage() {
    const message = {
      client_content: {
        turns: [
          {
            role: 'user',
            parts: [],
          },
        ],
        turn_complete: true,
      },
    };
    this.sendMessage(message);
  }

  sendContinueSignal() {
    const message = {
      client_content: {
        turns: [
          {
            role: 'user',
            parts: [],
          },
        ],
        turn_complete: false,
      },
    };
    this.sendMessage(message);
  }

  sendToolResponse(functionResponses) {
    const toolResponse = {
      tool_response: {
        function_responses: functionResponses,
      },
    };
    console.log('Sending tool response:', toolResponse);
    this.sendMessage(toolResponse);
  }

  async ensureConnected() {
    if (this.ws.readyState === WebSocket.OPEN) {
      return;
    }

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Connection timeout'));
      }, 5000);

      const onOpen = () => {
        clearTimeout(timeout);
        this.ws.removeEventListener('open', onOpen);
        this.ws.removeEventListener('error', onError);
        resolve();
      };

      const onError = (error) => {
        clearTimeout(timeout);
        this.ws.removeEventListener('open', onOpen);
        this.ws.removeEventListener('error', onError);
        reject(error);
      };

      this.ws.addEventListener('open', onOpen);
      this.ws.addEventListener('error', onError);
    });
  }
}
