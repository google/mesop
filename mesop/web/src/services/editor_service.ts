import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

const DEFAULT_INSTANCE = new ComponentProto();

export enum SelectionMode {
  DISABLED = 0,
  SELECTING = 1,
  SELECTED = 2,
}

/** Simple service to detect whether we are in editor mode. */
export class EditorService {
  isEditorMode(): boolean {
    return false;
  }

  getSelectionMode(): SelectionMode {
    return SelectionMode.DISABLED;
  }

  setSelectionMode(mode: SelectionMode): void {}

  toggleSelectionMode(): void {}

  setFocusedComponent(component: ComponentProto): void {}

  setOnSelectedComponent(callback: (component: ComponentProto) => void) {}

  getFocusedComponent(): ComponentProto | undefined {
    return DEFAULT_INSTANCE;
  }

  clearFocusedComponent() {}
}
