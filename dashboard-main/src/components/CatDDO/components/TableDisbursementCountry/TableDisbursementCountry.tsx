import React from 'react';
import type { TableColumn } from 'vizonomy';
import { Image } from 'vizonomy';
import type { DisbursementCountry } from '../../interfaces';
import {
  TableDisbursementCountryContainer,
  TableDisbursementCountryWrapper_Container,
  TableDisbursementCountryTitle,
  TableCellText,
  TableDisbursementCountryWrapper,
  DownloadButton,
} from './styled/TableDisbursementCountry.styled';
import { useTableDisbursementCountry } from './useTableDisbursementCountry';
import { useCSVDownloader } from '@/hooks/useCSVDownloader';

export const TableDisbursementCountry = () => {
  const { rows, rawData, isLoading } = useTableDisbursementCountry();
  const { downloadCSV } = useCSVDownloader();

  const handleDownloadCSV = () => {
    if (!rawData?.length) return;

    const csvData = rawData.map((row) => ({
      Country: row.country,
      'Net Commitment Amount ($)': row.rawNetCommitment,
      'Cumulative Disbursements ($)': row.rawDisbursements,
    }));

    downloadCSV(csvData, 'disbursements-by-country');
  };

  const columns: TableColumn<DisbursementCountry>[] = [
    {
      id: 'country',
      key: 'country',
      label: 'Country',
      width: '33.33%',
      render: (value: string, row: DisbursementCountry) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'netCommitmentAmount',
      key: 'netCommitmentAmount',
      label: 'Net Comm. Amt. - Total ($M)',
      width: '33.33%',
      align: 'left',
      render: (value: string, row: DisbursementCountry) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'cumulativeDisbursements',
      key: 'cumulativeDisbursements',
      label: 'Disbursements - Cum. Disb. ($M)',
      width: '33.34%',
      align: 'left',
      render: (value: string, row: DisbursementCountry) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
  ];

  return (
    <TableDisbursementCountryContainer>
      <TableDisbursementCountryTitle>
        Disbursements by Country
        <DownloadButton
          onClick={handleDownloadCSV}
          disabled={isLoading || !rawData?.length}
        >
          <Image
            src="/download-icon.svg"
            alt="Download CSV"
            className="w-6 h-6"
          />
        </DownloadButton>
      </TableDisbursementCountryTitle>
      <TableDisbursementCountryWrapper_Container>
        <TableDisbursementCountryWrapper
          data={rows}
          columns={columns}
          rowKey="id"
        />
      </TableDisbursementCountryWrapper_Container>
    </TableDisbursementCountryContainer>
  );
};

export default TableDisbursementCountry;
