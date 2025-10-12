import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';

// Mock data based on the Figma design showing disbursements by fiscal year and funding source
export const disbursementChartData: StackedBarChartDataPoint[] = [
  {
    id: '2009',
    label: "'09",
    values: { IBRD: 350, IDA: 0 },
  },
  {
    id: '2010',
    label: "'10",
    values: { IBRD: 0, IDA: 0 },
  },
  {
    id: '2011',
    label: "'11",
    values: { IBRD: 260, IDA: 0 },
  },
  {
    id: '2012',
    label: "'12",
    values: { IBRD: 100, IDA: 100 },
  },
  {
    id: '2013',
    label: "'13",
    values: { IBRD: 100, IDA: 0 },
  },
  {
    id: '2014',
    label: "'14",
    values: { IBRD: 100, IDA: 0 },
  },
  {
    id: '2015',
    label: "'15",
    values: { IBRD: 100, IDA: 0 },
  },
  {
    id: '2016',
    label: "'16",
    values: { IBRD: 100, IDA: 100 },
  },
  {
    id: '2017',
    label: "'17",
    values: { IBRD: 140, IDA: 140 },
  },
  {
    id: '2018',
    label: "'18",
    values: { IBRD: 140, IDA: 140 },
  },
  {
    id: '2019',
    label: "'19",
    values: { IBRD: 743, IDA: 7 },
  },
  {
    id: '2020',
    label: "'20",
    values: { IBRD: 1078, IDA: 672 },
  },
  {
    id: '2021',
    label: "'21",
    values: { IBRD: 520, IDA: 0 },
  },
  {
    id: '2022',
    label: "'22",
    values: { IBRD: 520, IDA: 0 },
  },
  {
    id: '2023',
    label: "'23",
    values: { IBRD: 520, IDA: 0 },
  },
  {
    id: '2024',
    label: "'24",
    values: { IBRD: 520, IDA: 0 },
  },
  {
    id: '2025',
    label: "'25",
    values: { IBRD: 520, IDA: 0 },
  },
];

export const disbursementSeries: BarChartSeries[] = [
  { key: 'IBRD', label: 'IBRD', color: '#295e84' },
  { key: 'IDA', label: 'IDA', color: '#89a3c5' },
  { key: 'IBRD and IDA', label: 'IBRD and IDA', color: '#5a7ba8' },
];
