'use client';

import React from 'react';
import { When } from 'vizonomy';
import type { TableColumn } from 'vizonomy';
import {
  TableFundingContainer,
  TableFundingWrapper,
  TableCellText,
} from '../TableFundingDDO/styled/TableFundingDDO.styled';
import { TableLink } from './styled/TablePortfolioList.styled';
import type { PortfolioListRow } from './TablePortfolioList.d';

interface TablePortfolioListProps {
  rows: PortfolioListRow[];
  isLoading: boolean;
}

export function TablePortfolioList({
  rows,
  isLoading,
}: TablePortfolioListProps) {
  const columns: TableColumn<PortfolioListRow>[] = [
    {
      id: 'projectId',
      key: 'projectId',
      label: 'Project ID',
      width: 90,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'country',
      key: 'country',
      label: 'Country',
      width: 120,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'projectName',
      key: 'projectName',
      label: 'Project Name',
      width: 260,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'fiscalYear',
      key: 'fiscalYear',
      label: 'Fiscal Year',
      width: 80,
      align: 'center',
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'status',
      key: 'status',
      label: 'Status',
      width: 90,
      align: 'center',
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'activationForCovid',
      key: 'activationForCovid',
      label: 'Activation for COVID',
      width: 120,
      align: 'center',
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'financier',
      key: 'financier',
      label: 'Project Financier',
      width: 120,
      align: 'center',
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'region',
      key: 'region',
      label: 'Region',
      width: 80,
      align: 'center',
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'globalPractice',
      key: 'globalPractice',
      label: 'Global Practice',
      width: 180,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'operationType',
      key: 'operationType',
      label: 'Mixed/Standalone',
      width: 140,
      align: 'center',
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'triggerText',
      key: 'triggerText',
      label: 'Trigger from Loan/Financing Agreements',
      width: 400,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'additionalInfo',
      key: 'additionalInfo',
      label: 'Additional Information from Minutes & Program Document',
      width: 360,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'healthRelatedEmergencies',
      key: 'healthRelatedEmergencies',
      label: 'Health Related emergencies mentioned in the Trigger',
      width: 320,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'disastersTriggered',
      key: 'disastersTriggered',
      label: 'Disasters that have triggered the DPF Cat DDO',
      width: 320,
      sortable: true,
      render: (v: string) => <TableCellText>{v}</TableCellText>,
    },
    {
      id: 'link',
      key: 'link',
      label: 'Link to Financing or Loan Agreement',
      width: 300,
      sortable: true,
      render: (v: string) => (
        <TableCellText>
          <When condition={!!v}>
            <TableLink href={v}>{v}</TableLink>
          </When>
          <When condition={!v}>-</When>
        </TableCellText>
      ),
    },
  ];

  if (isLoading) {
    return (
      <TableFundingContainer>
        <div className="flex items-center justify-center py-8">
          <div className="text-gray-500">Loading portfolio data...</div>
        </div>
      </TableFundingContainer>
    );
  }

  if (!rows?.length) {
    return (
      <TableFundingContainer>
        <div className="flex items-center justify-center py-8">
          <div className="text-gray-500">No portfolio data available</div>
        </div>
      </TableFundingContainer>
    );
  }

  return (
    <TableFundingContainer>
      <TableFundingWrapper
        data={rows}
        columns={columns}
        rowKey="id"
        maxBodyHeight={600}
        scroll={{ x: 2900 }}
        sorting={{ multiple: false }}
      />
    </TableFundingContainer>
  );
}

export default TablePortfolioList;
