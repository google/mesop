import {ComponentName} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function isComponentNameEquals(
  a: ComponentName | undefined,
  b: ComponentName | undefined,
) {
  // If either is undefined (even if both is undefined)
  // we should not treat them as equals.
  if (a === undefined || b === undefined) return false;
  return (
    a.getFnName() === b.getFnName() &&
    a.getCoreModule() === b.getCoreModule() &&
    a.getModulePath() === b.getModulePath()
  );
}
