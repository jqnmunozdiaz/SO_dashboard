'use client';

import {
  Sidebar,
  SidebarContent,
  HeaderContainer,
  LogoContainer,
  LogoText,
  TitleContainer,
  MainTitle,
  Subtitle,
  Navigation,
  FilterSection,
  FilterTitle,
  FilterList,
  CheckboxLabel,
  CheckboxInput,
  CheckboxText,
  BlueFilterList,
  FilterItem,
} from './Layout.styled';

export function WorldBankSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <HeaderContainer>
          <LogoContainer>
            <LogoText>WB</LogoText>
          </LogoContainer>
          <TitleContainer>
            <MainTitle>THE WORLD BANK</MainTitle>
            <Subtitle>IBRD • IDA | WORLD BANK GROUP</Subtitle>
          </TitleContainer>
        </HeaderContainer>

        <Navigation>
          <FilterSection>
            <FilterTitle>Project Status</FilterTitle>
            <FilterList>
              <CheckboxLabel>
                <CheckboxInput />
                <CheckboxText>Dropped</CheckboxText>
              </CheckboxLabel>
              <CheckboxLabel>
                <CheckboxInput />
                <CheckboxText>Pipeline</CheckboxText>
              </CheckboxLabel>
            </FilterList>
          </FilterSection>

          <FilterSection>
            <FilterTitle>Region</FilterTitle>
            <BlueFilterList>
              <FilterItem>AFE</FilterItem>
              <FilterItem>AFW</FilterItem>
              <FilterItem>EAP</FilterItem>
              <FilterItem>ECA</FilterItem>
              <FilterItem>LCR</FilterItem>
              <FilterItem>MNA</FilterItem>
              <FilterItem>SAR</FilterItem>
            </BlueFilterList>
          </FilterSection>

          <FilterSection>
            <FilterTitle>Country</FilterTitle>
            <BlueFilterList>
              <FilterItem>Barbados</FilterItem>
              <FilterItem>Belize</FilterItem>
              <FilterItem>Benin</FilterItem>
              <FilterItem>Bhutan</FilterItem>
              <FilterItem>Cabo Verde</FilterItem>
              <FilterItem>Chile</FilterItem>
              <FilterItem>Colombia</FilterItem>
            </BlueFilterList>
          </FilterSection>
        </Navigation>
      </SidebarContent>
    </Sidebar>
  );
}
