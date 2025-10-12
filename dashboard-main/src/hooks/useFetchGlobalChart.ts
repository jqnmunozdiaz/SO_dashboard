import { useState, useEffect } from 'react';
import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

interface GlobalChartResponse {
  data: StackedBarChartDataPoint[];
  series: BarChartSeries[];
}

export function useFetchGlobalChart() {
  const { filters } = useFilters();
  const [data, setData] = useState<StackedBarChartDataPoint[]>([]);
  const [series, setSeries] = useState<BarChartSeries[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        setError('');

        const url = buildApiUrl('/api/portfolio/global-chart', filters);
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: GlobalChartResponse = await response.json();
        setData(result.data);
        setSeries(result.series);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Failed to fetch global chart data';
        setError(message);
        console.error('Error fetching global chart data:', err);
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [filters]);

  return { data, series, isLoading, error };
}
