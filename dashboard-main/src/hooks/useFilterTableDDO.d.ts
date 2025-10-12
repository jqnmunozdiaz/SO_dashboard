import type { PortfolioListRow } from '@/components/CatDDO/components/TablePortfolioList/TablePortfolioList.d';

export interface FilterConfig {
  key: string;
  property: string;
  placeholder: string;
}

export interface UseFilterTableDDOProps {
  rows: PortfolioListRow[];
}
