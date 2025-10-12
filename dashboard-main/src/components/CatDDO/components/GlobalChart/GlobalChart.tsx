'use client';

import React from 'react';
import { BarChart } from '@/lib/BarChart';
import {
  ChartContainer,
  ChartWrapper,
  NoDataMessage,
} from './styled/GlobalChart.styled';
import { useGlobalChart } from './useGlobalChart';
import { ClientOnlyChart } from '../ChartWrapper';
import Tooltip from '../Tooltip';

export function GlobalChart() {
  const { data, series } = useGlobalChart();

  if (!data.length) {
    return (
      <ChartContainer>
        <ChartWrapper>
          <NoDataMessage />
        </ChartWrapper>
      </ChartContainer>
    );
  }

  return (
    <ChartContainer>
      <ChartWrapper>
        <ClientOnlyChart width={1058} height={385}>
          <BarChart
            data={data}
            series={series}
            width={1058}
            height={385}
            xAxisLabel="Fiscal Year"
            yAxisLabel="Number of DPF Cat DDOs"
            orientation="vertical"
            showLegend
            showGrid
            showTooltip
            legendItemGap={10}
            yAxisLabelOffset={10}
            barPadding={0.3}
            showIntegersOnly
            margin={{ top: 20, right: 20, bottom: 80, left: 60 }}
            styleProps={{
              barOutlineStyle: '2px solid #002f54',
            }}
            onOpenTooltip={(dataPoint, seriesKey) => {
              const seriesInfo = series.find((s) => s.key === seriesKey);
              const value = dataPoint.values[seriesKey] ?? 0;
              return (
                <Tooltip
                  content={`${seriesInfo?.label} (${dataPoint.label}): ${value}`}
                />
              );
            }}
          />
        </ClientOnlyChart>
      </ChartWrapper>
    </ChartContainer>
  );
}

export default GlobalChart;
