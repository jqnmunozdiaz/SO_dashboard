import { useState, useEffect } from 'react';
import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';
import type { PriorActionRow } from '@/lib/portfolio';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

interface PriorActionsResponse {
  chartData: StackedBarChartDataPoint[];
  series: BarChartSeries[];
  tableData: PriorActionRow[];
}

export function useFetchPriorActions() {
  const { filters } = useFilters();
  const [chartData, setChartData] = useState<StackedBarChartDataPoint[]>([]);
  const [series, setSeries] = useState<BarChartSeries[]>([]);
  const [tableData, setTableData] = useState<PriorActionRow[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        setError('');

        const url = buildApiUrl('/api/portfolio/prior-actions', filters);
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: PriorActionsResponse = await response.json();
        setChartData(result.chartData);
        setSeries(result.series);
        setTableData(result.tableData);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Failed to fetch prior actions data';
        setError(message);
        console.error('Error fetching prior actions data:', err);
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [filters]);

  return { chartData, series, tableData, isLoading, error };
}
