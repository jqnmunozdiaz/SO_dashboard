import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function ChartContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start p-0 relative shrink-0 w-[1058px]">
      {children}
    </div>
  );
}

export function ChartWrapper({ children }: ChildrenProps) {
  return (
    <div className="bg-[#ffffff] h-[385px] overflow-clip relative shadow-[0px_0px_0px_1px_rgba(26,26,26,0.06),0px_1px_1px_-6px_rgba(71,71,71,0.1)] shrink-0 w-full">
      {children}
    </div>
  );
}

export function NoDataMessage() {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '385px',
        fontSize: '16px',
        color: '#666',
      }}
    >
      No data available
    </div>
  );
}
