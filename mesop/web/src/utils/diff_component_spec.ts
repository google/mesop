import {
  Component,
  ComponentDiff,
  ComponentName,
  Key,
  SourceCodeLocation,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {applyComponentDiff} from 'mesop/mesop/web/src/utils/diff';

function createKey(name: string) {
  const key = new Key();
  key.setKey(name);
  return key;
}

function createStyle(color: string, columns: string) {
  const style = new Style();
  style.setColor(color);
  style.setColumns(columns);
  return style;
}

function createType(fnName: string) {
  const componentName = new ComponentName();
  componentName.setCoreModule(true);
  componentName.setFnName(fnName);
  const type = new Type();
  type.setName(componentName);
  type.setValue('value');
  return type;
}

function createSourceCodeLocation(module: string) {
  const sourceCodeLocation = new SourceCodeLocation();
  sourceCodeLocation.setModule(module);
  sourceCodeLocation.setLine(1);
  sourceCodeLocation.setCol(2);
  return sourceCodeLocation;
}

function createDefaultComponent() {
  const c = new Component();
  c.setKey(createKey('key'));
  c.setStyle(createStyle('red', '1'));
  c.setStyleDebugJson('debug json string');
  c.setType(createType('test'));
  c.setSourceCodeLocation(createSourceCodeLocation('x'));
  return c;
}

describe('applyComponentDiff functionality', () => {
  it('applies no diffs when there are no diffs', () => {
    const c = createDefaultComponent();
    const diff = new ComponentDiff();

    applyComponentDiff(c, diff);

    expect(c).toBe(c);
  });

  it('applies diffs on key field', () => {
    // Starting component
    const c = createDefaultComponent();
    // Diff
    const diff = new ComponentDiff();
    diff.setKey(createKey('key2'));
    diff.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    // Expected updates
    const expectedC = createDefaultComponent();
    expectedC.setKey(createKey('key2'));

    applyComponentDiff(c, diff);

    expect(c).toEqual(expectedC);
  });

  it('applies diffs on style field', () => {
    // Starting component
    const c = createDefaultComponent();
    // Diff
    const diff = new ComponentDiff();
    diff.setStyle(createStyle('blue', '100px'));
    diff.setUpdateStrategyStyle(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    // Expected updates
    const expectedC = createDefaultComponent();
    expectedC.setStyle(createStyle('blue', '100px'));

    applyComponentDiff(c, diff);

    expect(c).toEqual(expectedC);
  });

  it('applies diffs on styleDebugJson field', () => {
    // Starting component
    const c = createDefaultComponent();
    // Diff
    const diff = new ComponentDiff();
    diff.setStyleDebugJson('updated debug json');
    diff.setUpdateStrategyStyleDebugJson(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    // Expected updates
    const expectedC = createDefaultComponent();
    expectedC.setStyleDebugJson('updated debug json');

    applyComponentDiff(c, diff);

    expect(c).toEqual(expectedC);
  });

  it('applies diffs on type field', () => {
    // Starting component
    const c = createDefaultComponent();
    // Diff
    const diff = new ComponentDiff();
    diff.setType(createType('updated'));
    diff.setUpdateStrategyType(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    // Expected updates
    const expectedC = createDefaultComponent();
    expectedC.setType(createType('updated'));

    applyComponentDiff(c, diff);

    expect(c).toEqual(expectedC);
  });

  it('applies diffs on sourceCodeLocation field', () => {
    // Starting component
    const c = createDefaultComponent();
    // Diff
    const diff = new ComponentDiff();
    diff.setSourceCodeLocation(createSourceCodeLocation('y'));
    diff.setUpdateStrategySourceCodeLocation(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    // Expected updates
    const expectedC = createDefaultComponent();
    expectedC.setSourceCodeLocation(createSourceCodeLocation('y'));

    applyComponentDiff(c, diff);

    expect(c).toEqual(expectedC);
  });

  it('applies multiple diffs', () => {
    // Starting component
    const c = createDefaultComponent();
    // Diff
    const diff = new ComponentDiff();
    diff.setKey(createKey('key2'));
    diff.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diff.setSourceCodeLocation(createSourceCodeLocation('y'));
    diff.setUpdateStrategySourceCodeLocation(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    // Expected updates
    const expectedC = createDefaultComponent();
    expectedC.setKey(createKey('key2'));
    expectedC.setSourceCodeLocation(createSourceCodeLocation('y'));

    applyComponentDiff(c, diff);

    expect(c).toEqual(expectedC);
  });

  it('applies update diffs on child components', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    c1.addChildren(c1c1);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C1 = new ComponentDiff();
    diffC1C1.setKey(createKey('key2'));
    diffC1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    diffC1C1.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diffC1.addChildren(diffC1C1);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C1 = createDefaultComponent();
    expectedC1C1.setKey(createKey('key2'));
    expectedC1.addChildren(expectedC1C1);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies update diffs on multiple child components', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    const c1c2 = createDefaultComponent();
    c1.addChildren(c1c1);
    c1.addChildren(c1c2);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C1 = new ComponentDiff();
    diffC1C1.setKey(createKey('key1 - update'));
    diffC1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    diffC1C1.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diffC1.addChildren(diffC1C1);
    const diffC1C2 = new ComponentDiff();
    diffC1C2.setIndex(1);
    diffC1C2.setKey(createKey('key2 - update'));
    diffC1C2.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    diffC1C2.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diffC1.addChildren(diffC1C2);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C1 = createDefaultComponent();
    expectedC1C1.setKey(createKey('key1 - update'));
    expectedC1.addChildren(expectedC1C1);
    const expectedC1C2 = createDefaultComponent();
    expectedC1C2.setKey(createKey('key2 - update'));
    expectedC1.addChildren(expectedC1C2);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies add diffs', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    c1.addChildren(c1c1);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C1 = new ComponentDiff();
    diffC1C1.setIndex(1);
    const addC = createDefaultComponent();
    addC.setKey(createKey('key 2'));
    diffC1C1.setComponent(addC);
    diffC1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_ADD);
    diffC1.addChildren(diffC1C1);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C1 = createDefaultComponent();
    expectedC1.addChildren(expectedC1C1);
    const expectedC1C2 = createDefaultComponent();
    expectedC1C2.setKey(createKey('key 2'));
    expectedC1.addChildren(expectedC1C2);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies delete diffs', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    c1.addChildren(c1c1);
    const c1c2 = createDefaultComponent();
    c1.addChildren(c1c2);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C2 = new ComponentDiff();
    diffC1C2.setIndex(1);
    diffC1C2.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_DELETE);
    diffC1.addChildren(diffC1C2);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC11 = createDefaultComponent();
    expectedC1.addChildren(expectedC11);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies mutliple delete diffs', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    c1.addChildren(c1c1);
    const c1c2 = createDefaultComponent();
    c1.addChildren(c1c2);
    const c1c3 = createDefaultComponent();
    c1.addChildren(c1c3);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C2 = new ComponentDiff();
    diffC1C2.setIndex(1);
    diffC1C2.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_DELETE);
    diffC1.addChildren(diffC1C2);
    const diffC1C3 = new ComponentDiff();
    diffC1C3.setIndex(2);
    diffC1C3.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_DELETE);
    diffC1.addChildren(diffC1C3);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C1 = createDefaultComponent();
    expectedC1.addChildren(expectedC1C1);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies update / delete diffs on child components', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    c1.addChildren(c1c1);
    const c1c2 = createDefaultComponent();
    c1.addChildren(c1c2);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C1 = new ComponentDiff();
    diffC1C1.setKey(createKey('key2'));
    diffC1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    diffC1C1.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diffC1.addChildren(diffC1C1);
    const diffC1C2 = new ComponentDiff();
    diffC1C2.setIndex(1);
    diffC1C2.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_DELETE);
    diffC1.addChildren(diffC1C2);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C2 = createDefaultComponent();
    expectedC1C2.setKey(createKey('key2'));
    expectedC1.addChildren(expectedC1C2);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies update / add diffs on child components', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    c1.addChildren(c1c1);
    // Diff
    const diffC1 = new ComponentDiff();
    const diffC1C1 = new ComponentDiff();
    diffC1C1.setKey(createKey('key2'));
    diffC1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    diffC1C1.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diffC1.addChildren(diffC1C1);
    const diffC1C2 = new ComponentDiff();
    diffC1C2.setIndex(1);
    diffC1C2.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_ADD);
    const addC = createDefaultComponent();
    diffC1C2.setComponent(addC);
    diffC1.addChildren(diffC1C2);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C1 = createDefaultComponent();
    expectedC1C1.setKey(createKey('key2'));
    expectedC1.addChildren(expectedC1C1);
    const expectedC1C2 = createDefaultComponent();
    expectedC1.addChildren(expectedC1C2);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });

  it('applies diffs on child child components', () => {
    // Starting component
    const c1 = createDefaultComponent();
    const c1c1 = createDefaultComponent();
    const c1c1c1 = createDefaultComponent();
    c1c1.addChildren(c1c1c1);
    c1.addChildren(c1c1);
    // Diff
    const diffC1 = new ComponentDiff();
    diffC1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    const diffC1C1 = new ComponentDiff();
    diffC1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    const diffC1C1C1 = new ComponentDiff();
    diffC1C1C1.setKey(createKey('key1 - update'));
    diffC1C1C1.setDiffType(ComponentDiff.DiffType.DIFF_TYPE_UPDATE);
    diffC1C1C1.setUpdateStrategyKey(
      ComponentDiff.UpdateStrategy.UPDATE_STRATEGY_REPLACE,
    );
    diffC1C1.addChildren(diffC1C1C1);
    diffC1.addChildren(diffC1C1);
    // Expected updates
    const expectedC1 = createDefaultComponent();
    const expectedC1C1 = createDefaultComponent();
    const expectedC1C1C1 = createDefaultComponent();
    expectedC1C1C1.setKey(createKey('key1 - update'));
    expectedC1C1.addChildren(expectedC1C1C1);
    expectedC1.addChildren(expectedC1C1);

    applyComponentDiff(c1, diffC1);

    expect(c1).toEqual(expectedC1);
  });
});
