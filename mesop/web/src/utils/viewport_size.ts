import {ViewportSize} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function getViewportSize(): ViewportSize {
  const viewportSize = new ViewportSize();
  viewportSize.setWidth(window.innerWidth);
  viewportSize.setHeight(window.innerHeight);
  return viewportSize;
}
