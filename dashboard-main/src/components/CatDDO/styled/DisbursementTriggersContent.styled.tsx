import React, { type ReactNode } from 'react';
import { Button, Image } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

export function DisbursementTriggersContainer({ children }: ChildrenProps) {
  return <div className="p-4">{children}</div>;
}

export function DisbursementTriggersTitle({ children }: ChildrenProps) {
  return (
    <div className="flex items-center justify-between mb-4 w-full">
      <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold h-6 leading-[0] not-italic relative shrink-0 text-[#295e84] text-[24px] text-left tracking-[-0.18px] min-w-0">
        <p className="block leading-[24px] whitespace-nowrap">{children}</p>
      </div>
    </div>
  );
}

export function TitleAndFiltersRow({ children }: ChildrenProps) {
  return (
    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-4 w-full">
      {children}
    </div>
  );
}

export function TitleSection({ children }: ChildrenProps) {
  return (
    <div className="flex items-center gap-3 flex-shrink-0">
      <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold text-[#295e84] text-[20px] sm:text-[24px] tracking-[-0.18px] leading-tight">
        DPF Cat DDO Disbursement Triggers Content
      </div>
      {children}
    </div>
  );
}

export function FiltersSection({ children }: ChildrenProps) {
  return (
    <div className="flex flex-wrap items-center gap-1 w-full lg:w-auto">
      {children}
    </div>
  );
}

export function DownloadButtonTrigger({
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

export function FilterSection({ children }: ChildrenProps) {
  return <div className="mb-6">{children}</div>;
}

export function FilterInputContainer({ children }: ChildrenProps) {
  return <div className="w-full">{children}</div>;
}

export function FilterSelectContainerOriginal({ children }: ChildrenProps) {
  return <div className="relative w-full">{children}</div>;
}

export function SelectButton({
  children,
  onClick,
  ...props
}: {
  children: ReactNode;
  onClick: () => void;
} & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="w-full p-2 border border-gray-300 rounded text-left flex justify-between items-center bg-white hover:border-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
      {...props}
    >
      {children}
    </button>
  );
}

export function SelectButtonText({ children }: ChildrenProps) {
  return <span className="truncate">{children}</span>;
}

export function SelectDropdown({ children }: ChildrenProps) {
  return (
    <ul
      className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded shadow-lg max-h-60 overflow-y-auto"
      role="listbox"
      aria-multiselectable="true"
    >
      {children}
    </ul>
  );
}

export function SelectOption({
  children,
  isSelected,
  onClick,
  onKeyDown,
  ...props
}: {
  children: ReactNode;
  isSelected: boolean;
  onClick: () => void;
  onKeyDown: (e: React.KeyboardEvent) => void;
} & React.LiHTMLAttributes<HTMLLIElement>) {
  return (
    <li
      onClick={onClick}
      onKeyDown={onKeyDown}
      className={`p-2 hover:bg-gray-100 cursor-pointer flex items-center ${
        isSelected ? 'bg-blue-100 font-semibold' : ''
      }`}
      role="option"
      aria-selected={isSelected}
      tabIndex={0}
      {...props}
    >
      {children}
    </li>
  );
}

export function OptionCheckbox({ checked }: { checked: boolean }) {
  return <input type="checkbox" checked={checked} readOnly className="mr-2" />;
}

export function FilterResultsInfo({ children }: ChildrenProps) {
  return <div className="mb-4 text-sm text-gray-600">{children}</div>;
}

export function FilterContainer({ children }: ChildrenProps) {
  return <div className="flex flex-col gap-1">{children}</div>;
}

export function FilterResetButton({
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
      className="self-end px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 hover:text-gray-800 rounded transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      title="Reset filter"
    >
      Reset
    </button>
  );
}

export function ResetAllButton({
  children,
  onClick,
  disabled = false,
}: {
  children: ReactNode;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="px-3 sm:px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 hover:text-red-800 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm sm:text-base"
      title="Reset all filters"
    >
      {children}
    </button>
  );
}

// New styled components for search functionality
export function SearchContainer({ children }: ChildrenProps) {
  return (
    <div className="relative w-full" data-search-container>
      {children}
    </div>
  );
}

export function SearchInputWrapper({ children }: ChildrenProps) {
  return (
    <div className="relative flex items-center w-full min-h-[40px] h-auto">
      {children}
    </div>
  );
}

export function SearchIcon({ children }: ChildrenProps) {
  return (
    <div className="absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none flex items-center justify-center z-10">
      {children}
    </div>
  );
}

export function SelectWrapper({ children }: ChildrenProps) {
  return <div className="w-full">{children}</div>;
}

export function DropdownContainer({
  children,
  shouldShowAbove = false,
}: {
  children: ReactNode;
  shouldShowAbove?: boolean;
}) {
  return (
    <div
      className={`absolute z-50 w-full bg-white border border-gray-300 rounded shadow-lg max-h-60 overflow-y-auto ${
        shouldShowAbove ? 'bottom-full mb-1' : 'top-full mt-1'
      }`}
      role="listbox"
      aria-multiselectable="true"
    >
      {children}
    </div>
  );
}

export function DropdownList({ children }: ChildrenProps) {
  return <ul className="py-1">{children}</ul>;
}

export function DropdownItem({
  children,
  isSelected,
  onClick,
  onKeyDown,
  ...props
}: {
  children: ReactNode;
  isSelected: boolean;
  onClick: () => void;
  onKeyDown: (e: React.KeyboardEvent) => void;
} & React.LiHTMLAttributes<HTMLLIElement>) {
  return (
    <li
      onClick={onClick}
      onKeyDown={onKeyDown}
      className={`p-2 hover:bg-gray-100 cursor-pointer flex items-center ${
        isSelected ? 'bg-blue-100 font-semibold' : ''
      }`}
      role="option"
      aria-selected={isSelected}
      tabIndex={0}
      {...props}
    >
      {children}
    </li>
  );
}

export function NoResultsMessage({ children }: ChildrenProps) {
  return (
    <div className="p-3 text-center text-gray-500 text-sm">{children}</div>
  );
}

// New styled components for Figma design
export function TopFilterRow({ children }: ChildrenProps) {
  return (
    <div className="flex items-center justify-start mb-4 space-x-2">
      {children}
    </div>
  );
}

export function SearchInput({ children }: ChildrenProps) {
  return (
    <div className="relative w-[150px] sm:w-[160px] md:w-[180px] flex-shrink-0 h-auto">
      {children}
    </div>
  );
}

export function CountryFilter({ children }: ChildrenProps) {
  return <div className="relative min-w-[120px] max-w-[200px]">{children}</div>;
}

export function MoreFiltersButton({
  children,
  onClick,
  isActive = false,
}: {
  children: ReactNode;
  onClick: () => void;
  isActive?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex gap-2 items-center justify-center px-3 sm:px-4 py-2 rounded-lg border transition-all duration-200 flex-shrink-0 ${
        isActive
          ? 'bg-[#295e84] border-[#295e84] text-white'
          : 'bg-white border-[#295e84] text-[#295e84] hover:bg-[#295e84] hover:text-white'
      }`}
    >
      <div className="flex items-center justify-center">{children}</div>
      <span className="text-sm font-medium whitespace-nowrap">
        More Filters
      </span>
    </button>
  );
}

export function AdditionalFiltersRow({ children }: ChildrenProps) {
  return <div className="flex flex-wrap gap-3 items-start">{children}</div>;
}

export function ResetButtonContainer({ children }: ChildrenProps) {
  return <div className="flex justify-end mt-3">{children}</div>;
}

export function FilterDropdown({ children }: ChildrenProps) {
  return <div className="relative">{children}</div>;
}

export function FilterDropdownButton({ children }: ChildrenProps) {
  return (
    <button
      type="button"
      className="flex gap-2 items-center justify-between px-3 py-2 bg-white border border-gray-200 rounded-lg hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 min-w-[100px] shadow-sm"
    >
      {children}
    </button>
  );
}

export function FilterDropdownText({ children }: ChildrenProps) {
  return (
    <span className="text-sm text-gray-600 font-normal whitespace-nowrap">
      {children}
    </span>
  );
}

export function FilterDropdownIcon({ children }: ChildrenProps) {
  return (
    <div className="w-4 h-4 flex-shrink-0 flex items-center justify-center">
      {children}
    </div>
  );
}

// New Figma-based Country Select Components
export function CountrySelectContainer({ children }: ChildrenProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      {children}
    </div>
  );
}

export function CountrySelectHeader({ children }: ChildrenProps) {
  return (
    <div className="bg-white border-b border-gray-200 px-5 py-4">
      <div className="flex items-center justify-between">{children}</div>
    </div>
  );
}

export function CountrySelectTitle({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Medium',_sans-serif] font-medium text-[#0e121b] text-[14px] leading-[20px] tracking-[-0.084px]">
      {children}
    </div>
  );
}

export function SelectAllButton({ onClick }: { onClick: () => void }) {
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

export function CountrySelectContent({ children }: ChildrenProps) {
  return (
    <div className="bg-white px-5 py-5">
      <div className="flex flex-col gap-4 max-h-60 overflow-y-auto">
        {children}
      </div>
    </div>
  );
}

export function CountryOption({
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
      className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors duration-200"
      onClick={onClick}
    >
      <CountryCheckbox checked={isSelected} />
      <div className="font-['Inter:Regular',_sans-serif] font-normal text-[#0e121b] text-[14px] leading-[20px] tracking-[-0.084px]">
        {children}
      </div>
    </div>
  );
}

export function CountryCheckbox({ checked }: { checked: boolean }) {
  if (checked) {
    return (
      <div className="relative w-5 h-5">
        <Image
          alt="Checked checkbox"
          className="block w-full h-full"
          src="/checkbox-checked.svg"
        />
      </div>
    );
  }

  return (
    <div className="relative w-5 h-5 overflow-hidden">
      <div className="absolute bg-[#e1e4ea] left-1/2 top-1/2 w-4 h-4 rounded-[4px] -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute bg-white left-1/2 top-1/2 w-[13px] h-[13px] rounded-[2.6px] shadow-[0px_2px_2px_0px_rgba(27,28,29,0.12)] -translate-x-1/2 -translate-y-1/2" />
    </div>
  );
}

export function CountrySelectFooter({ children }: ChildrenProps) {
  return (
    <div className="bg-white border-t border-gray-200 px-5 py-4">
      <div className="flex gap-4 items-center justify-start">{children}</div>
    </div>
  );
}

export function ClearButton({
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

export function ApplyButton({
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

export const FilterSelectContainer = React.forwardRef<
  HTMLDivElement,
  ChildrenProps
>(({ children }, ref) => {
  return (
    <div className="relative" ref={ref}>
      {children}
    </div>
  );
});

FilterSelectContainer.displayName = 'FilterSelectContainer';

export function FilterSelectButton({
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

export function FilterSelectContent({ children }: ChildrenProps) {
  return <div className="flex items-center gap-2 min-w-0">{children}</div>;
}

export function FilterSelectText({ children }: ChildrenProps) {
  return <span className="text-left text-gray-600 truncate">{children}</span>;
}

export function FilterSelectIcon({ children }: ChildrenProps) {
  return <div className="w-4 h-4 flex-shrink-0">{children}</div>;
}

export function StyledSearchInput({
  placeholder,
  value,
  onChange,
  ...props
}: {
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="w-full pl-8 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm h-10 leading-10 box-border text-gray-700 placeholder:text-gray-500"
      {...props}
    />
  );
}
