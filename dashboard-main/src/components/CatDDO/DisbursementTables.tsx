import React from 'react';
import { TableDisbursementRegion } from './components/TableDisbursementRegion';
import { TableDisbursementCountry } from './components/TableDisbursementCountry';
import { DisbursementTablesContainer } from './styled/DisbursementTables.styled';

export const DisbursementTables = () => {
  return (
    <DisbursementTablesContainer>
      <TableDisbursementRegion />
      <TableDisbursementCountry />
    </DisbursementTablesContainer>
  );
};

export default DisbursementTables;
