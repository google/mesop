import {Component, ElementRef, Inject, OnInit, ViewChild} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CdkDrag, CdkDragEnd} from '@angular/cdk/drag-drop';
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
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'mesop-editor-toolbar',
  templateUrl: 'editor_toolbar.ng.html',
  standalone: true,
  styleUrl: 'editor_toolbar.css',
  imports: [
    MatIconModule,
    MatButtonModule,
    FormsModule,
    MatSnackBarModule,
    CommonModule,
    CdkDrag,
  ],
})
export class EditorToolbar implements OnInit {
  prompt = '';
  responseTime = 0;
  isLoading = false;
  private timerSubscription: Subscription | null = null;
  isToolbarExpanded = true;
  position: {x: number | null; y: number | null} = {x: null, y: null};
  @ViewChild('toolbar', {static: true}) toolbar!: ElementRef;

  constructor(
    private editorToolbarService: EditorToolbarService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
  ) {
    const savedState = localStorage.getItem('isToolbarExpanded');
    this.isToolbarExpanded = savedState === 'true';
  }

  ngOnInit() {
    this.loadSavedPosition();
  }

  toggleToolbar() {
    this.isToolbarExpanded = !this.isToolbarExpanded;
    localStorage.setItem(
      'isToolbarExpanded',
      this.isToolbarExpanded.toString(),
    );
    if (!this.isToolbarExpanded) {
      this.position = {x: null, y: null};
    }
    if (this.isToolbarExpanded) {
      this.loadSavedPosition();
    }
  }

  async onEnter(event: Event) {
    event.preventDefault();
    await this.sendPrompt();
  }

  async sendPrompt() {
    const prompt = this.prompt;
    this.prompt = '';
    this.isLoading = true;
    this.responseTime = 0;

    const startTime = performance.now();
    this.startTimer(startTime);

    try {
      const response = await this.editorToolbarService.sendPrompt(prompt);
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
      this.snackBar.open(
        'An error occurred while processing your request',
        'Close',
        {
          duration: 3000,
        },
      );
    } finally {
      this.stopTimer();
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

  onDragEnded(event: CdkDragEnd) {
    const element = event.source.element.nativeElement;
    const rect = element.getBoundingClientRect();

    // Get position relative to the viewport
    const x = rect.left;
    const y = rect.top;

    this.position = {x, y};
    this.savePosition();
  }

  private loadSavedPosition() {
    const savedPosition = localStorage.getItem('editorToolbarPosition');
    if (!savedPosition) {
      return;
    }
    this.position = JSON.parse(savedPosition);

    // Ensure the toolbar stays within the viewport
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const toolbarRect = this.toolbar.nativeElement.getBoundingClientRect();

    const left = Math.max(0, Math.min(this.position.x!, viewportWidth - 600));
    const top = Math.max(
      0,
      Math.min(this.position.y!, viewportHeight - toolbarRect.height),
    );

    this.toolbar.nativeElement.style.left = `${left}px`;
    this.toolbar.nativeElement.style.top = `${top}px`;
  }

  private savePosition() {
    localStorage.setItem(
      'editorToolbarPosition',
      JSON.stringify(this.position),
    );
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
