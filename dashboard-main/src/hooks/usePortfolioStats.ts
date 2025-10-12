import { useMemo } from 'react';
import { useFetchApprovalsByFiscalYearRegion } from './useFetchApprovalsByFiscalYearRegion';
import { useFetchRegionByStatus } from './useFetchRegionByStatus';
import { useFetchPortfolioList } from './useFetchPortfolioList';
import { STATUS_TYPES } from '@/components/CatDDO/constants/PortfolioContent.constants';

export interface PortfolioStats {
  totalApproved: number;
  totalCountries: number;
  totalClosed: number;
  totalPipeline: number;
  isLoading: boolean;
}

export function usePortfolioStats(): PortfolioStats {
  const { data: regionData, isLoading: regionLoading } =
    useFetchApprovalsByFiscalYearRegion();
  const { data: statusData, isLoading: statusLoading } =
    useFetchRegionByStatus();
  const { data: portfolioList, isLoading: portfolioLoading } =
    useFetchPortfolioList();

  const stats = useMemo(() => {
    if (
      regionLoading ||
      statusLoading ||
      portfolioLoading ||
      !regionData ||
      !statusData ||
      !portfolioList
    ) {
      return {
        totalApproved: 0,
        totalCountries: 0,
        totalClosed: 0,
        totalPipeline: 0,
        isLoading: true,
      };
    }

    let totalClosed = 0;
    let totalPipeline = 0;
    let totalActive = 0;

    portfolioList.forEach((item) => {
      if (item.status === STATUS_TYPES.Closed) {
        totalClosed += 1;
      } else if (item.status === STATUS_TYPES.Pipeline) {
        totalPipeline += 1;
      } else if (item.status === STATUS_TYPES.Active) {
        totalActive += 1;
      }
    });

    const totalApproved = totalActive + totalClosed;

    const uniqueCountries = new Set(
      portfolioList
        .filter(
          (item) =>
            item.status === STATUS_TYPES.Active ||
            item.status === STATUS_TYPES.Closed
        )
        .map((item) => item.country)
    ).size;

    return {
      totalApproved,
      totalCountries: uniqueCountries,
      totalClosed,
      totalPipeline,
      isLoading: false,
    };
  }, [
    regionData,
    statusData,
    portfolioList,
    regionLoading,
    statusLoading,
    portfolioLoading,
  ]);

  return stats;
}
