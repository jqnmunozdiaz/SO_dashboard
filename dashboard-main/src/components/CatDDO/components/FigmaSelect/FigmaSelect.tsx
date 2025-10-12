import React from 'react';
import { Image, When } from 'vizonomy';
import type { Option } from 'vizonomy-ui';
import { useFigmaSelect } from './useFigmaSelect';
import {
  FigmaSelectContainer,
  FigmaSelectButton,
  FigmaSelectContent,
  FigmaSelectText,
  FigmaSelectIcon,
  FigmaDropdownContainer,
  FigmaSelectDropdown,
  FigmaSelectHeader,
  FigmaSelectTitle,
  FigmaSelectAllButton,
  FigmaSelectOptionsContainer,
  FigmaSelectOption,
  FigmaSelectFooter,
  FigmaSelectClearButton,
  FigmaSelectApplyButton,
  FigmaSelectNoOptions,
} from './FigmaSelect.styled';

export interface FigmaSelectProps {
  options: Option[];
  selected: Option[];
  onChange: (options: Option[]) => void;
  placeholder: string;
  pluralPlaceholder?: string;
  disabled?: boolean;
}

export const FigmaSelect: React.FC<FigmaSelectProps> = ({
  options,
  selected,
  onChange,
  placeholder,
  pluralPlaceholder,
  disabled = false,
}) => {
  const {
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
  } = useFigmaSelect({
    options,
    selected,
    onChange,
    placeholder,
    pluralPlaceholder,
    disabled,
  });

  return (
    <FigmaSelectContainer ref={dropdownRef}>
      <FigmaSelectButton onClick={handleToggleDropdown}>
        <FigmaSelectContent>
          <When condition={placeholder === 'Country'}>
            <FigmaSelectIcon>
              <Image
                alt="Globe"
                className="w-4 h-4 flex-shrink-0"
                src="/globe.svg"
              />
            </FigmaSelectIcon>
          </When>
          <FigmaSelectText>{getDisplayValue()}</FigmaSelectText>
        </FigmaSelectContent>
        <FigmaSelectIcon>
          <Image
            alt="Arrow Down"
            className="w-4 h-4 flex-shrink-0"
            src="/chevron.svg"
          />
        </FigmaSelectIcon>
      </FigmaSelectButton>

      <When condition={isOpen}>
        <FigmaDropdownContainer>
          <FigmaSelectDropdown>
            <FigmaSelectHeader>
              <FigmaSelectTitle>{placeholder}</FigmaSelectTitle>
              <FigmaSelectAllButton onClick={handleSelectAll} />
            </FigmaSelectHeader>

            <FigmaSelectOptionsContainer>
              <When condition={!!options?.length}>
                {options.map((option) => (
                  <FigmaSelectOption
                    key={option.id}
                    isSelected={isSelected(option)}
                    onClick={() => toggleOption(option)}
                  >
                    {option.label}
                  </FigmaSelectOption>
                ))}
              </When>
              <When condition={!options?.length}>
                <FigmaSelectNoOptions>
                  No options available
                </FigmaSelectNoOptions>
              </When>
            </FigmaSelectOptionsContainer>

            <FigmaSelectFooter>
              <FigmaSelectClearButton
                onClick={handleClear}
                disabled={!pendingSelection?.length}
              />
              <FigmaSelectApplyButton
                onClick={handleApply}
                disabled={!pendingSelection?.length}
              />
            </FigmaSelectFooter>
          </FigmaSelectDropdown>
        </FigmaDropdownContainer>
      </When>
    </FigmaSelectContainer>
  );
};
