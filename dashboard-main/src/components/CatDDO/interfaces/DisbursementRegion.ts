export interface DisbursementRegion {
  id: string;
  region: string;
  netCommitmentAmount: string;
  cumulativeDisbursements: string;
  isTotal?: boolean;
}
