import type { ReactNode } from 'react';

interface LoadingPlaceholderProps {
  children: ReactNode;
  width?: number | string;
  height?: number | string;
}

export function LoadingPlaceholder({
  children,
  width,
  height,
}: LoadingPlaceholderProps) {
  const widthStyle = typeof width === 'number' ? `${width}px` : width || '100%';
  const heightStyle =
    typeof height === 'number' ? `${height}px` : height || '385px';

  return (
    <div
      className="flex items-center justify-center border border-gray-200 rounded-lg bg-gray-50 text-gray-500 text-sm"
      style={{
        width: widthStyle,
        height: heightStyle,
      }}
    >
      {children}
    </div>
  );
}
