import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ExperimentService {
  concurrentUpdatesEnabled = false;
  experimentalEditorToolbarEnabled = false;
  websocketsEnabled = false;
}
