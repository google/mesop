import {Injectable} from '@angular/core';

export interface PromptInteraction extends PromptResponse {
  readonly prompt: string;
  readonly path: string;
}

export interface PromptResponse {
  readonly beforeCode: string;
  readonly afterCode: string;
  readonly diff: string;
}

@Injectable({
  providedIn: 'root',
})
export class EditorToolbarService {
  history: PromptInteraction[] = [];

  getHistory(): readonly PromptInteraction[] {
    return this.history;
  }

  async sendPrompt(prompt: string): Promise<PromptResponse> {
    console.debug('sendPrompt', prompt);
    const path = window.location.pathname;
    const response = await fetch('/__editor__/page-generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({prompt, path}),
    });
    await handleError(response);
    const json = (await response.json()) as PromptResponse;
    // Insert at the top of the history so we display the most recent interactions first.
    this.history.unshift({
      path,
      prompt,
      ...json,
    });
    return json;
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
