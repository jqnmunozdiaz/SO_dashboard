import classNames from 'classnames';
import { Button } from 'vizonomy';
import type { ButtonProps } from 'vizonomy';

type StyledButtonProps = ButtonProps & {
  variant?: 'primary' | 'secondary';
  className?: string;
};

export function ResetFiltersButton({ className, ...props }: StyledButtonProps) {
  const buttonClasses = classNames(
    'box-border',
    'content-stretch',
    'flex',
    'flex-row',
    'gap-2.5',
    'items-center',
    'justify-center',
    'overflow-clip',
    'px-6',
    'py-[13px]',
    'relative',
    'w-full',
    'cursor-pointer',
    'bg-transparent',
    'border',
    'border-[#295e84]',
    'border-solid',
    'rounded-[99px]',
    "font-['Inter:Bold',_sans-serif]",
    'font-bold',
    'text-[#295e84]',
    'text-[14px]',
    'tracking-[-0.15px]',
    'hover:bg-[#295e84]',
    'hover:text-white',
    'transition-colors',
    'duration-200',
    className
  );

  return <Button className={buttonClasses} {...props} />;
}

export function UnderstandingDataButton({
  className,
  ...props
}: StyledButtonProps) {
  const buttonClasses = classNames(
    'box-border',
    'content-stretch',
    'flex',
    'flex-row',
    'gap-2.5',
    'items-center',
    'justify-center',
    'overflow-clip',
    'px-6',
    'py-[13px]',
    'relative',
    'rounded-[99px]',
    'shrink-0',
    'w-full',
    'cursor-pointer',
    'bg-[#295e84]',
    "font-['Inter:Bold',_sans-serif]",
    'font-bold',
    'text-[#ffffff]',
    'text-[14px]',
    'tracking-[-0.15px]',
    'hover:bg-[#1e4a6b]',
    'transition-colors',
    'duration-200',
    className
  );

  return <Button className={buttonClasses} {...props} />;
}
