import React, { type ReactNode } from 'react';
import { Image } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

export const FigmaSelectContainer = React.forwardRef<
  HTMLDivElement,
  ChildrenProps
>(({ children }, ref) => {
  return (
    <div className="relative" ref={ref}>
      {children}
    </div>
  );
});

FigmaSelectContainer.displayName = 'FigmaSelectContainer';

export function FigmaSelectButton({
  children,
  onClick,
}: {
  children: ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex items-center justify-between px-2 py-2 text-sm bg-white border border-gray-200 rounded-lg hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm w-full"
    >
      {children}
    </button>
  );
}

export function FigmaSelectContent({ children }: ChildrenProps) {
  return <div className="flex items-center gap-4 min-w-0">{children}</div>;
}

export function FigmaSelectText({ children }: ChildrenProps) {
  return <span className="text-left text-gray-600 truncate">{children}</span>;
}

export function FigmaSelectIcon({ children }: ChildrenProps) {
  return <div className="w-4 h-4 flex-shrink-0 ml-2">{children}</div>;
}

export function FigmaDropdownContainer({ children }: ChildrenProps) {
  return <div className="absolute z-50 mt-1 w-80">{children}</div>;
}

export function FigmaSelectDropdown({ children }: ChildrenProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      {children}
    </div>
  );
}

export function FigmaSelectHeader({ children }: ChildrenProps) {
  return (
    <div className="bg-white border-b border-gray-200 px-5 py-4">
      <div className="flex items-center justify-between">{children}</div>
    </div>
  );
}

export function FigmaSelectTitle({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Medium',_sans-serif] font-medium text-[#0e121b] text-[14px] leading-[20px] tracking-[-0.084px]">
      {children}
    </div>
  );
}

export function FigmaSelectAllButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="font-['Inter:Medium',_sans-serif] font-medium text-[#525866] text-[14px] leading-[20px] tracking-[-0.084px] underline hover:text-[#295e84] transition-colors duration-200"
    >
      Select All
    </button>
  );
}

export function FigmaSelectOptionsContainer({ children }: ChildrenProps) {
  return (
    <div className="bg-white px-5 py-3">
      <div className="flex flex-col gap-2 max-h-60 overflow-y-auto">
        {children}
      </div>
    </div>
  );
}

export function FigmaSelectOption({
  children,
  isSelected,
  onClick,
}: {
  children: ReactNode;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <div
      className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1.5 rounded transition-colors duration-200"
      onClick={onClick}
    >
      <FigmaSelectCheckbox checked={isSelected} />
      <div className="font-['Inter:Regular',_sans-serif] font-normal text-[#0e121b] text-[14px] leading-[20px] tracking-[-0.084px]">
        {children}
      </div>
    </div>
  );
}

export function FigmaSelectCheckbox({ checked }: { checked: boolean }) {
  if (checked) {
    return (
      <div className="relative w-5 h-5 flex-shrink-0">
        <Image
          alt="Checked checkbox"
          className="block w-full h-full object-contain"
          src="/checkbox-checked.svg"
        />
      </div>
    );
  }

  return (
    <div className="relative w-5 h-5 flex-shrink-0 overflow-hidden">
      <div className="absolute bg-[#e1e4ea] left-1/2 top-1/2 w-4 h-4 rounded-[4px] -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute bg-white left-1/2 top-1/2 w-[13px] h-[13px] rounded-[2.6px] shadow-[0px_2px_2px_0px_rgba(27,28,29,0.12)] -translate-x-1/2 -translate-y-1/2" />
    </div>
  );
}

export function FigmaSelectFooter({ children }: ChildrenProps) {
  return (
    <div className="bg-white border-t border-gray-200 px-5 py-4">
      <div className="flex gap-4 items-center justify-start">{children}</div>
    </div>
  );
}

export function FigmaSelectClearButton({
  onClick,
  disabled = false,
}: {
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="flex-1 bg-white border border-[#e1e4ea] rounded-lg px-4 py-2 font-['Inter:Medium',_sans-serif] font-medium text-[#525866] text-[14px] leading-[20px] tracking-[-0.084px] hover:bg-gray-50 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0px_1px_2px_0px_rgba(10,13,20,0.03)]"
    >
      Clear
    </button>
  );
}

export function FigmaSelectApplyButton({
  onClick,
  disabled = false,
}: {
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="flex-1 bg-[#295e84] rounded-lg px-4 py-2 font-['Inter:Medium',_sans-serif] font-medium text-white text-[14px] leading-[20px] tracking-[-0.084px] hover:bg-[#1e4a6b] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      Apply
    </button>
  );
}

export function FigmaSelectNoOptions({ children }: ChildrenProps) {
  return (
    <div className="p-3 text-center text-gray-500 text-sm">{children}</div>
  );
}
