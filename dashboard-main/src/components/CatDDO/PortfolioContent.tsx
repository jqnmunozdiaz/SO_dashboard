import React from 'react';
import { When } from 'vizonomy';
import {
  PortfolioContainer,
  PortfolioTitle,
  PortfolioDescription,
  ChartsContainer,
  PortfolioWrapper,
} from './styled';
import { DisbursementChart, RegionChart, StatusChart } from './components';
import { GlobalCatDDO } from './GlobalCatDDO';
import DisbursementTables from './DisbursementTables';
import { ClimateCoBenefits } from './ClimateCoBenefits';
import { usePortfolioStats } from '@/hooks/usePortfolioStats';
import { useFetchMetadata } from '@/hooks/useFetchMetadata';
import { formatLastUpdate } from '@/utils/date-utils';

export const PortfolioContent = () => {
  const {
    totalApproved,
    totalCountries,
    totalClosed,
    isLoading: statsLoading,
  } = usePortfolioStats();
  const { metadata, isLoading: metadataLoading } = useFetchMetadata();

  const formattedDate = formatLastUpdate(metadata, metadataLoading);

  return (
    <PortfolioWrapper>
      <PortfolioContainer>
        <PortfolioTitle>
          Overview of the evolution and composition of the DPF Cat DDO portfolio
        </PortfolioTitle>
        <PortfolioDescription>
          <When condition={statsLoading || metadataLoading}>
            Loading portfolio information...
          </When>
          <When condition={!statsLoading && !metadataLoading}>
            As of {formattedDate}, {totalApproved} DPF Cat DDOs have been
            approved in {totalCountries} countries, with {totalClosed} of these
            operations having already been closed.
          </When>
        </PortfolioDescription>
      </PortfolioContainer>

      <ChartsContainer>
        <RegionChart />
        <StatusChart />
      </ChartsContainer>
      <DisbursementChart />
      <DisbursementTables />
      <GlobalCatDDO />
      <ClimateCoBenefits />
    </PortfolioWrapper>
  );
};

export default PortfolioContent;
