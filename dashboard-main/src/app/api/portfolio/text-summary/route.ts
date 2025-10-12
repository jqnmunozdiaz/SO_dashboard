import { NextResponse } from 'next/server';
import {
  buildTextSummary,
  loadMetadata,
  loadPortfolioFiltered,
} from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const portfolio = loadPortfolioFiltered(filters);
    const metadata = loadMetadata();
    const result = buildTextSummary(portfolio, metadata);
    return NextResponse.json(result);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
