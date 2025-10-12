'use client';

import React from 'react';
import {
  ChartContainer,
  ChartWrapper,
  ChartTitle,
  NoDataMessage,
} from './styled';
import { useMixedDPOChart } from './useMixedDPOChart';
import { ClientOnlyChart } from '../../../ChartWrapper';
import { BAR_HEIGHT, CHART_PADDING } from './constants/mixedDPOChartData';
import { BarChart } from '@/lib/BarChart';
import Tooltip from '../../../Tooltip';

export function MixedDPOChart() {
  const { data, series } = useMixedDPOChart();

  const chartHeight = data.length * BAR_HEIGHT + CHART_PADDING;

  if (!data?.length) {
    return (
      <ChartContainer>
        <ChartTitle>Mixed DPOs</ChartTitle>
        <ChartWrapper>
          <NoDataMessage>No data available</NoDataMessage>
        </ChartWrapper>
      </ChartContainer>
    );
  }

  return (
    <ChartContainer>
      <ChartTitle>Mixed DPOs</ChartTitle>
      <ChartWrapper>
        <ClientOnlyChart width={493} height={chartHeight}>
          <BarChart
            data={data}
            series={series}
            width={493}
            height={chartHeight}
            xAxisLabel="Climate co-benefits %"
            yAxisLabel=""
            orientation="horizontal"
            showLegend={false}
            showGrid={false}
            showTooltip={true}
            barPadding={0.3}
            margin={{ top: 20, right: 20, bottom: 40, left: 200 }}
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

export default MixedDPOChart;
