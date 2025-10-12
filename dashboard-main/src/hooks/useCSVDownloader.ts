import { useCallback } from 'react';
import Papa from 'papaparse';

export const useCSVDownloader = () => {
  const downloadCSV = useCallback(
    <T extends Record<string, unknown>>(
      data: T[],
      filename: string,
      headers?: Record<keyof T, string>
    ): void => {
      const csvContent = Papa.unparse(data, {
        header: true,
        columns: headers ? Object.keys(headers) : undefined,
        delimiter: ',',
        quoteChar: '"',
        escapeChar: '"',
        newline: '\r\n',
        skipEmptyLines: true,
        quotes: (value: unknown) => {
          if (typeof value === 'string') {
            return (
              value.includes('\n') ||
              value.includes('\r') ||
              value.includes(',') ||
              value.includes('"')
            );
          }
          return false;
        },
      });

      const BOM = '\uFEFF';
      const blob = new Blob([BOM + csvContent], {
        type: 'text/csv;charset=utf-8;',
      });

      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `${filename}.csv`);
      link.click();
      URL.revokeObjectURL(url);
    },
    []
  );

  return { downloadCSV };
};
