'use client';

import dynamic from 'next/dynamic';
import React from 'react';
import { LoadingPlaceholder } from './styled/ChartWrapper.styled';

interface ChartWrapperProps {
  children: React.ReactNode;
  width?: number | string;
  height?: number | string;
  loadingText?: string;
}

interface LoadingPlaceholderProps {
  width?: number | string;
  height?: number | string;
  loadingText?: string;
}

const LoadingPlaceholderComponent: React.FC<LoadingPlaceholderProps> = ({
  width = '100%',
  height = '385px',
  loadingText = 'Loading chart...',
}) => (
  <LoadingPlaceholder width={width} height={height}>
    {loadingText}
  </LoadingPlaceholder>
);

export const withChartWrapper = <P extends object>(
  WrappedComponent: React.ComponentType<P>,
  defaultWidth?: number | string,
  defaultHeight?: number | string
) => {
  const ChartWithWrapper = dynamic(
    () => Promise.resolve({ default: WrappedComponent }),
    {
      ssr: false,
      loading: () => (
        <LoadingPlaceholderComponent
          width={defaultWidth}
          height={defaultHeight}
        />
      ),
    }
  );

  ChartWithWrapper.displayName = `withChartWrapper(${WrappedComponent.displayName || WrappedComponent.name})`;

  return ChartWithWrapper;
};

export const ClientOnlyChart: React.FC<ChartWrapperProps> = ({
  children,
  width,
  height,
  loadingText,
}) => {
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <LoadingPlaceholderComponent
        width={width}
        height={height}
        loadingText={loadingText}
      />
    );
  }

  return <>{children}</>;
};

export default ClientOnlyChart;
