export interface PortfolioListRow {
  id: string;
  projectId: string;
  country: string;
  projectName: string;
  fiscalYear: string;
  status: string;
  activationForCovid: string;
  financier: string;
  region: string;
  globalPractice: string;
  operationType: string;
  triggerText?: string;
  additionalInfo?: string;
  healthRelatedEmergencies?: string;
  disastersTriggered?: string;
  link?: string;
}
