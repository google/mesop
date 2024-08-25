import {Injectable, NgZone} from '@angular/core';
import {SSE} from '../utils/sse';
import {BehaviorSubject, Observable} from 'rxjs';

export interface PromptInteraction extends PromptResponse {
  readonly prompt: string;
  readonly path: string;
}

export interface PromptResponse {
  readonly beforeCode: string;
  readonly afterCode: string;
  readonly diff: string;
}

interface GenerateEndMessage extends PromptResponse {
  type: 'end';
}

interface GenerateProgressMessage {
  type: 'progress';
  data: string;
}

type GenerateData = GenerateEndMessage | GenerateProgressMessage;

@Injectable({
  providedIn: 'root',
})
export class EditorToolbarService {
  history: PromptInteraction[] = [];
  eventSource: SSE | undefined;
  private progressSubject = new BehaviorSubject<string>('');
  progress$: Observable<string> = this.progressSubject.asObservable();

  constructor(private readonly ngZone: NgZone) {}

  getHistory(): readonly PromptInteraction[] {
    return this.history;
  }

  async sendPrompt(prompt: string): Promise<PromptResponse> {
    console.debug('sendPrompt', prompt);
    // Clear the progress subject
    this.progressSubject.next('');
    const path = window.location.pathname;
    return new Promise((resolve, reject) => {
      this.eventSource = new SSE('/__editor__/page-generate', {
        payload: JSON.stringify({prompt, path}),
        headers: {
          'Content-Type': 'application/json',
        },
      });
      this.eventSource.addEventListener('message', (e) => {
        // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
        this.ngZone.run(() => {
          try {
            const data = (e as any).data;
            console.debug('sendPrompt eventSource message', data);
            const obj = JSON.parse(data) as GenerateData;
            if (!obj.type) {
              reject(new Error('Invalid event source message'));
              return;
            }
            if (obj.type === 'end') {
              this.eventSource!.close();
              this.eventSource = undefined;
              const {beforeCode, afterCode, diff} = obj;
              this.history.unshift({
                path,
                prompt,
                beforeCode,
                afterCode,
                diff,
              });
              resolve({beforeCode, afterCode, diff});
            }
            if (obj.type === 'progress') {
              this.progressSubject.next(
                this.progressSubject.getValue() + obj.data,
              );
            }
          } catch (e) {
            console.error('sendPrompt eventSource error', e);
            reject(e);
          }
        });
      });
    });
  }

  async commit(code: string) {
    console.debug('commit', prompt);
    const response = await fetch('/__editor__/page-commit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({code, path: window.location.pathname}),
    });
    await handleError(response);
  }

  async saveInteraction(interaction: PromptInteraction): Promise<string> {
    console.debug('saveInteraction', interaction);
    const response = await fetch('/__editor__/save-interaction', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: interaction.prompt,
        beforeCode: interaction.beforeCode,
        diff: interaction.diff,
      }),
    });
    await handleError(response);
    const json = (await response.json()) as {folder: string};
    return json.folder;
  }
}

async function handleError(response: Response) {
  if (response.ok) {
    return;
  }
  console.error(response.status, response.statusText);
  let error = '';
  try {
    error = await response.text();
  } catch (e) {}
  throw new Error(`${response.status} ${response.statusText} ${error}`);
}
