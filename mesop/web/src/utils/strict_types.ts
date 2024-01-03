/**
 * A strictly typed wrapper around JSON.parse.
 *
 * Do not call JSON.parse directly elsewhere in the codebase, otherwise we will
 * get type errors downstream.
 *
 * This is a simple workaround to not using strict types as part of the TS compilation step
 * e.g. https://github.com/tensorflow/tensorboard/blob/master/tensorboard/defs/strict_type_check.d.ts
 *
 * @param text
 * @return
 */
export function jsonParse(text: string): unknown {
  // Explicitly type as unknown due to https://github.com/bazelbuild/rules_nodejs/issues/2367
  return JSON.parse(text) as unknown;
}
