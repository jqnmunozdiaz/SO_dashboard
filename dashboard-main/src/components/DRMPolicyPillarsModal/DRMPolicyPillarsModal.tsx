import React from 'react';
import { Button, StepModal } from 'vizonomy';
import { useFetchMetadata } from '@/hooks/useFetchMetadata';
import { formatLastUpdate } from '@/utils/date-utils';
import {
  ContentContainer,
  DescriptionContainer,
  DescriptionText,
  ButtonContainer,
} from './DRMPolicyPillarsModal.styled';

interface DRMPolicyPillarsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const DRMPolicyPillarsModal: React.FC<DRMPolicyPillarsModalProps> = ({
  isOpen,
  onClose,
}) => {
  const { metadata, isLoading } = useFetchMetadata();

  return (
    <StepModal.Root isOpen={isOpen} onClose={onClose}>
      <StepModal.Overlay className="z-[9999]">
        <StepModal.Content
          size="xl"
          className="!w-[900px] max-w-[900px] max-h-[90vh] overflow-y-auto z-[10000] !bg-[#f9fafb] shadow-2xl"
        >
          <StepModal.Header>
            <StepModal.Title className="text-[32px] font-bold !text-[#295e84] leading-[32px]">
              Understanding Data
            </StepModal.Title>
            <StepModal.Close className="!text-[#295e84] hover:!text-[#1e4a6b]" />
          </StepModal.Header>

          <StepModal.Body className="px-8 pt-2 pb-[41px]">
            <StepModal.Step>
              <ContentContainer>
                <DescriptionContainer className="gap-2">
                  <DescriptionText>
                    This dashboard compiles information extracted from the World
                    Bank operations portal as of{' '}
                    {formatLastUpdate(metadata, isLoading)}. It covers three
                    essential dimensions related to DPF Cat DDOs: (i) portfolio
                    financial trends, (ii) DPF Cat DDO policy program and
                    DRM-related reforms supported through past operations, and
                    (iii) DPF Cat DDO disbursement triggers' definition and use.
                  </DescriptionText>
                </DescriptionContainer>
              </ContentContainer>
            </StepModal.Step>
          </StepModal.Body>

          <StepModal.Footer>
            <ButtonContainer>
              <Button
                variant="primary"
                size="md"
                onClick={onClose}
                className="bg-[#295e84] text-white px-6 py-[13px] rounded-[99px] font-bold text-[14px] leading-[20px] tracking-[-0.15px] hover:bg-[#1e4a6b] transition-colors"
              >
                Close
              </Button>
            </ButtonContainer>
          </StepModal.Footer>
        </StepModal.Content>
      </StepModal.Overlay>
    </StepModal.Root>
  );
};

export default DRMPolicyPillarsModal;
