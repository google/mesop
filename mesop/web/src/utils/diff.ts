import {
  Component,
  ComponentDiff,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

/** Updates the given component in place with the provided diffs. */
export function applyComponentDiff(component: Component, diff: ComponentDiff) {
  if (
    diff.getUpdateStrategyKey() ===
    ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE
  ) {
    component.setKey(diff.getKey());
  }
  if (
    diff.getUpdateStrategySourceCodeLocation() ===
    ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE
  ) {
    component.setSourceCodeLocation(diff.getSourceCodeLocation());
  }
  if (
    diff.getUpdateStrategyStyle() ===
    ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE
  ) {
    component.setStyle(diff.getStyle());
  }
  if (
    diff.getUpdateStrategyStyleDebugJson() ===
    ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE
  ) {
    component.setStyleDebugJson(diff.getStyleDebugJson() as string);
  }
  if (
    diff.getUpdateStrategyType() ===
    ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE
  ) {
    component.setType(diff.getType());
  }

  let deleteIndex = -1;
  for (const childDiff of diff.getChildrenList()) {
    if (childDiff.getDiffType() === ComponentDiff.DiffType.DIFF_TYPE_UPDATE) {
      applyComponentDiff(
        component.getChildrenList()[childDiff.getIndex() as number],
        childDiff,
      );
    } else if (
      // We do not care about adding the node to a specific index since we expect
      // additions to be added in order after all updates.
      //
      // Once deletions are applied, the additions should be at the expected location
      // in the component tree.
      childDiff.getDiffType() === ComponentDiff.DiffType.DIFF_TYPE_ADD
    ) {
      component.addChildren(childDiff.getComponent());
    } else if (
      childDiff.getDiffType() === ComponentDiff.DiffType.DIFF_TYPE_DELETE &&
      (deleteIndex === -1 || (childDiff.getIndex() as number) < deleteIndex)
    ) {
      // Only track the smallest `deleteIndex` if there are deletions. See comment
      // below.
      deleteIndex = childDiff.getIndex() as number;
    }
  }

  // If deleteIndex is set to a non-negative number, this means that we have child nodes
  // to delete.
  //
  // Due to the way deletes are determined, we know that deletes will always occur
  // sequentially to the end of the list. This allows us to delete all nodes after the
  // lowest `deleteIndex` found.
  if (deleteIndex !== -1) {
    component.setChildrenList(
      component.getChildrenList().slice(0, deleteIndex),
    );
  }
}
