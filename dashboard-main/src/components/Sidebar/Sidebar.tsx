'use client';

import { When } from 'vizonomy';
import type { SidebarProps } from './Sidebar.d';
import { useSidebar } from './useSidebar';
import {
  SIDEBAR_LOGO_IMAGE,
  FILTER_ICON_GROUP,
  FILTER_ICON_IMAGE,
} from './Sidebar.constants';
import {
  SidebarContainer,
  SidebarContent,
  LogoContainer,
  LogoImage,
  FilterSectionContainer,
  FilterSectionHeader,
  FilterSectionTitle,
  FilterIconContainer,
  FilterIconWrapper,
  FilterIcon,
  FilterOptionsContainer,
  FilterOptionButton,
  FilterOptionLabel,
  FilterOptionText,
  ActionButtonsContainer,
  ButtonContainer,
  SidebarBorder,
  LoadingMessage,
  ErrorMessage,
} from './Sidebar.styled';
import { ResetFiltersButton, UnderstandingDataButton } from './SidebarButtons';
import DRMPolicyPillarsModal from '../DRMPolicyPillarsModal';
import Collapse, {
  CollapseTrigger,
  CollapseContent,
  CollapseContainer,
} from '../../lib/Collapse';

function Sidebar({ className }: SidebarProps) {
  const {
    filterSections,
    isLoading,
    error,
    handleFilterToggle,
    handleResetFilters,
    handleUnderstandingData,
    isDRMModalOpen,
    handleCloseDRMModal,
  } = useSidebar();

  return (
    <SidebarContainer className={className}>
      <SidebarContent>
        <LogoContainer>
          <LogoImage src={SIDEBAR_LOGO_IMAGE} />
        </LogoContainer>

        <When condition={isLoading}>
          <LoadingMessage>Loading filters...</LoadingMessage>
        </When>

        <When condition={!!error}>
          <ErrorMessage>Error loading filters: {error}</ErrorMessage>
        </When>

        <When condition={!isLoading && !error}>
          {filterSections.map((section) => {
            let sectionSize: 'small' | 'default' | 'large' = 'default';

            if (section.id === 'project-status') {
              sectionSize = 'small';
            } else if (section.id === 'pillar') {
              sectionSize = 'large';
            } else {
              sectionSize = 'default';
            }

            return (
              <FilterSectionContainer key={section.id} size={sectionSize}>
                <Collapse defaultOpen={true} animated={true} duration={300}>
                  {() => (
                    <CollapseContainer>
                      <FilterSectionHeader>
                        <CollapseTrigger>
                          <FilterSectionTitle>
                            {section.title}
                          </FilterSectionTitle>
                          <When condition={section.hasFilterIcon}>
                            <FilterIconContainer>
                              <FilterIconWrapper>
                                <FilterIcon
                                  groupSrc={FILTER_ICON_GROUP}
                                  imageSrc={FILTER_ICON_IMAGE}
                                />
                              </FilterIconWrapper>
                            </FilterIconContainer>
                          </When>
                        </CollapseTrigger>
                      </FilterSectionHeader>

                      <CollapseContent>
                        <div style={{ marginTop: '8px', marginBottom: '12px' }}>
                          <FilterOptionsContainer
                            style={{
                              maxHeight:
                                sectionSize === 'small'
                                  ? '200px'
                                  : sectionSize === 'large'
                                    ? '500px'
                                    : '300px',
                            }}
                          >
                            {section.options.map((option) => (
                              <FilterOptionButton
                                key={option.id}
                                isSelected={option.isSelected}
                                onClick={() =>
                                  handleFilterToggle(section.id, option.id)
                                }
                              >
                                <FilterOptionLabel>
                                  <FilterOptionText
                                    isSelected={option.isSelected}
                                  >
                                    {option.label}
                                  </FilterOptionText>
                                </FilterOptionLabel>
                              </FilterOptionButton>
                            ))}
                          </FilterOptionsContainer>
                        </div>
                      </CollapseContent>
                    </CollapseContainer>
                  )}
                </Collapse>
              </FilterSectionContainer>
            );
          })}
        </When>

        <ActionButtonsContainer>
          <ButtonContainer>
            <ResetFiltersButton onClick={handleResetFilters}>
              Reset Filters
            </ResetFiltersButton>
          </ButtonContainer>
          <ButtonContainer>
            <UnderstandingDataButton onClick={handleUnderstandingData}>
              Understanding the Data
            </UnderstandingDataButton>
          </ButtonContainer>
        </ActionButtonsContainer>
      </SidebarContent>
      <SidebarBorder />

      <DRMPolicyPillarsModal
        isOpen={isDRMModalOpen}
        onClose={handleCloseDRMModal}
      />
    </SidebarContainer>
  );
}

export default Sidebar;
