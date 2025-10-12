export interface DisbursementCountry {
  id: string;
  country: string;
  netCommitmentAmount: string;
  cumulativeDisbursements: string;
  isTotal?: boolean;
}
