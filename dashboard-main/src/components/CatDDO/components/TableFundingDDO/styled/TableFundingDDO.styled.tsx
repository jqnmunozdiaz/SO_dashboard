import type { ReactNode } from 'react';
import { Table, type TableProps, type TableColumn, Image } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

interface SortIconProps {
  direction?: 'asc' | 'desc' | null;
}

export function SortIcon({ direction }: SortIconProps) {
  const getIconSrc = () => {
    switch (direction) {
      case 'asc':
        return '/chevron.svg';
      case 'desc':
        return '/chevron.svg';
      default:
        return '/chevron-up-down.svg';
    }
  };

  const getRotation = () => {
    switch (direction) {
      case 'asc':
        return 'rotate-180';
      case 'desc':
        return 'rotate-0';
      default:
        return 'rotate-0';
    }
  };

  return (
    <Image
      src={getIconSrc()}
      alt={`Sort ${direction || 'neutral'}`}
      className={`w-3 h-3 transition-transform duration-200 ${getRotation()}`}
    />
  );
}

export function TableFundingContainer({ children }: ChildrenProps) {
  return (
    <div className="box-border content-stretch flex flex-col gap-2 items-start justify-start p-0 relative w-full min-w-0 overflow-x-auto">
      {children}
    </div>
  );
}

export function TableFundingNote({ children }: ChildrenProps) {
  return (
    <div className="font-['Inter:Italic',_sans-serif] font-normal italic leading-[0] relative shrink-0 text-[#295e84] text-[12px] text-left text-nowrap">
      <p className="block leading-[18px] whitespace-pre">{children}</p>
    </div>
  );
}

interface TableCellTextProps extends ChildrenProps {
  isTotal?: boolean;
}

export function TableCellText({
  children,
  isTotal = false,
}: TableCellTextProps) {
  return (
    <span
      className={`font-['Inter:${isTotal ? 'Semi_Bold' : 'Regular'}',_sans-serif] ${
        isTotal ? 'font-semibold' : 'font-normal'
      } text-[#295e84] text-[14px] ${isTotal ? 'leading-[18px]' : 'leading-normal'} tracking-[-0.154px]`}
    >
      {children}
    </span>
  );
}

export interface TableFundingWrapperProps<T = unknown> {
  data: T[];
  columns: TableColumn<T>[];
  className?: string;
  maxBodyHeight?: number;
  scroll?: { x?: number | boolean; y?: number };
  sorting?: unknown;
  rowKey?: string;
}

export const TableFundingWrapper = <T,>(props: TableFundingWrapperProps<T>) => {
  const {
    maxBodyHeight = 360,
    scroll,
    ...rest
  } = props as TableFundingWrapperProps<T>;
  const incoming = rest as unknown as TableProps & {
    scroll?: { x?: number | boolean; y?: number };
  };
  const mergedScroll = {
    ...(incoming.scroll ?? {}),
    ...(scroll ?? {}),
    y: maxBodyHeight,
  };
  return (
    <Table
      {...incoming}
      bordered
      size="small"
      renderSortIcon={(direction: string) => (
        <SortIcon direction={direction as 'asc' | 'desc' | null} />
      )}
      className="w-full [&_thead]:bg-[#f2f3f5] [&_th]:text-[#295e84] [&_th]:font-['Inter:Medium',_sans-serif] [&_th]:font-medium [&_th]:text-[14px] [&_th]:leading-[21px] [&_th]:tracking-[-0.154px] [&_th]:px-4 [&_th]:py-3 [&_td]:px-4 [&_td]:py-3 [&_tr]:border-b [&_tr]:border-[rgba(0,0,0,0.1)] [&_thead_th]:sticky [&_thead_th]:top-0 [&_thead_th]:z-10"
      scroll={mergedScroll}
      onRow={(row: Record<string, unknown>) => ({
        className: (row as { isTotal?: boolean }).isTotal
          ? 'border-t-2 border-gray-300'
          : '',
      })}
    />
  );
};
