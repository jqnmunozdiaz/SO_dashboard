import type { BarChartSeries, StackedBarChartDataPoint } from '@/lib/BarChart';

export const BAR_HEIGHT = 20;
export const CHART_PADDING = 120;

export const mixedDPOChartData: StackedBarChartDataPoint[] = [
  {
    id: 'mixed-dpo-19',
    label: 'Dominican Republic (FY19)',
    values: {
      'climate-benefit': 88,
      'non-climate': 12,
    },
  },
  {
    id: 'mixed-dpo-20',
    label: 'Dominican Republic (FY20)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'mixed-dpo-21',
    label: 'Dominican Republic (FY21)',
    values: {
      'climate-benefit': 96,
      'non-climate': 4,
    },
  },
  {
    id: 'mixed-dpo-22',
    label: 'Dominican Republic (FY22)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'mixed-dpo-23',
    label: 'Dominican Republic (FY23)',
    values: {
      'climate-benefit': 95,
      'non-climate': 5,
    },
  },
  {
    id: 'mixed-dpo-24',
    label: 'Dominican Republic (FY24)',
    values: {
      'climate-benefit': 21,
      'non-climate': 79,
    },
  },
  {
    id: 'mixed-dpo-25',
    label: 'Dominican Republic (FY25)',
    values: {
      'climate-benefit': 55,
      'non-climate': 45,
    },
  },
  {
    id: 'mixed-dpo-26',
    label: 'Dominican Republic (FY26)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'mixed-dpo-27',
    label: 'Dominican Republic (FY27)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'mixed-dpo-28',
    label: 'Dominican Republic (FY28)',
    values: {
      'climate-benefit': 92,
      'non-climate': 8,
    },
  },
  {
    id: 'mixed-dpo-29',
    label: 'Dominican Republic (FY29)',
    values: {
      'climate-benefit': 84,
      'non-climate': 16,
    },
  },
  {
    id: 'mixed-dpo-30',
    label: 'Dominican Republic (FY30)',
    values: {
      'climate-benefit': 74,
      'non-climate': 26,
    },
  },
];

export const mixedDPOSeries: BarChartSeries[] = [
  {
    key: 'climate-benefit',
    label: 'Climate Co-Benefits',
    color: '#295e84',
  },
  {
    key: 'non-climate',
    label: 'Non-Climate',
    color: '#89a3c5',
  },
];
