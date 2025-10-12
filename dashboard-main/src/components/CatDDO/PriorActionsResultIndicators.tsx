import * as React from 'react';
import { When } from 'vizonomy-ui';
import { Image } from 'vizonomy';
import { PriorActionsChart } from './components/PriorActionsChart';
import { TablePriorActions } from './components/TablePriorActions';
import { useTablePriorActions } from './components/TablePriorActions/useTablePriorActions';
import { useCSVDownloader } from '@/hooks/useCSVDownloader';
import { useFilterPriorActions } from '@/hooks/useFilterPriorActions';
import { FigmaSelect } from './components';
import {
  PriorActionsWrapper,
  PriorActionsContainer,
  PriorActionsTitle,
  PriorActionsContentWrapper,
  PriorActionsChartContainer,
  PriorActionsTableSection,
  DownloadButton,
  PriorActionsSearchInput,
  PriorActionsSearchInputWrapper,
  PriorActionsStyledSearchInput,
  PriorActionsSearchIcon,
  PriorActionsFilterSelect,
  PriorActionsResetAllButton,
} from './styled/PriorActionsResultIndicators.styled';

export const PriorActionsResultIndicators = () => {
  const { rows, isLoading } = useTablePriorActions();
  const { downloadCSV } = useCSVDownloader();

  const {
    inputValue,
    selectedCountryFilter,
    selectedDrmPillarFilter,
    filterOptions,
    filteredRows,
    handleInputChange,
    setCountryFilter,
    setDrmPillarFilter,
    resetAllFilters,
    hasActiveFilters,
  } = useFilterPriorActions({
    rows: rows ?? [],
  });

  const handleDownloadCSV = () => {
    if (!filteredRows?.length) return;

    const csvData = filteredRows
      .filter((row) => !row.isTotal)
      .map((row) => ({
        'P#': row.projectNumber,
        Country: row.country,
        'DRM Pillar': row.drmPillar,
        'Prior Action': row.priorAction,
        'Result Indicator': row.resultIndicator?.replace(/\r?\n/g, ' | '),
      }));

    downloadCSV(csvData, 'prior-actions');
  };

  return (
    <PriorActionsWrapper>
      <PriorActionsContainer>
        <PriorActionsTitle>
          Prior Actions and Result indicators
          <DownloadButton
            onClick={handleDownloadCSV}
            disabled={isLoading || !filteredRows?.length}
          >
            <Image
              src="/download-icon.svg"
              alt="Download CSV"
              className="w-6 h-6"
            />
          </DownloadButton>
        </PriorActionsTitle>

        <PriorActionsContentWrapper>
          <PriorActionsChartContainer>
            <PriorActionsChart filteredRows={filteredRows} />
          </PriorActionsChartContainer>

          <div className="flex items-center justify-between mb-4 w-full">
            <div className="flex items-center gap-4">
              <PriorActionsSearchInput>
                <PriorActionsSearchInputWrapper>
                  <PriorActionsStyledSearchInput
                    placeholder="Search by Project ID..."
                    value={inputValue}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                      handleInputChange(e.target.value);
                    }}
                  />
                  <PriorActionsSearchIcon>
                    <Image
                      alt="Search"
                      className="w-4 h-4"
                      src="/search-icon.svg"
                    />
                  </PriorActionsSearchIcon>
                </PriorActionsSearchInputWrapper>
              </PriorActionsSearchInput>

              <PriorActionsFilterSelect>
                <FigmaSelect
                  options={filterOptions.country ?? []}
                  selected={selectedCountryFilter ?? []}
                  onChange={setCountryFilter}
                  placeholder="Country"
                />
              </PriorActionsFilterSelect>

              <PriorActionsFilterSelect>
                <FigmaSelect
                  options={filterOptions.drmPillars ?? []}
                  selected={selectedDrmPillarFilter ?? []}
                  onChange={setDrmPillarFilter}
                  placeholder="DRM Pillars"
                />
              </PriorActionsFilterSelect>
            </div>

            <div className="flex items-center">
              <When condition={hasActiveFilters}>
                <PriorActionsResetAllButton
                  onClick={resetAllFilters}
                  disabled={!hasActiveFilters}
                >
                  Reset All
                </PriorActionsResetAllButton>
              </When>
            </div>
          </div>

          <PriorActionsTableSection>
            <TablePriorActions rows={filteredRows} isLoading={isLoading} />
          </PriorActionsTableSection>
        </PriorActionsContentWrapper>
      </PriorActionsContainer>
    </PriorActionsWrapper>
  );
};

export default PriorActionsResultIndicators;
