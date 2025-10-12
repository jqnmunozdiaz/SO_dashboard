import type { ReactNode } from 'react';
import { Button } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

export function PriorActionsWrapper({ children }: ChildrenProps) {
  return <div className="flex flex-col gap-6">{children}</div>;
}

export function PriorActionsContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-4 items-start justify-start p-0 relative size-full">
      {children}
    </div>
  );
}

export function PriorActionsTitle({ children }: ChildrenProps) {
  return (
    <div className="flex items-center justify-between mb-4 w-full">
      <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold leading-[0] not-italic relative shrink-0 text-[#295e84] text-[24px] text-left tracking-[-0.18px]">
        <p className="block leading-[24px]">{children}</p>
      </div>
    </div>
  );
}

export function PriorActionsContentWrapper({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col items-start justify-start gap-4 p-0 relative shrink-0 w-full">
      {children}
    </div>
  );
}

export function PriorActionsChartContainer({ children }: ChildrenProps) {
  return (
    <div className="bg-[#ffffff] h-[320px] overflow-visible relative shrink-0 w-full">
      {children}
    </div>
  );
}

export function PriorActionsTableSection({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-row items-start justify-between p-0 relative shrink-0 w-full">
      {children}
    </div>
  );
}

export function DownloadButton({
  children,
  onClick,
  disabled,
}: {
  children: ReactNode;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <Button
      onClick={onClick}
      disabled={disabled}
      className="p-2 hover:bg-gray-100 rounded-md transition-colors duration-200 cursor-pointer bg-transparent border-none"
      title="Download CSV"
    >
      {children}
    </Button>
  );
}

export function PriorActionsFiltersSection({ children }: ChildrenProps) {
  return (
    <div className="flex flex-wrap items-center gap-1 w-full lg:w-auto">
      {children}
    </div>
  );
}

export function PriorActionsSearchInput({ children }: ChildrenProps) {
  return <div className="relative min-w-[200px]">{children}</div>;
}

export function PriorActionsSearchInputWrapper({ children }: ChildrenProps) {
  return <div className="relative flex items-center">{children}</div>;
}

export function PriorActionsStyledSearchInput({
  placeholder,
  value,
  onChange,
}: {
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="w-full p-2 pl-10 border border-gray-300 rounded text-sm outline-none transition-colors focus:border-blue-500 focus:ring-2 focus:ring-blue-200 text-gray-700 placeholder:text-gray-500"
    />
  );
}

export function PriorActionsSearchIcon({ children }: ChildrenProps) {
  return (
    <div className="absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-500">
      {children}
    </div>
  );
}

export function PriorActionsFilterSelect({ children }: ChildrenProps) {
  return <div className="min-w-[150px]">{children}</div>;
}

export function PriorActionsResetButtonContainer({ children }: ChildrenProps) {
  return <div className="flex justify-end mt-2">{children}</div>;
}

export function PriorActionsResetAllButton({
  children,
  onClick,
  disabled,
}: {
  children: ReactNode;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-3 sm:px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 hover:text-red-800 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm sm:text-base"
      title="Reset all filters"
    >
      {children}
    </button>
  );
}
