import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';

export const BAR_HEIGHT = 20;
export const CHART_PADDING = 120;

export const standaloneChartData: StackedBarChartDataPoint[] = [
  {
    id: 'dominican-republic-19',
    label: 'Dominican Republic (FY19)',
    values: {
      'climate-benefit': 88,
      'non-climate': 12,
    },
  },
  {
    id: 'dominican-republic-20',
    label: 'Dominican Republic (FY20)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'dominican-republic-21',
    label: 'Dominican Republic (FY21)',
    values: {
      'climate-benefit': 92,
      'non-climate': 8,
    },
  },
  {
    id: 'dominican-republic-22',
    label: 'Dominican Republic (FY22)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'dominican-republic-23',
    label: 'Dominican Republic (FY23)',
    values: {
      'climate-benefit': 85,
      'non-climate': 15,
    },
  },
  {
    id: 'dominican-republic-24',
    label: 'Dominican Republic (FY24)',
    values: {
      'climate-benefit': 21,
      'non-climate': 79,
    },
  },
  {
    id: 'dominican-republic-25',
    label: 'Dominican Republic (FY25)',
    values: {
      'climate-benefit': 90,
      'non-climate': 10,
    },
  },
  {
    id: 'dominican-republic-26',
    label: 'Dominican Republic (FY26)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'dominican-republic-27',
    label: 'Dominican Republic (FY27)',
    values: {
      'climate-benefit': 100,
      'non-climate': 0,
    },
  },
  {
    id: 'dominican-republic-28',
    label: 'Dominican Republic (FY28)',
    values: {
      'climate-benefit': 93,
      'non-climate': 7,
    },
  },
  {
    id: 'dominican-republic-29',
    label: 'Dominican Republic (FY29)',
    values: {
      'climate-benefit': 84,
      'non-climate': 16,
    },
  },
  {
    id: 'dominican-republic-30',
    label: 'Dominican Republic (FY30)',
    values: {
      'climate-benefit': 76,
      'non-climate': 24,
    },
  },
];

export const standaloneSeries: BarChartSeries[] = [
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
