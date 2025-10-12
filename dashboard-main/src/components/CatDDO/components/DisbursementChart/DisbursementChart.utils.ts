export const formatValueToMillions = (value: number): string => {
  return `$${Math.round(value / 1000000)}M`;
};

export const formatTotalLabel = (total: number): string => {
  return formatValueToMillions(total);
};

export const formatValueLabel = (value: number): string => {
  return formatValueToMillions(value);
};

export const formatCategoryLabel = (category: string): string => {
  return category;
};
