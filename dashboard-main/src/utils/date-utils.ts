import type { Metadata } from '@/lib/portfolio';

export function formatLastUpdate(
  metadata: Metadata,
  isLoading: boolean
): string {
  if (
    isLoading ||
    !metadata.Update_Day ||
    !metadata.Update_Month ||
    !metadata.Update_Year
  ) {
    return 'Loading...';
  }

  const day = metadata.Update_Day.padStart(2, '0');
  const month = metadata.Update_Month.substring(0, 3);
  const year = metadata.Update_Year;

  return `${day} ${month} ${year}`;
}
