import React, { useState } from 'react';
import { When } from 'vizonomy-ui';
import { Image } from 'vizonomy';
import {
  DisbursementTriggersContainer,
  DownloadButtonTrigger,
  FilterSection,
  SearchInput,
  SearchInputWrapper,
  SearchIcon,
  CountryFilter,
  MoreFiltersButton,
  ResetAllButton,
  AdditionalFiltersRow,
  ResetButtonContainer,
  TitleAndFiltersRow,
  TitleSection,
  FiltersSection,
  StyledSearchInput,
} from './styled';
import { TablePortfolioList, FigmaSelect } from './components';
import { useTablePortfolioList } from './components/TablePortfolioList/useTablePortfolioList';
import { useCSVDownloader } from '@/hooks/useCSVDownloader';
import { useFilterTableDDO } from '@/hooks/useFilterTableDDO';

export const DisbursementTriggersContent = () => {
  const { rows, isLoading } = useTablePortfolioList();
  const { downloadCSV } = useCSVDownloader();
  const [showMoreFilters, setShowMoreFilters] = useState(false);

  const {
    inputValue,
    selectedFilters,
    selectedCountryFilter,
    filterOptions,
    filteredRows,
    handleInputChange,
    setFilter,
    setCountryFilter,
    resetAllFilters,
    hasActiveFilters,
    filterConfig,
  } = useFilterTableDDO({
    rows: rows ?? [],
  });

  const handleDownloadCSV = () => {
    if (!filteredRows?.length) return;

    const csvData = filteredRows.map((row) => ({
      'Project ID': row.projectId,
      Country: row.country,
      'Project Name': row.projectName,
      'Fiscal Year': row.fiscalYear,
      Status: row.status,
      'Activation for COVID': row.activationForCovid,
      'Project Financier': row.financier,
      Region: row.region,
      'Global Practice': row.globalPractice,
      'Mixed/Standalone': row.operationType,
      'Trigger from Loan/Financing Agreements': row.triggerText?.replace(
        /\r?\n/g,
        ' | '
      ),
      'Additional Information from Minutes & Program Document':
        row.additionalInfo?.replace(/\r?\n/g, ' | '),
      'Health Related emergencies mentioned in the Trigger':
        row.healthRelatedEmergencies?.replace(/\r?\n/g, ' | '),
      'Disasters that have triggered the DPF Cat DDO':
        row.disastersTriggered?.replace(/\r?\n/g, ' | '),
      'Link to Financing or Loan Agreement': row.link,
    }));

    downloadCSV(csvData, 'portfolio-list');
  };

  return (
    <DisbursementTriggersContainer>
      <TitleAndFiltersRow>
        <TitleSection>
          <DownloadButtonTrigger
            onClick={handleDownloadCSV}
            disabled={isLoading || !filteredRows?.length}
          >
            <Image
              src="/download-icon.svg"
              alt="Download CSV"
              className="w-5 h-5"
            />
          </DownloadButtonTrigger>
        </TitleSection>

        <FiltersSection>
          <SearchInput>
            <SearchInputWrapper>
              <StyledSearchInput
                placeholder="Search projects..."
                value={inputValue}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  handleInputChange(e.target.value);
                }}
              />
              <SearchIcon>
                <Image
                  alt="Search"
                  className="w-4 h-4"
                  src="/search-icon.svg"
                />
              </SearchIcon>
            </SearchInputWrapper>
          </SearchInput>

          <CountryFilter>
            <FigmaSelect
              options={filterOptions.country ?? []}
              selected={selectedCountryFilter ?? []}
              onChange={setCountryFilter}
              placeholder="Country"
              pluralPlaceholder="countries"
            />
          </CountryFilter>

          <MoreFiltersButton
            onClick={() => setShowMoreFilters(!showMoreFilters)}
            isActive={showMoreFilters}
          >
            <Image alt="Filter" className="w-4 h-4" src="/filter-icon.svg" />
          </MoreFiltersButton>
        </FiltersSection>
      </TitleAndFiltersRow>

      <FilterSection>
        <When condition={showMoreFilters}>
          <AdditionalFiltersRow>
            {filterConfig.map((config) => (
              <FigmaSelect
                key={config.key}
                options={filterOptions[config.key] ?? []}
                selected={selectedFilters[config.key] ?? []}
                onChange={(options) => setFilter(config.key, options)}
                placeholder={config.placeholder}
              />
            ))}
          </AdditionalFiltersRow>
        </When>

        <When condition={hasActiveFilters}>
          <ResetButtonContainer>
            <ResetAllButton
              onClick={resetAllFilters}
              disabled={!hasActiveFilters}
            >
              Reset All
            </ResetAllButton>
          </ResetButtonContainer>
        </When>
      </FilterSection>

      <TablePortfolioList rows={filteredRows} isLoading={isLoading} />
    </DisbursementTriggersContainer>
  );
};

export default DisbursementTriggersContent;
