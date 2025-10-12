'use client';

import React from 'react';
import { StepModal, Image } from 'vizonomy';
import {
  ModalContent,
  ContentWrapper,
  TextSection,
  TextContainer,
  TitleContainer,
  DisclaimerText,
  WelcomeTitle,
  DescriptionText,
  EnterButton,
  ButtonText,
  LogoSection,
  LogoGrid,
  LogoRow,
  LogoItem,
  LogoBottomRow,
} from './WelcomeModal.styled';

interface WelcomeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const WelcomeModal: React.FC<WelcomeModalProps> = ({ isOpen, onClose }) => {
  return (
    <StepModal.Root isOpen={isOpen} onClose={onClose}>
      <StepModal.Overlay className="z-[9999]">
        <StepModal.Content
          size="xl"
          className="!w-[900px] max-w-[900px] max-h-[90vh] overflow-y-auto z-[10000] !bg-[#f9fafb] shadow-2xl"
        >
          <StepModal.Body className="px-8 py-[41px]">
            <StepModal.Step>
              <ModalContent>
                <ContentWrapper>
                  <TextSection>
                    <TextContainer>
                      <TitleContainer>
                        <DisclaimerText>DISCLAIMER</DisclaimerText>
                        <WelcomeTitle>Welcome</WelcomeTitle>
                      </TitleContainer>
                      <DescriptionText>
                        This dashboard was made possible with the financial
                        support from the Japan-Bank Program for Mainstreaming
                        Disaster Risk Management in Developing Countries, which
                        is financed by the Government of Japan and receives
                        technical support from the World Bank Global Facility
                        for Disaster Reduction and Recovery (GFDRR) Tokyo
                        Disaster Risk Management Hub.
                      </DescriptionText>
                    </TextContainer>

                    <EnterButton onClick={onClose}>
                      <ButtonText>
                        <p className="leading-[20px] whitespace-pre">Enter</p>
                      </ButtonText>
                    </EnterButton>
                  </TextSection>

                  <LogoSection>
                    <LogoGrid>
                      <LogoRow>
                        <LogoItem>
                          <Image
                            src="/world-bank-logo.png"
                            alt="World Bank Logo"
                            className="h-[65px] w-auto object-contain"
                          />
                        </LogoItem>

                        <LogoItem>
                          <Image
                            src="/japan-gov-logo.png"
                            alt="Japan Government Logo"
                            className="h-[57px] w-auto object-contain"
                          />
                        </LogoItem>
                      </LogoRow>

                      <LogoBottomRow>
                        <LogoItem>
                          <Image
                            src="/gfdrr-logo.png"
                            alt="GFDRR Logo"
                            className="h-[82px] w-auto object-contain"
                          />
                        </LogoItem>
                      </LogoBottomRow>
                    </LogoGrid>
                  </LogoSection>
                </ContentWrapper>
              </ModalContent>
            </StepModal.Step>
          </StepModal.Body>
        </StepModal.Content>
      </StepModal.Overlay>
    </StepModal.Root>
  );
};

export default WelcomeModal;
