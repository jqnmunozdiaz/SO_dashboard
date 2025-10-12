// DRM Policy Pillars Modal Styled Components
import type { ReactNode } from 'react';
import classNames from 'classnames';

interface ChildrenProps {
  children: ReactNode;
}

export function ContentContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames('space-y-6', className);

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
    'max-w-none lg:max-w-4xl',
    className
  );

  return <div className={textClasses}>{children}</div>;
}

export function LinkText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const linkClasses = classNames(
    'text-[#26a0f8] underline decoration-solid underline-offset-1',
    className
  );

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
    'flex flex-nowrap gap-2 justify-start',
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

export function ButtonContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames('flex justify-start', className);

  return <div className={containerClasses}>{children}</div>;
}

export function ModalOverlay({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const overlayClasses = classNames('z-[9999]', className);

  return <div className={overlayClasses}>{children}</div>;
}

export function ModalContent({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const contentClasses = classNames(
    '!w-[900px] max-w-[900px] max-h-[90vh] overflow-y-auto z-[10000]',
    className
  );

  return <div className={contentClasses}>{children}</div>;
}

export function ModalTitle({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const titleClasses = classNames(
    'text-[32px] font-bold text-[#1e4a6b] leading-[40px]',
    className
  );

  return <div className={titleClasses}>{children}</div>;
}

export function ModalBody({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const bodyClasses = classNames('px-8 py-[41px]', className);

  return <div className={bodyClasses}>{children}</div>;
}

export function ModalButton({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const buttonClasses = classNames(
    'bg-[#295e84] text-white px-6 py-[13px] rounded-[99px] font-bold text-[14px] leading-[20px] tracking-[-0.15px] hover:bg-[#1e4a6b] transition-colors',
    className
  );

  return <div className={buttonClasses}>{children}</div>;
}
