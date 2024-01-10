import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

const DEFAULT_INSTANCE = new ComponentProto();
/** Simple service to detect whether we are in editor mode. */
export class EditorService {
  isEditorMode(): boolean {
    return false;
  }

  setFocusedComponent(component: ComponentProto): void {}

  getFocusedComponent(): ComponentProto | undefined {
    return DEFAULT_INSTANCE;
  }

  clearFocusedComponent() {}
}
