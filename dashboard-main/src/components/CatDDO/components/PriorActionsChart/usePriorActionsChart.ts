import { useMemo } from 'react';
import { useFetchPriorActions } from '@/hooks/useFetchPriorActions';
import { makeDrmPillarComparator } from '@/constants/drmPillars';
import { DRM_PILLAR_COLORS } from '@/constants/drmPillars';
import type { PriorAction } from '@/components/CatDDO/interfaces/PriorAction';

export function usePriorActionsChart(filteredRows?: PriorAction[]) {
  const { tableData, isLoading, error } = useFetchPriorActions();

  const chartData = useMemo(() => {
    const dataToUse = filteredRows ?? tableData ?? [];

    if (!dataToUse.length) return [];

    const pillarCounts = new Map<string, number>();

    for (const row of dataToUse) {
      const pillar = row.drmPillar ?? 'Unknown';
      pillarCounts.set(pillar, (pillarCounts.get(pillar) ?? 0) + 1);
    }

    const comparator = makeDrmPillarComparator();
    const sortedPillars = Array.from(pillarCounts.keys()).sort(comparator);

    return sortedPillars.map((pillar) => ({
      id: pillar,
      label: pillar,
      values: {
        [pillar]: pillarCounts.get(pillar) ?? 0,
      },
    }));
  }, [filteredRows, tableData]);

  const series = useMemo(() => {
    if (!chartData.length) return [];

    const pillarColorMap: Record<string, string> = DRM_PILLAR_COLORS;

    return chartData.map((dataPoint) => ({
      key: dataPoint.label,
      label: dataPoint.label,
      color: pillarColorMap[dataPoint.label] ?? '#cccccc',
    }));
  }, [chartData]);

  return {
    data: chartData,
    series,
    isLoading,
    errorMessage: error,
  };
}
