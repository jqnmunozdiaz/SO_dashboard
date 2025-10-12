import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function ChartContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start p-0 relative shrink-0 w-[1019px]">
      {children}
    </div>
  );
}

export function ChartWrapper({ children }: ChildrenProps) {
  return (
    <div className="bg-[#ffffff] relative shrink-0 w-full">
      <div className="box-border content-stretch flex flex-col gap-3 items-start justify-start overflow-clip px-0 py-4 relative w-full">
        {children}
      </div>
      <div
        aria-hidden="true"
        className="absolute border-[1px_0px] border-[rgba(0,0,0,0.1)] border-solid inset-0 pointer-events-none"
      />
    </div>
  );
}

export function NoDataMessage({ children }: ChildrenProps) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '280px',
        fontSize: '16px',
        color: '#666',
      }}
    >
      {children}
    </div>
  );
}
