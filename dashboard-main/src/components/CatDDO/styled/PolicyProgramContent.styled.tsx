import type { ReactNode } from 'react';
import classNames from 'classnames';

interface ChildrenProps {
  children: ReactNode;
}

export function PolicyProgramContainer({ children }: ChildrenProps) {
  return <div className="p-4">{children}</div>;
}

export function PolicyProgramTitle({ children }: ChildrenProps) {
  return (
    <h3 className="text-[32px] font-bold !text-[#295e84] leading-[40px] mb-4">
      {children}
    </h3>
  );
}

export function ContentContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames('space-y-6 mb-12', className);

  return <div className={containerClasses}>{children}</div>;
}

export function DescriptionContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames('space-y-4', className);

  return <div className={containerClasses}>{children}</div>;
}

export function DescriptionText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const textClasses = classNames(
    'text-[14px] text-[#295e84] leading-[21px] tracking-[-0.15px]',
    'w-full',
    className
  );

  return <div className={textClasses}>{children}</div>;
}

export function LinkText({
  children,
  className,
  href,
}: ChildrenProps & { className?: string; href?: string }) {
  const linkClasses = classNames(
    'text-[#26a0f8] underline decoration-solid underline-offset-1',
    'cursor-pointer hover:text-[#1e7bb8] transition-colors duration-200',
    className
  );

  if (href) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className={linkClasses}
      >
        {children}
      </a>
    );
  }

  return <span className={linkClasses}>{children}</span>;
}

export function DiagramContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames(
    'border border-[rgba(41,94,132,0.1)] rounded-lg p-1',
    'w-full overflow-x-auto',
    className
  );

  return <div className={containerClasses}>{children}</div>;
}

export function PillarsRow({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const rowClasses = classNames(
    'flex flex-nowrap gap-2 justify-center',
    'min-w-full',
    className
  );

  return <div className={rowClasses}>{children}</div>;
}

export function PillarColumn({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const columnClasses = classNames(
    'flex flex-col gap-1 flex-shrink-0',
    className
  );

  return <div className={columnClasses}>{children}</div>;
}

export function PillarBox({
  children,
  backgroundColor,
  className,
}: ChildrenProps & {
  backgroundColor: string;
  className?: string;
}) {
  const boxClasses = classNames(
    'h-[50px] w-[130px] rounded-lg flex items-center justify-center p-1',
    className
  );

  return (
    <div className={boxClasses} style={{ backgroundColor }}>
      {children}
    </div>
  );
}

export function SubPillarBox({
  children,
  backgroundColor,
  className,
}: ChildrenProps & {
  backgroundColor: string;
  className?: string;
}) {
  const boxClasses = classNames(
    'w-[130px] rounded-lg flex items-center justify-center p-1',
    className
  );

  return (
    <div className={boxClasses} style={{ backgroundColor }}>
      {children}
    </div>
  );
}

export function PillarText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const textClasses = classNames(
    'text-[10px] font-semibold text-[#295e84] text-center leading-[14px] tracking-[-0.15px]',
    'w-full max-w-[120px]',
    'break-words',
    className
  );

  return <div className={textClasses}>{children}</div>;
}

export function SubPillarText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const textClasses = classNames(
    'text-[10px] text-[#295e84] text-center leading-[14px] tracking-[-0.15px]',
    'w-full max-w-[120px]',
    'break-words',
    className
  );

  return <div className={textClasses}>{children}</div>;
}
