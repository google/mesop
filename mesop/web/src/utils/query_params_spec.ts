import {getQueryParamsForTesting} from './query_params';

describe('getQueryParams', () => {
  it('should parse query parameters correctly', () => {
    const result = getQueryParamsForTesting(
      '?param1=value1&param2=value2&param3=value3a&param3=value3b',
    );

    expect(result.length).toBe(3);

    const param1 = result.find((p) => p.getKey() === 'param1');
    expect(param1).toBeDefined();
    expect(param1?.getValuesList()).toEqual(['value1']);

    const param2 = result.find((p) => p.getKey() === 'param2');
    expect(param2).toBeDefined();
    expect(param2?.getValuesList()).toEqual(['value2']);

    const param3 = result.find((p) => p.getKey() === 'param3');
    expect(param3).toBeDefined();
    expect(param3?.getValuesList()).toEqual(['value3a', 'value3b']);
  });

  it('should return an empty array for no query parameters', () => {
    const result = getQueryParamsForTesting('');

    expect(result).toEqual([]);
  });
});
