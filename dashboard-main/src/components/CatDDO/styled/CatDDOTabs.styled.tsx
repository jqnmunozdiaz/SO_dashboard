import type { ReactNode } from 'react';
import { Tabs, TabsProps } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

export function TabTextContainer({ children }: ChildrenProps) {
  return (
    <div className="font-['Roboto:Medium',_sans-serif] font-medium leading-[0] relative shrink-0 text-[#295e84] text-[16px] text-left text-nowrap tracking-[0.15px]">
      {children}
    </div>
  );
}

export function TabContentWithIcon({ children }: ChildrenProps) {
  return <div className="flex flex-row gap-[5px] items-center">{children}</div>;
}

export function IconContainer({
  children,
  onClick,
  className,
}: ChildrenProps & {
  onClick?: (e: React.MouseEvent) => void;
  className?: string;
}) {
  return (
    <div
      className={`relative shrink-0 size-5 ${className || ''}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
}

export function TabsWrapper({ children }: ChildrenProps) {
  return (
    <div className="w-full border-t border-gray-200 bg-white">{children}</div>
  );
}

export function TabsInnerContainer({ children }: ChildrenProps) {
  return <div className="max-w-7xl mx-auto px-8 py-4">{children}</div>;
}

export function TabTextParagraph({ children }: ChildrenProps) {
  return (
    <p className="adjustLetterSpacing block leading-[24px] whitespace-pre">
      {children}
    </p>
  );
}

export const TabStyledWrapper = (props: TabsProps) => {
  return (
    <Tabs
      {...props}
      className="w-full [&_[role=tablist]]:flex [&_[role=tablist]]:gap-2 [&_[role=tablist]]:items-center [&_[role=tablist]]:justify-start [&_[role=tablist]]:size-full [&_[role=tab]]:flex [&_[role=tab]]:gap-2.5 [&_[role=tab]]:items-center [&_[role=tab]]:justify-center [&_[role=tab]]:px-4 [&_[role=tab]]:py-2 [&_[role=tab]]:rounded-[99px] [&_[role=tab]:hover]:bg-[#EDEEF0]/70 [&_[role=tab][aria-selected=true]]:bg-[#EDEEF0] [&_[role=tabpanel]]:mt-4"
    />
  );
};
