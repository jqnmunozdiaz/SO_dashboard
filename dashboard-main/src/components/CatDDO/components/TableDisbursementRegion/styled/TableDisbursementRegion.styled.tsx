import type { ReactNode } from 'react';
import { Table, type TableProps, type TableColumn, Button } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

export function TableDisbursementRegionContainer({ children }: ChildrenProps) {
  return <div className="w-full">{children}</div>;
}

export function TableDisbursementRegionWrapper_Container({
  children,
}: ChildrenProps) {
  return <div className="w-full">{children}</div>;
}

export function TableDisbursementRegionTitle({ children }: ChildrenProps) {
  return (
    <div className="flex items-center justify-between mb-4 w-full">
      <div className="font-['Inter:Semi_Bold',_sans-serif] font-semibold h-6 leading-[0] not-italic relative shrink-0 text-[#295e84] text-[24px] text-left tracking-[-0.18px]">
        <p className="block leading-[24px]">{children}</p>
      </div>
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
      } text-[#295e84] text-[14px] ${isTotal ? 'leading-[18px]' : 'leading-[normal]'} tracking-[-0.154px]`}
    >
      {children}
    </span>
  );
}

export interface TableDisbursementRegionWrapperProps<T = unknown> {
  data: T[];
  columns: TableColumn<T>[];
  className?: string;
  maxBodyHeight?: number;
  scroll?: { x?: number | boolean; y?: number };
  sorting?: unknown;
  rowKey?: string;
}

export const TableDisbursementRegionWrapper = <T,>(
  props: TableDisbursementRegionWrapperProps<T>
) => {
  const {
    maxBodyHeight = 360,
    scroll,
    ...rest
  } = props as TableDisbursementRegionWrapperProps<T>;
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
      className="!w-full !min-w-full [&_thead]:bg-[#f2f3f5] [&_th]:text-[#295e84] [&_th]:font-['Inter:Medium',_sans-serif] [&_th]:font-medium [&_th]:text-[14px] [&_th]:leading-[21px] [&_th]:tracking-[-0.154px] [&_th]:px-4 [&_th]:py-3 [&_td]:px-4 [&_td]:py-2 [&_tr:not(:last-child)]:border-b [&_tr:not(:last-child)]:border-[rgba(0,0,0,0.1)] [&_thead_th]:sticky [&_thead_th]:top-0 [&_thead_th]:z-10"
      scroll={mergedScroll}
      onRow={(row: Record<string, unknown>) => ({
        className: (row as { isTotal?: boolean }).isTotal
          ? 'border-t-2 border-gray-300'
          : '',
      })}
    />
  );
};

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
