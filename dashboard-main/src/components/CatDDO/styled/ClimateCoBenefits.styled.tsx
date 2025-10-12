import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function ClimateWrapper({ children }: ChildrenProps) {
  return <div className="flex flex-col gap-8">{children}</div>;
}

export function ClimateContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-8 items-start justify-start p-0 relative size-full">
      {children}
    </div>
  );
}

export function ClimateTitle({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start leading-[0] not-italic p-0 relative shrink-0 text-[#295e84] text-left w-[987px]">
      <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold relative shrink-0 text-[24px] tracking-[-0.18px] w-full">
        <p className="block leading-[24px]">{children}</p>
      </div>
    </div>
  );
}

export function ClimateContentWrapper({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col items-start justify-start gap-8 p-0 relative shrink-0 w-full">
      {children}
    </div>
  );
}

export function ClimateBulletPointsContainer({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Regular',_sans-serif] font-normal leading-[0] min-w-full not-italic relative shrink-0 text-[#295e84] text-[14px] text-left">
      <ul className="css-ed5n1g">{children}</ul>
    </div>
  );
}

export function ClimateBulletPoint({ children }: ChildrenProps) {
  return (
    <li className="list-disc mb-0 ms-[21px]">
      <span className="leading-[24px]">{children}</span>
    </li>
  );
}

export function ClimateSubBulletPointsContainer({ children }: ChildrenProps) {
  return <ul className="css-ed5n1g list-disc">{children}</ul>;
}

export function ClimateSubBulletPoint({ children }: ChildrenProps) {
  return (
    <li className="mb-0 ms-[42px]">
      <span className="leading-[24px]">{children}</span>
    </li>
  );
}

export function ClimateChartsContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-row gap-8 items-start justify-start p-0 relative shrink-0">
      {children}
    </div>
  );
}
