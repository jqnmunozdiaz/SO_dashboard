import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function GlobalWrapper({ children }: ChildrenProps) {
  return <div className="flex flex-col gap-6">{children}</div>;
}

export function GlobalContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start p-0 relative size-full">
      {children}
    </div>
  );
}

export function GlobalTitle({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold leading-[0] min-w-full not-italic relative shrink-0 text-[#295e84] text-[24px] text-left tracking-[-0.18px]">
      <p className="block leading-[24px]">{children}</p>
    </div>
  );
}

export function GlobalContentWrapper({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col items-start justify-start gap-4 p-0 relative shrink-0 w-full">
      {children}
    </div>
  );
}

export function GlobalBulletPointsContainer({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Regular',_sans-serif] font-normal leading-[0] min-w-full not-italic relative shrink-0 text-[#295e84] text-[14px] text-left">
      <ul className="list-disc space-y-2">{children}</ul>
    </div>
  );
}

export function GlobalBulletPoint({ children }: ChildrenProps) {
  return (
    <li className="leading-[24px] mb-0 ms-[21px]">
      <span className="block">{children}</span>
    </li>
  );
}

export function GlobalSubBulletPointsContainer({ children }: ChildrenProps) {
  return <ul className="list-disc space-y-2">{children}</ul>;
}

export function GlobalSubBulletPoint({ children }: ChildrenProps) {
  return (
    <li className="mb-0 ms-[42px]">
      <span className="leading-[24px]">{children}</span>
    </li>
  );
}
