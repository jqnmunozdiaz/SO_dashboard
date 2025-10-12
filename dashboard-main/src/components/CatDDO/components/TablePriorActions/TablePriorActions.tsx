import React from 'react';
import type { TableColumn } from 'vizonomy';
import type { PriorAction } from '../../interfaces';
import {
  TablePriorActionsContainer,
  TablePriorActionsWrapper_Container,
  TableCellText,
  TablePriorActionsWrapper,
  NoDataMessage,
} from './styled/TablePriorActions.styled';

interface TablePriorActionsProps {
  rows?: PriorAction[];
  isLoading?: boolean;
}

export const TablePriorActions = ({
  rows = [],
  isLoading = false,
}: TablePriorActionsProps) => {
  const columns: TableColumn<PriorAction>[] = [
    {
      id: 'projectNumber',
      key: 'projectNumber',
      label: 'P#',
      width: '10%',
      render: (value: string, row: PriorAction) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'country',
      key: 'country',
      label: 'Country',
      width: '15%',
      render: (value: string, row: PriorAction) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'drmPillar',
      key: 'drmPillar',
      label: 'DRM Pillar',
      width: '20%',
      render: (value: string, row: PriorAction) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'priorAction',
      key: 'priorAction',
      label: 'Prior Action',
      width: '27.5%',
      render: (value: string, row: PriorAction) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
    {
      id: 'resultIndicator',
      key: 'resultIndicator',
      label: 'Result Indicator',
      width: '27.5%',
      render: (value: string, row: PriorAction) => (
        <TableCellText isTotal={row.isTotal}>{value}</TableCellText>
      ),
    },
  ];

  if (isLoading) {
    return (
      <TablePriorActionsContainer>
        <TablePriorActionsWrapper_Container>
          <NoDataMessage>Loading table data...</NoDataMessage>
        </TablePriorActionsWrapper_Container>
      </TablePriorActionsContainer>
    );
  }

  if (!rows?.length) {
    return (
      <TablePriorActionsContainer>
        <TablePriorActionsWrapper_Container>
          <NoDataMessage>No data available</NoDataMessage>
        </TablePriorActionsWrapper_Container>
      </TablePriorActionsContainer>
    );
  }

  return (
    <TablePriorActionsContainer>
      <TablePriorActionsWrapper_Container>
        <TablePriorActionsWrapper data={rows} columns={columns} rowKey="id" />
      </TablePriorActionsWrapper_Container>
    </TablePriorActionsContainer>
  );
};

export default TablePriorActions;
