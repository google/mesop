import {QueryParam} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function getQueryParams() {
  return getQueryParamsForTesting(window.location.search);
}

/** Only exported for unit testing. */
export function getQueryParamsForTesting(queryString: string): QueryParam[] {
  const urlParams = new URLSearchParams(queryString);
  const params: Record<string, string[]> = {};
  urlParams.forEach((value, key) => {
    if (!params[key]) {
      params[key] = [value];
    } else {
      params[key].push(value);
    }
  });
  const queryParams: QueryParam[] = [];
  for (const [key, values] of Object.entries(params)) {
    const queryParam = new QueryParam();
    queryParam.setKey(key);
    queryParam.setValuesList(values);
    queryParams.push(queryParam);
  }
  return queryParams;
}
