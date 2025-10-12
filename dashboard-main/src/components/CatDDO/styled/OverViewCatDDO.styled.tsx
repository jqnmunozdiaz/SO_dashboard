import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function OverViewContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start p-0 relative size-full">
      {children}
    </div>
  );
}

export function OverViewTitle({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold leading-[0] not-italic relative shrink-0 text-[#295e84] text-[18px] text-left tracking-[-0.18px] w-full">
      <p className="block leading-[24px]">{children}</p>
    </div>
  );
}

export function ContentWrapper({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-row items-start justify-start gap-6 p-0 relative shrink-0 w-full">
      {children}
    </div>
  );
}

export function BulletPointsContainer({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Regular',_sans-serif] font-normal leading-[0] not-italic relative shrink-0 text-[#295e84] text-[14px] text-left w-[619px] ml-6">
      <ul className="list-disc space-y-2">{children}</ul>
    </div>
  );
}

export function BulletPoint({ children }: ChildrenProps) {
  return (
    <li className="leading-[24px] mb-2 ms-[21px]">
      <span className="block">{children}</span>
    </li>
  );
}

export function OverViewWrapper({ children }: ChildrenProps) {
  return <div className="flex flex-col gap-6">{children}</div>;
}

export function SemiboldText({ children }: ChildrenProps) {
  return <span className="font-semibold">{children}</span>;
}
