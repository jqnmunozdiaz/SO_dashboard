import { useState, useEffect, useCallback } from 'react';
import { useFetchFilters } from '@/hooks/useFetchFilters';
import { useFilters } from '@/contexts/FilterContext';
import { useTab } from '@/contexts/TabContext';
import { REGION_LABELS } from './Sidebar.constants';
import { makeDrmPillarComparator } from '@/constants/drmPillars';

export type FilterSection = {
  id: string;
  title: string;
  hasFilterIcon: boolean;
  options: Array<{
    id: string;
    label: string;
    isSelected: boolean;
  }>;
};

export const useSidebar = () => {
  const { filterData, isLoading, error } = useFetchFilters();
  const { filters, updateFilter } = useFilters();
  const { activeTab } = useTab();
  const [filterSections, setFilterSections] = useState<FilterSection[]>([]);
  const [isDRMModalOpen, setIsDRMModalOpen] = useState(false);

  useEffect(() => {
    if (filterData) {
      const comparator = makeDrmPillarComparator();
      const orderedPillars = (filterData.pillars ?? [])
        .slice()
        .sort(comparator);

      const sections: FilterSection[] = [
        {
          id: 'project-status',
          title: 'Project Status',
          hasFilterIcon: true,
          options: filterData.statuses.map((status) => ({
            id: status.toLowerCase().replace(/\s+/g, '-'),
            label: status,
            isSelected: filters.statuses.includes(status),
          })),
        },
      ];

      if (activeTab !== 'policy') {
        sections.push(
          {
            id: 'region',
            title: 'Region',
            hasFilterIcon: true,
            options: filterData.regions.map((region) => ({
              id: region.toLowerCase().replace(/\s+/g, '-'),
              label: REGION_LABELS[region] || region,
              isSelected: filters.regions.includes(region),
            })),
          },
          {
            id: 'country',
            title: 'Country',
            hasFilterIcon: true,
            options: filterData.countries.map((country) => ({
              id: country.toLowerCase().replace(/\s+/g, '-'),
              label: country,
              isSelected: filters.countries.includes(country),
            })),
          }
        );
      }

      if (activeTab === 'policy' && filterData.pillars) {
        sections.push({
          id: 'pillar',
          title: 'DRM Pillar',
          hasFilterIcon: true,
          options: orderedPillars.map((pillar) => ({
            id: pillar.toLowerCase().replace(/\s+/g, '-'),
            label: pillar,
            isSelected: filters.pillars.includes(pillar),
          })),
        });
      }

      setFilterSections(sections);
    }
  }, [filterData, filters, activeTab]);

  const handleFilterToggle = useCallback(
    (sectionId: string, optionId: string) => {
      // Update local state immediately for UI responsiveness
      setFilterSections((prevSections) =>
        prevSections.map((section) => {
          if (section.id === sectionId) {
            return {
              ...section,
              options: section.options.map((option) => {
                if (option.id === optionId) {
                  return { ...option, isSelected: !option.isSelected };
                }
                return option;
              }),
            };
          }
          return section;
        })
      );

      // Update context in the next tick to avoid render issues
      setTimeout(() => {
        if (sectionId === 'project-status') {
          const status = filterData?.statuses.find(
            (s) => s.toLowerCase().replace(/\s+/g, '-') === optionId
          );
          if (status) {
            const isCurrentlySelected = filters.statuses.includes(status);
            const newStatuses = isCurrentlySelected
              ? filters.statuses.filter((s) => s !== status)
              : [...filters.statuses, status];
            updateFilter('statuses', newStatuses);
          }
        } else if (sectionId === 'region') {
          const region = filterData?.regions.find(
            (r) => r.toLowerCase().replace(/\s+/g, '-') === optionId
          );
          if (region) {
            const isCurrentlySelected = filters.regions.includes(region);
            const newRegions = isCurrentlySelected
              ? filters.regions.filter((r) => r !== region)
              : [...filters.regions, region];
            updateFilter('regions', newRegions);
          }
        } else if (sectionId === 'country') {
          const country = filterData?.countries.find(
            (c) => c.toLowerCase().replace(/\s+/g, '-') === optionId
          );
          if (country) {
            const isCurrentlySelected = filters.countries.includes(country);
            const newCountries = isCurrentlySelected
              ? filters.countries.filter((c) => c !== country)
              : [...filters.countries, country];
            updateFilter('countries', newCountries);
          }
        } else if (sectionId === 'pillar') {
          const pillar = filterData?.pillars?.find(
            (p) => p.toLowerCase().replace(/\s+/g, '-') === optionId
          );
          if (pillar) {
            const isCurrentlySelected = filters.pillars.includes(pillar);
            const newPillars = isCurrentlySelected
              ? filters.pillars.filter((p) => p !== pillar)
              : [...filters.pillars, pillar];
            updateFilter('pillars', newPillars);
          }
        }
      }, 0);
    },
    [filterData, filters, updateFilter]
  );

  const handleResetFilters = useCallback(() => {
    setFilterSections((prevSections) =>
      prevSections.map((section) => ({
        ...section,
        options: section.options.map((option) => ({
          ...option,
          isSelected: false,
        })),
      }))
    );

    setTimeout(() => {
      updateFilter('statuses', []);
      updateFilter('regions', []);
      updateFilter('countries', []);
      updateFilter('pillars', []);
    }, 0);
  }, [updateFilter]);

  const handleUnderstandingData = useCallback(() => {
    setIsDRMModalOpen(true);
  }, []);

  const handleCloseDRMModal = useCallback(() => {
    setIsDRMModalOpen(false);
  }, []);

  return {
    filterSections,
    isLoading,
    error,
    handleFilterToggle,
    handleResetFilters,
    handleUnderstandingData,
    isDRMModalOpen,
    handleCloseDRMModal,
  };
};
