import { NextResponse } from 'next/server';
import { loadPortfolioFiltered } from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

type ListRow = {
  id: string;
  projectId: string;
  country: string;
  projectName: string;
  fiscalYear: string;
  status: string;
  activationForCovid: string;
  financier: string;
  region: string;
  globalPractice: string;
  operationType: string;
};

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const rows = loadPortfolioFiltered(filters);
    const list: ListRow[] = rows.map((r, index) => {
      const pid = (r['P#'] ?? '').toString().trim();
      const safeId = pid ?? `row-${index + 1}`;
      return {
        id: safeId,
        projectId: pid,
        country: (r['Country'] ?? '').toString().trim(),
        projectName: (r['Description'] ?? '').toString().trim(),
        fiscalYear: (r['Fiscal Year'] ?? '').toString().trim(),
        status: (r['Status'] ?? '').toString().trim(),
        activationForCovid: (
          r['Activation for COVID'] ??
          r['Activation for COVID '] ??
          ''
        )
          .toString()
          .trim(),
        financier: (r['Source'] ?? '').toString().trim(),
        region: (r['Region'] ?? '').toString().trim(),
        globalPractice: (r['Global Practice'] ?? '').toString().trim(),
        operationType: (r['Standalone/Mixed'] ?? '').toString().trim(),
      };
    });
    return NextResponse.json({ data: list });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
