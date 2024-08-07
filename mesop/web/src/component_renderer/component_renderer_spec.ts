import {checkPropertyNameIsSafe} from './component_renderer';

describe('component renderer', () => {
  describe('checkPropertyNameIsSafe', () => {
    it('should raise an exception for unsafe attribute keys', () => {
      const unsafeKeys = ['src', 'SRC', 'srcdoc', 'on', 'On', 'ON', 'onClick'];
      unsafeKeys.forEach((key) => {
        expect(() => checkPropertyNameIsSafe(key)).toThrowError(
          `Unsafe property name '${key}' cannot be used.`,
        );
      });
    });

    it('should pass for safe attribute keys', () => {
      const safeKeys = ['a', 'decrement', 'click-on'];
      safeKeys.forEach((key) => {
        expect(() => checkPropertyNameIsSafe(key)).not.toThrow();
      });
    });
  });
});
