export interface PriorAction {
  id: string;
  projectNumber: string;
  country: string;
  drmPillar: string;
  priorAction: string;
  resultIndicator: string;
  isTotal?: boolean;
}

export interface PriorActionChartData {
  category: string;
  value: number;
  color?: string;
}
