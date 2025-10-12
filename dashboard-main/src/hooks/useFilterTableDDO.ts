import { useState, useMemo, useCallback } from 'react';
import type { Option } from 'vizonomy';
import { debounce } from '@/utils/debounce';
import type { PortfolioListRow } from '@/components/CatDDO/components/TablePortfolioList/TablePortfolioList.d';
import type { UseFilterTableDDOProps } from './useFilterTableDDO.d';
import {
  FILTER_CONFIG,
  COUNTRY_FILTER_CONFIG,
} from '@/constants/FilterConstants';
import { useFilters } from '@/contexts/FilterContext';

export function useFilterTableDDO({ rows }: UseFilterTableDDOProps) {
  const [inputValue, setInputValue] = useState('');
  const [filterValue, setFilterValue] = useState('');
  const { filters, updateFilter } = useFilters();

  const [selectedFilters, setSelectedFilters] = useState<
    Record<string, Option[]>
  >(
    FILTER_CONFIG.reduce(
      (acc, config) => {
        acc[config.key] = [];
        return acc;
      },
      {} as Record<string, Option[]>
    )
  );

  const debouncedSetFilterValue = useMemo(
    () => debounce((value: string) => setFilterValue(value), 300),
    [setFilterValue]
  );

  const createOptions = useCallback(
    (
      property: keyof PortfolioListRow,
      prefix: string = '',
      sourceData?: PortfolioListRow[]
    ) => {
      const dataToUse = sourceData ?? rows;
      if (!dataToUse) return [];

      const uniqueValues = Array.from(
        new Set(dataToUse.map((row) => row[property]).filter(Boolean))
      ).sort();

      return uniqueValues.map((value) => ({
        id: `${prefix}-${`${value ?? ''}`.replace(/\s+/g, '-').toLowerCase()}`,
        value: value ?? '',
        label: value ?? '',
      }));
    },
    [rows]
  );

  const applyFilterBySelectedValues = useMemo(
    () =>
      (
        data: PortfolioListRow[],
        selectedOptions: Option[],
        property: keyof PortfolioListRow
      ) => {
        if (!selectedOptions?.length) return data;

        const selectedValues = selectedOptions.map((option) => option.value);
        return data.filter((row) =>
          selectedValues.includes(`${row[property] ?? ''}`)
        );
      },
    []
  );

  const applyFilters = useCallback(
    (data: PortfolioListRow[]) => {
      let filtered = data;

      if (filterValue.trim()) {
        const searchTerm = filterValue.toLowerCase().trim();
        filtered = filtered.filter((row) => {
          const projectId = `${row.projectId ?? ''}`.toLowerCase();
          const projectName = `${row.projectName ?? ''}`.toLowerCase();
          const country = `${row.country ?? ''}`.toLowerCase();
          const region = `${row.region ?? ''}`.toLowerCase();
          const globalPractice = `${row.globalPractice ?? ''}`.toLowerCase();
          const financier = `${row.financier ?? ''}`.toLowerCase();

          return (
            projectId.includes(searchTerm) ||
            projectName.includes(searchTerm) ||
            country.includes(searchTerm) ||
            region.includes(searchTerm) ||
            globalPractice.includes(searchTerm) ||
            financier.includes(searchTerm)
          );
        });
      }

      if (filters.countries?.length) {
        filtered = filtered.filter((row) =>
          filters.countries.includes(
            `${row[COUNTRY_FILTER_CONFIG.property as keyof PortfolioListRow] ?? ''}`
          )
        );
      }

      FILTER_CONFIG.forEach((config) => {
        const selectedOptions = selectedFilters[config.key];
        filtered = applyFilterBySelectedValues(
          filtered,
          selectedOptions,
          config.property as keyof PortfolioListRow
        );
      });

      return filtered;
    },
    [
      filterValue,
      filters.countries,
      selectedFilters,
      applyFilterBySelectedValues,
    ]
  );

  const filterOptions = useMemo((): Record<string, Option[]> => {
    let baseFilteredData = rows;
    if (filterValue.trim()) {
      const searchTerm = filterValue.toLowerCase().trim();
      baseFilteredData = rows.filter((row) => {
        const projectId = `${row.projectId ?? ''}`.toLowerCase();
        const projectName = `${row.projectName ?? ''}`.toLowerCase();
        const country = `${row.country ?? ''}`.toLowerCase();
        const region = `${row.region ?? ''}`.toLowerCase();
        const globalPractice = `${row.globalPractice ?? ''}`.toLowerCase();
        const financier = `${row.financier ?? ''}`.toLowerCase();

        return (
          projectId.includes(searchTerm) ||
          projectName.includes(searchTerm) ||
          country.includes(searchTerm) ||
          region.includes(searchTerm) ||
          globalPractice.includes(searchTerm) ||
          financier.includes(searchTerm)
        );
      });
    }

    let countryFilteredData = baseFilteredData;
    if (filters.countries?.length) {
      countryFilteredData = baseFilteredData.filter((row) =>
        filters.countries.includes(
          `${row[COUNTRY_FILTER_CONFIG.property as keyof PortfolioListRow] ?? ''}`
        )
      );
    }

    let cascadingFilteredData = countryFilteredData;
    FILTER_CONFIG.forEach((config) => {
      const selectedOptions = selectedFilters[config.key];
      cascadingFilteredData = applyFilterBySelectedValues(
        cascadingFilteredData,
        selectedOptions,
        config.property as keyof PortfolioListRow
      );
    });

    const regularFilterOptions = FILTER_CONFIG.reduce(
      (acc, config) => {
        const availableOptions = createOptions(
          config.property as keyof PortfolioListRow,
          config.key,
          cascadingFilteredData
        );
        const selectedOptions = selectedFilters[config.key] ?? [];

        const availableOptionsMap = new Map(
          availableOptions.map((opt) => [opt.value, opt])
        );

        const finalOptions = [...availableOptions];

        selectedOptions.forEach((selectedOption) => {
          if (!availableOptionsMap.has(selectedOption.value)) {
            const optionFromOriginal = createOptions(
              config.property as keyof PortfolioListRow,
              config.key,
              rows
            ).find((opt) => opt.value === selectedOption.value);
            if (optionFromOriginal) {
              finalOptions.push(optionFromOriginal);
            }
          }
        });

        acc[config.key] = finalOptions;
        return acc;
      },
      {} as Record<string, Option[]>
    );

    const countryOptions = createOptions(
      COUNTRY_FILTER_CONFIG.property as keyof PortfolioListRow,
      COUNTRY_FILTER_CONFIG.key,
      baseFilteredData
    );
    const selectedCountryOptions = filters.countries.map((country) => ({
      id: `country-${country.replace(/\s+/g, '-').toLowerCase()}`,
      value: country,
      label: country,
    }));

    const countryOptionsMap = new Map(
      countryOptions.map((opt) => [opt.value, opt])
    );

    const finalCountryOptions = [...countryOptions];

    selectedCountryOptions.forEach((selectedOption) => {
      if (!countryOptionsMap.has(selectedOption.value)) {
        const optionFromOriginal = createOptions(
          COUNTRY_FILTER_CONFIG.property as keyof PortfolioListRow,
          COUNTRY_FILTER_CONFIG.key,
          rows
        ).find((opt) => opt.value === selectedOption.value);
        if (optionFromOriginal) {
          finalCountryOptions.push(optionFromOriginal);
        }
      }
    });

    return {
      ...regularFilterOptions,
      country: finalCountryOptions,
    };
  }, [
    createOptions,
    rows,
    filterValue,
    selectedFilters,
    filters.countries,
    applyFilterBySelectedValues,
  ]);

  const filteredRows = useMemo(() => {
    if (!rows) return rows;
    return applyFilters(rows);
  }, [rows, applyFilters]);

  const handleInputChange = useCallback(
    (value: string) => {
      setInputValue(value);
      debouncedSetFilterValue(value);
    },
    [debouncedSetFilterValue]
  );

  const setFilter = useCallback((filterKey: string, options: Option[]) => {
    setSelectedFilters((prev) => ({
      ...prev,
      [filterKey]: options,
    }));
  }, []);

  const setCountryFilter = useCallback(
    (options: Option[]) => {
      const countryValues = options.map((option) => option.value);
      updateFilter('countries', countryValues);
    },
    [updateFilter]
  );

  const resetFilter = useCallback((filterKey: string) => {
    setSelectedFilters((prev) => ({
      ...prev,
      [filterKey]: [],
    }));
  }, []);

  const resetCountryFilter = useCallback(() => {
    updateFilter('countries', []);
  }, [updateFilter]);

  const resetAllFilters = useCallback(() => {
    setInputValue('');
    setFilterValue('');
    updateFilter('countries', []);
    setSelectedFilters(
      FILTER_CONFIG.reduce(
        (acc, config) => {
          acc[config.key] = [];
          return acc;
        },
        {} as Record<string, Option[]>
      )
    );
  }, [updateFilter]);

  const hasActiveFilters =
    filterValue.trim() ||
    filters.countries?.length ||
    Object.values(selectedFilters).some((filter) => filter?.length);

  const getFilterCounts = useCallback(() => {
    const counts = FILTER_CONFIG.reduce(
      (acc, config) => {
        acc[config.key] = filterOptions[config.key]?.length ?? 0;
        return acc;
      },
      {} as Record<string, number>
    );

    counts.country = filterOptions.country?.length ?? 0;

    return counts;
  }, [filterOptions]);

  const getSelectedCounts = useCallback(() => {
    const counts = FILTER_CONFIG.reduce(
      (acc, config) => {
        acc[config.key] = selectedFilters[config.key]?.length ?? 0;
        return acc;
      },
      {} as Record<string, number>
    );

    counts.country = filters.countries?.length ?? 0;

    return counts;
  }, [selectedFilters, filters.countries]);

  const selectedCountryFilter = useMemo(() => {
    return filters.countries.map((country) => ({
      id: `country-${country.replace(/\s+/g, '-').toLowerCase()}`,
      value: country,
      label: country,
    }));
  }, [filters.countries]);

  return {
    inputValue,
    filterValue,
    selectedFilters,
    selectedCountryFilter,
    filterOptions,
    filteredRows,
    handleInputChange,
    setFilter,
    setCountryFilter,
    resetFilter,
    resetCountryFilter,
    resetAllFilters,
    hasActiveFilters,
    filterConfig: FILTER_CONFIG,
    getFilterCounts,
    getSelectedCounts,
  };
}
