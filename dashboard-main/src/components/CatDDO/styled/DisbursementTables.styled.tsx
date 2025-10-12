import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function DisbursementTablesContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-6 items-start justify-start p-0 relative size-full">
      {children}
    </div>
  );
}
