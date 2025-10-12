import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';

export const regionChartData: StackedBarChartDataPoint[] = [
  {
    id: '2009',
    label: "'09",
    values: { SAR: 4, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
  {
    id: '2010',
    label: "'10",
    values: { SAR: 0, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
  {
    id: '2011',
    label: "'11",
    values: { SAR: 0, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 3 },
  },
  {
    id: '2012',
    label: "'12",
    values: { SAR: 0, ECA: 2, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
  {
    id: '2013',
    label: "'13",
    values: { SAR: 0, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 1, MNA: 0 },
  },
  {
    id: '2014',
    label: "'14",
    values: { SAR: 0, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 1, MNA: 0 },
  },
  {
    id: '2015',
    label: "'15",
    values: { SAR: 0, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 2 },
  },
  {
    id: '2016',
    label: "'16",
    values: { SAR: 1, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
  {
    id: '2017',
    label: "'17",
    values: { SAR: 0, ECA: 0, AFW: 2, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
  {
    id: '2018',
    label: "'18",
    values: { SAR: 0, ECA: 0, AFW: 2, AFE: 0, EAP: 0, LCR: 0, MNA: 5 },
  },
  {
    id: '2019',
    label: "'19",
    values: { SAR: 0, ECA: 0, AFW: 1, AFE: 1, EAP: 0, LCR: 0, MNA: 5 },
  },
  {
    id: '2020',
    label: "'20",
    values: { SAR: 0, ECA: 0, AFW: 1, AFE: 1, EAP: 1, LCR: 0, MNA: 4 },
  },
  {
    id: '2021',
    label: "'21",
    values: { SAR: 0, ECA: 0, AFW: 1, AFE: 1, EAP: 1, LCR: 0, MNA: 5 },
  },
  {
    id: '2022',
    label: "'22",
    values: { SAR: 0, ECA: 0, AFW: 1, AFE: 1, EAP: 1, LCR: 0, MNA: 6 },
  },
  {
    id: '2023',
    label: "'23",
    values: { SAR: 0, ECA: 0, AFW: 1, AFE: 2, EAP: 2, LCR: 0, MNA: 8 },
  },
  {
    id: '2024',
    label: "'24",
    values: { SAR: 0, ECA: 0, AFW: 1, AFE: 2, EAP: 2, LCR: 0, MNA: 10 },
  },
  {
    id: '2025',
    label: "'25",
    values: { SAR: 2, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
  {
    id: '2026',
    label: "'26",
    values: { SAR: 0, ECA: 0, AFW: 0, AFE: 0, EAP: 0, LCR: 0, MNA: 0 },
  },
];

export const regionSeries: BarChartSeries[] = [
  { key: 'LCR', label: 'LCR', color: '#e7cabc' },
  { key: 'EAP', label: 'EAP', color: '#c35225' },
  { key: 'AFE', label: 'AFE', color: '#9d4449' },
  { key: 'AFW', label: 'AFW', color: '#a3c0e4' },
  { key: 'ECA', label: 'ECA', color: '#89a3c5' },
  { key: 'MNA', label: 'MNA', color: '#6b7280' },
  { key: 'SAR', label: 'SAR', color: '#295e84' },
];
