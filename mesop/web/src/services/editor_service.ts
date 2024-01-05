import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

/** Simple service to detect whether we are in editor mode. */
export class EditorService {
  component = new ComponentProto();
  isEditorMode(): boolean {
    return false;
  }

  setFocusedComponent(component: ComponentProto): void {}

  getFocusedComponent(): ComponentProto {
    return this.component;
  }
}
