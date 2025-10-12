'use client';

import React from 'react';
import { BarChart } from '@/lib/BarChart';
import {
  ChartContainer,
  ChartHeader,
  ChartTitle,
  ChartWrapper,
} from './styled/DisbursementChart.styled';
import { useDisbursementChart } from './useDisbursementChart';
import { formatTotalLabel, formatValueLabel } from './DisbursementChart.utils';
import { ClientOnlyChart } from '../ChartWrapper';
import Tooltip from '../Tooltip';

export function DisbursementChart() {
  const { data, series } = useDisbursementChart();

  return (
    <ChartContainer>
      <ChartHeader>
        <ChartTitle>
          DPF Cat DDO disbursements (in million US$) per funding source
        </ChartTitle>
      </ChartHeader>
      <ChartWrapper>
        <ClientOnlyChart width={1040} height={385}>
          <BarChart
            data={data}
            series={series}
            width={1040}
            height={385}
            xAxisLabel="Fiscal Year"
            yAxisLabel="Disbursement Amount"
            orientation="vertical"
            showTotals
            showLegend
            showGrid
            yAxisLabelOffset={45}
            barPadding={0.3}
            legendItemGap={10}
            margin={{ top: 20, right: 20, bottom: 80, left: 80 }}
            formatTotalLabel={formatTotalLabel}
            formatValueLabel={formatValueLabel}
            styleProps={{
              barOutlineStyle: '2px solid #002f54',
            }}
            onOpenTooltip={(dataPoint, seriesKey) => {
              const seriesInfo = series.find((s) => s.key === seriesKey);
              const value = dataPoint.values[seriesKey] ?? 0;
              return (
                <Tooltip
                  content={`${seriesInfo?.label} (${dataPoint.label}): ${formatValueLabel(value)}`}
                />
              );
            }}
          />
        </ClientOnlyChart>
      </ChartWrapper>
    </ChartContainer>
  );
}

export default DisbursementChart;
