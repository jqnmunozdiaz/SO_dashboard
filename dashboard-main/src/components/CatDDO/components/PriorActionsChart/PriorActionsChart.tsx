'use client';

import React from 'react';
import { BarChart } from '@/lib/BarChart';
import {
  ChartContainer,
  ChartWrapper,
  NoDataMessage,
} from './styled/PriorActionsChart.styled';
import { usePriorActionsChart } from './usePriorActionsChart';
import { ClientOnlyChart } from '../ChartWrapper';
import Tooltip from '../Tooltip';
import type { PriorAction } from '@/components/CatDDO/interfaces/PriorAction';

interface PriorActionsChartProps {
  filteredRows?: PriorAction[];
}

export function PriorActionsChart({ filteredRows }: PriorActionsChartProps) {
  const { data, series } = usePriorActionsChart(filteredRows);

  if (!data.length) {
    return (
      <ChartContainer>
        <ChartWrapper>
          <NoDataMessage>No data available</NoDataMessage>
        </ChartWrapper>
      </ChartContainer>
    );
  }

  return (
    <ChartContainer>
      <ChartWrapper>
        <ClientOnlyChart width={1019} height={280}>
          <BarChart
            data={data}
            series={series}
            width={1019}
            height={280}
            xAxisLabel=""
            yAxisLabel=""
            orientation="horizontal"
            showLegend={false}
            showGrid={true}
            showTooltip={false}
            legendItemGap={10}
            yAxisLabelOffset={10}
            barPadding={0.4}
            yAxisLabelMaxWidth={150}
            yAxisLabelShowPopup={true}
            margin={{ top: 20, right: 20, bottom: 60, left: 200 }}
            styleProps={{
              barOutlineStyle: '2px solid #002f54',
            }}
            onOpenTooltip={(dataPoint, seriesKey) => {
              const value = dataPoint.values[seriesKey] ?? 0;
              return <Tooltip content={`${dataPoint.label}: ${value}`} />;
            }}
          />
        </ClientOnlyChart>
      </ChartWrapper>
    </ChartContainer>
  );
}

export default PriorActionsChart;
