import { useState, useEffect, useRef } from 'react';
import type { Option } from 'vizonomy-ui';

export interface UseFigmaSelectProps {
  options: Option[];
  selected: Option[];
  onChange: (options: Option[]) => void;
  placeholder: string;
  pluralPlaceholder?: string;
  disabled?: boolean;
}

export function useFigmaSelect({
  options,
  selected,
  onChange,
  placeholder,
  pluralPlaceholder,
  disabled = false,
}: UseFigmaSelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [pendingSelection, setPendingSelection] = useState<Option[]>(
    selected || []
  );
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setPendingSelection(selected || []);
  }, [selected]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
        setPendingSelection(selected || []);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, selected]);

  const handleSelectAll = () => {
    setPendingSelection(options);
  };

  const handleClear = () => {
    setPendingSelection([]);
    onChange([]);
    setIsOpen(false);
  };

  const handleApply = () => {
    onChange(pendingSelection);
    setIsOpen(false);
  };

  const toggleOption = (option: Option) => {
    const isSelected = pendingSelection.some((item) => item.id === option.id);
    if (isSelected) {
      setPendingSelection(
        pendingSelection.filter((item) => item.id !== option.id)
      );
    } else {
      setPendingSelection([...pendingSelection, option]);
    }
  };

  const isSelected = (option: Option) => {
    return pendingSelection.some((item) => item.id === option.id);
  };

  const getDisplayValue = () => {
    if (!selected?.length) {
      return placeholder;
    }
    const SHOW_ONE_SELECTED = 1;
    if (selected.length === SHOW_ONE_SELECTED) {
      return selected[0].label;
    }

    const pluralText = pluralPlaceholder ?? placeholder.toLowerCase();
    return `${selected.length} ${pluralText} selected`;
  };

  const handleToggleDropdown = () => {
    if (!disabled) {
      setIsOpen(!isOpen);
    }
  };

  return {
    isOpen,
    pendingSelection,
    dropdownRef,
    handleSelectAll,
    handleClear,
    handleApply,
    toggleOption,
    isSelected,
    getDisplayValue,
    handleToggleDropdown,
  };
}
