import React from 'react';
import type { TableColumn } from 'vizonomy';
import { Image } from 'vizonomy';
import type { DisbursementRegion } from '../../interfaces';
import {
  TableDisbursementRegionContainer,
  TableDisbursementRegionWrapper_Container,
  TableDisbursementRegionTitle,
  TableCellText,
  TableDisbursementRegionWrapper,
  DownloadButton,
} from './styled/TableDisbursementRegion.styled';
import { useTableDisbursementRegion } from './useTableDisbursementRegion';
import { useCSVDownloader } from '@/hooks/useCSVDownloader';

export const TableDisbursementRegion = () => {
  const { rows, rawData, isLoading } = useTableDisbursementRegion();
  const { downloadCSV } = useCSVDownloader();

  const handleDownloadCSV = () => {
    if (!rawData?.length) return;

    const csvData = rawData.map((row) => ({
      Region: row.region,
      'Net Commitment Amount ($)': row.rawNetCommitment,
      'Cumulative Disbursements ($)': row.rawDisbursements,
    }));

    downloadCSV(csvData, 'disbursements-by-region');
  };

  const columns: TableColumn<DisbursementRegion>[] = [
    {
      id: 'region',
      key: 'region',
      label: 'Region',
      width: '33.33%',
      render: (value: string, row: DisbursementRegion) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'netCommitmentAmount',
      key: 'netCommitmentAmount',
      label: 'Net Comm. Amt. - Total ($M)',
      width: '33.33%',
      align: 'left',
      render: (value: string, row: DisbursementRegion) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'cumulativeDisbursements',
      key: 'cumulativeDisbursements',
      label: 'Disbursements - Cum. Disb. ($M)',
      width: '33.34%',
      align: 'left',
      render: (value: string, row: DisbursementRegion) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
  ];

  return (
    <TableDisbursementRegionContainer>
      <TableDisbursementRegionTitle>
        Disbursements by Region
        <DownloadButton
          onClick={handleDownloadCSV}
          disabled={isLoading || !rawData || rawData.length === 0}
        >
          <Image
            src="/download-icon.svg"
            alt="Download CSV"
            className="w-6 h-6"
          />
        </DownloadButton>
      </TableDisbursementRegionTitle>
      <TableDisbursementRegionWrapper_Container>
        <TableDisbursementRegionWrapper
          data={rows}
          columns={columns}
          rowKey="id"
        />
      </TableDisbursementRegionWrapper_Container>
    </TableDisbursementRegionContainer>
  );
};

export default TableDisbursementRegion;
