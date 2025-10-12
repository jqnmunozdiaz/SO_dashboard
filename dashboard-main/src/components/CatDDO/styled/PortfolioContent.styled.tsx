import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function PortfolioContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start leading-[0] not-italic p-0 relative size-full text-[#295e84] text-left">
      {children}
    </div>
  );
}

export function PortfolioTitle({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold relative shrink-0 text-[24px] tracking-[-0.18px] w-full">
      <p className="block leading-[24px]">{children}</p>
    </div>
  );
}

export function PortfolioDescription({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Regular',_sans-serif] font-normal relative shrink-0 text-[14px] w-full">
      <p className="block leading-[24px]">{children}</p>
    </div>
  );
}

export function ChartsContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-row gap-6 items-start justify-start p-0 relative size-full">
      {children}
    </div>
  );
}

export function PortfolioWrapper({ children }: ChildrenProps) {
  return <div className="flex flex-col gap-6">{children}</div>;
}
