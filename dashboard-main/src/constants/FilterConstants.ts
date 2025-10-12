import type { FilterConfig } from '@/hooks/useFilterTableDDO.d';

export const FILTER_CONFIG: FilterConfig[] = [
  { key: 'fiscalYear', property: 'fiscalYear', placeholder: 'Fiscal Year' },
  { key: 'status', property: 'status', placeholder: 'Status' },
  {
    key: 'covidActivation',
    property: 'activationForCovid',
    placeholder: 'COVID Activation',
  },
  {
    key: 'projectFinancier',
    property: 'financier',
    placeholder: 'Project Financier',
  },
  { key: 'region', property: 'region', placeholder: 'Region' },
  {
    key: 'globalPractice',
    property: 'globalPractice',
    placeholder: 'Global Practice',
  },
  {
    key: 'mixedStandalone',
    property: 'operationType',
    placeholder: 'Mixed/Standalone',
  },
  { key: 'disaster', property: 'disastersTriggered', placeholder: 'Disaster' },
];

export const COUNTRY_FILTER_CONFIG = {
  key: 'country',
  property: 'country',
  placeholder: 'Country',
};
