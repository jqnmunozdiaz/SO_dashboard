import { NextResponse } from 'next/server';
import {
  getFyColumns,
  loadMetadata,
  loadPortfolioFiltered,
  sumDisbursementsByFyAndSource,
} from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const portfolio = loadPortfolioFiltered(filters);
    const metadata = loadMetadata();
    const { fyColumns, fyShortLabels } = getFyColumns(portfolio, metadata);
    const { ibrd, ida, ibrdAndIda } = sumDisbursementsByFyAndSource(
      portfolio,
      fyColumns
    );
    const total = ibrd.map((v, i) => v + ida[i] + ibrdAndIda[i]);
    return NextResponse.json({
      fiscalYears: fyColumns,
      labels: fyShortLabels,
      ibrd,
      ida,
      ibrdAndIda,
      total,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
