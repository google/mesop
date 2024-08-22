import {Component, Inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {EditorToolbarService, PromptResponse} from './editor_toolbar_service';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogModule,
} from '@angular/material/dialog';
import {CodeMirrorComponent} from './code_mirror_component';
import {interval, Subscription} from 'rxjs';

@Component({
  selector: 'mesop-editor-toolbar',
  templateUrl: 'editor_toolbar.ng.html',
  standalone: true,
  styleUrl: 'editor_toolbar.css',
  imports: [MatIconModule, MatButtonModule, FormsModule],
})
export class EditorToolbar {
  prompt = '';
  responseTime = 0;
  isLoading = false;
  private timerSubscription: Subscription | null = null;

  constructor(
    private editorToolbarService: EditorToolbarService,
    private dialog: MatDialog,
  ) {}

  async onEnter(event: Event) {
    event.preventDefault();

    const prompt = this.prompt;
    this.prompt = '';
    this.isLoading = true;
    this.responseTime = 0;

    const startTime = performance.now();
    this.startTimer(startTime);

    try {
      const response = await this.editorToolbarService.sendPrompt(prompt);
      this.stopTimer();
      console.log('response', response);

      // show material dialog
      const dialogRef = this.dialog.open(EditorPromptResponseDialog, {
        data: {response: response, responseTime: this.responseTime},
        width: '90%',
      });

      dialogRef.afterClosed().subscribe((result) => {
        console.log('result', result);
        if (result) {
          console.log('User clicked OK');
          this.editorToolbarService.commit(response.afterCode);
          // Add your logic here for when the user clicks OK
        }
      });
    } catch (error) {
      console.error('Error:', error);
    } finally {
      this.isLoading = false;
    }
  }

  private startTimer(startTime: number) {
    this.timerSubscription = interval(100).subscribe(() => {
      this.responseTime = Number(
        ((performance.now() - startTime) / 1000).toFixed(1),
      );
    });
  }

  private stopTimer() {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
      this.timerSubscription = null;
    }
  }

  ngOnDestroy() {
    this.stopTimer();
  }
}

@Component({
  templateUrl: 'editor_response_dialog.ng.html',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule, CodeMirrorComponent],
})
class EditorPromptResponseDialog {
  constructor(
    @Inject(MAT_DIALOG_DATA)
    public data: {response: PromptResponse; responseTime: number},
  ) {}
}
