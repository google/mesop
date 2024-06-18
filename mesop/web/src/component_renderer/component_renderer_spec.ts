import {checkAttributeNameIsSafe} from './component_renderer';

describe('component renderer', () => {
  describe('checkAttributeNameIsSafe', () => {
    it('should raise an exception for unsafe attribute keys', () => {
      const unsafeKeys = ['src', 'SRC', 'srcdoc', 'on', 'On', 'ON', 'onClick'];
      unsafeKeys.forEach((key) => {
        expect(() => checkAttributeNameIsSafe(key)).toThrowError(
          `Unsafe attribute name '${key}' cannot be used.`,
        );
      });
    });

    it('should pass for safe attribute keys', () => {
      const safeKeys = ['a', 'decrement', 'click-on'];
      safeKeys.forEach((key) => {
        expect(() => checkAttributeNameIsSafe(key)).not.toThrow();
      });
    });
  });
});
