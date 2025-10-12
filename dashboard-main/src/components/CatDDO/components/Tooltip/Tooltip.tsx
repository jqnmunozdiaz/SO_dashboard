import React from 'react';

interface TooltipProps {
  content: string;
}

export const Tooltip: React.FC<TooltipProps> = ({ content }) => {
  return (
    <div className="bg-white border border-[#295e84] rounded-lg p-3 shadow-lg">
      <div className="font-['Inter:Regular',_sans-serif] font-normal relative shrink-0 text-[14px] w-full text-[#295e84]">
        {content}
      </div>
    </div>
  );
};

export default Tooltip;
