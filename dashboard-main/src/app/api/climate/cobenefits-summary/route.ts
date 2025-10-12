import { NextResponse } from 'next/server';
import { cobenefitsSummary } from '@/lib/climate';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const result = cobenefitsSummary();
    return NextResponse.json(result);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
