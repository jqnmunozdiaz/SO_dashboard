'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface FilterState {
  statuses: string[];
  regions: string[];
  countries: string[];
  pillars: string[];
}

interface FilterContextType {
  filters: FilterState;
  setFilters: (filters: FilterState) => void;
  updateFilter: (filterType: keyof FilterState, values: string[]) => void;
  clearFilters: () => void;
  hasActiveFilters: boolean;
}

const FilterContext = createContext<FilterContextType | undefined>(undefined);

const initialFilters: FilterState = {
  statuses: [],
  regions: [],
  countries: [],
  pillars: [],
};

interface FilterProviderProps {
  children: ReactNode;
}

export function FilterProvider({ children }: FilterProviderProps) {
  const [filters, setFilters] = useState<FilterState>(initialFilters);

  const updateFilter = (filterType: keyof FilterState, values: string[]) => {
    setFilters((prev) => ({
      ...prev,
      [filterType]: values,
    }));
  };

  const clearFilters = () => {
    setFilters(initialFilters);
  };

  const hasActiveFilters =
    !!filters.statuses.length ||
    !!filters.regions.length ||
    !!filters.countries.length ||
    !!filters.pillars.length;

  const value: FilterContextType = {
    filters,
    setFilters,
    updateFilter,
    clearFilters,
    hasActiveFilters,
  };

  return (
    <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
  );
}

export function useFilters() {
  const context = useContext(FilterContext);
  if (context === undefined) {
    throw new Error('useFilters must be used within a FilterProvider');
  }
  return context;
}
