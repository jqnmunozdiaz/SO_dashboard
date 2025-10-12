export const API_BASE_PATH = '';

export const PORTFOLIO_ENDPOINTS = {
  approvalsByFiscalYearRegion: `${API_BASE_PATH}/api/portfolio/approvals-by-fy-region`,
  regionByStatus: `${API_BASE_PATH}/api/portfolio/region-by-status`,
  summaryTable: `${API_BASE_PATH}/api/portfolio/summary-table`,
  list: `${API_BASE_PATH}/api/portfolio/list`,
  triggers: `${API_BASE_PATH}/api/portfolio/triggers`,
  disbursementsByFySource: `${API_BASE_PATH}/api/portfolio/disbursements-by-fy-source`,
} as const;

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface FetchJsonOptions {
  method?: HttpMethod;
  signal?: AbortSignal;
}

export async function fetchJson<TResponse>(
  url: string,
  options: FetchJsonOptions = {}
): Promise<TResponse> {
  const response = await fetch(url, {
    method: options.method ?? 'GET',
    cache: 'no-store',
    signal: options.signal,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  const json = (await response.json()) as TResponse;
  return json;
}
