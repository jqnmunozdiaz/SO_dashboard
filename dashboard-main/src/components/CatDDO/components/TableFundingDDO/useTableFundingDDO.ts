import { useMemo } from 'react';
import type { FundingSource } from '../../interfaces';
import { useFetchSummaryTable } from '@/hooks/useFetchSummaryTable';

export const useTableFundingDDO = () => {
  const { data, isLoading, errorMessage } = useFetchSummaryTable();

  const rows = useMemo<FundingSource[]>(() => {
    if (!data) return [];
    const format = (n: number) =>
      n.toLocaleString('en-US', { maximumFractionDigits: 1 });
    const makeRow = (
      id: string,
      source: string,
      ibrd: number,
      ida: number
    ) => ({
      id,
      source,
      ibrd: format(ibrd),
      ida: format(ida),
      total: format(Number((ibrd + ida).toFixed(1))),
    });

    const disbursed = makeRow(
      '1',
      'Disbursed',
      data.table.IBRD.Disbursed,
      data.table.IDA.Disbursed
    );
    const undisbursed = makeRow(
      '2',
      'Undisbursed',
      data.table.IBRD.Undisbursed,
      data.table.IDA.Undisbursed
    );
    const pipeline = makeRow(
      '3',
      'Pipeline',
      data.table.IBRD.Pipeline,
      data.table.IDA.Pipeline
    );
    const total: FundingSource = {
      id: '4',
      source: 'Total',
      ibrd: format(
        data.table.IBRD.Disbursed +
          data.table.IBRD.Undisbursed +
          data.table.IBRD.Pipeline
      ),
      ida: format(
        data.table.IDA.Disbursed +
          data.table.IDA.Undisbursed +
          data.table.IDA.Pipeline
      ),
      total: format(
        Number(
          (
            data.Total.Disbursed +
            data.Total.Undisbursed +
            data.Total.Pipeline
          ).toFixed(1)
        )
      ),
      isTotal: true,
    };

    return [disbursed, undisbursed, pipeline, total];
  }, [data]);

  return { rows, isLoading, errorMessage };
};
