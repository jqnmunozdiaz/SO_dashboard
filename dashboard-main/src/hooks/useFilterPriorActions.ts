import { useState, useMemo, useCallback } from 'react';
import type { Option } from 'vizonomy';
import { debounce } from '@/utils/debounce';
import type { PriorAction } from '@/components/CatDDO/interfaces/PriorAction';
import { useFilters } from '@/contexts/FilterContext';
import { makeDrmPillarComparator } from '@/constants/drmPillars';

export interface UseFilterPriorActionsProps {
  rows: PriorAction[];
}

export function useFilterPriorActions({ rows }: UseFilterPriorActionsProps) {
  const [inputValue, setInputValue] = useState('');
  const [filterValue, setFilterValue] = useState('');
  const [selectedCountryFilter, setSelectedCountryFilter] = useState<Option[]>(
    []
  );
  const { filters, updateFilter } = useFilters();

  const debouncedSetFilterValue = useMemo(
    () => debounce((value: string) => setFilterValue(value), 300),
    [setFilterValue]
  );

  const createOptions = useCallback(
    (property: keyof PriorAction, prefix: string = '') => {
      if (!rows) return [];

      const uniqueValues = Array.from(
        new Set(rows.map((row) => row[property]).filter(Boolean))
      ) as string[];

      const sortedValues =
        property === 'drmPillar'
          ? uniqueValues.sort(makeDrmPillarComparator())
          : uniqueValues.sort();

      return sortedValues.map((value) => ({
        id: `${prefix}-${`${value ?? ''}`.replace(/\s+/g, '-').toLowerCase()}`,
        value: value ?? '',
        label: value ?? '',
      }));
    },
    [rows]
  );

  const applyFilters = useCallback(
    (data: PriorAction[]) => {
      let filtered = data;

      if (filterValue.trim()) {
        const searchTerm = filterValue.toLowerCase().trim();
        filtered = filtered.filter((row) => {
          const projectNumber = `${row.projectNumber ?? ''}`.toLowerCase();
          return projectNumber.includes(searchTerm);
        });
      }

      if (selectedCountryFilter?.length) {
        const selectedCountryValues = selectedCountryFilter.map(
          (option) => option.value
        );
        filtered = filtered.filter((row) =>
          selectedCountryValues.includes(`${row.country ?? ''}`)
        );
      }

      if (filters.pillars?.length) {
        filtered = filtered.filter((row) =>
          filters.pillars.includes(`${row.drmPillar ?? ''}`)
        );
      }

      return filtered;
    },
    [filterValue, selectedCountryFilter, filters.pillars]
  );

  const filterOptions = useMemo((): Record<string, Option[]> => {
    const countryOptions = createOptions('country', 'country');
    const drmPillarOptions = createOptions('drmPillar', 'drm-pillar');

    return {
      country: countryOptions,
      drmPillars: drmPillarOptions,
    };
  }, [createOptions]);

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

  const setCountryFilter = useCallback((options: Option[]) => {
    setSelectedCountryFilter(options);
  }, []);

  const setDrmPillarFilter = useCallback(
    (options: Option[]) => {
      const pillarValues = options.map((option) => option.value);
      updateFilter('pillars', pillarValues);
    },
    [updateFilter]
  );

  const resetAllFilters = useCallback(() => {
    setInputValue('');
    setFilterValue('');
    setSelectedCountryFilter([]);
    updateFilter('pillars', []);
  }, [updateFilter]);

  const hasActiveFilters =
    filterValue.trim() ||
    selectedCountryFilter?.length ||
    filters.pillars?.length;

  const selectedDrmPillarFilter = useMemo(() => {
    return filters.pillars.map((pillar) => ({
      id: `drm-pillar-${pillar.replace(/\s+/g, '-').toLowerCase()}`,
      value: pillar,
      label: pillar,
    }));
  }, [filters.pillars]);

  return {
    inputValue,
    filterValue,
    selectedCountryFilter,
    selectedDrmPillarFilter,
    filterOptions,
    filteredRows,
    handleInputChange,
    setCountryFilter,
    setDrmPillarFilter,
    resetAllFilters,
    hasActiveFilters,
  };
}
