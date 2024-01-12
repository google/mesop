import {ComponentName} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function isComponentNameEquals(a: ComponentName, b: ComponentName) {
  return (
    a.getFnName() === b.getFnName() &&
    a.getCoreModule() === b.getCoreModule() &&
    a.getModulePath() === b.getModulePath()
  );
}
