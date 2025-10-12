import { NextResponse } from 'next/server';
import { loadMetadata } from '@/lib/portfolio';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const metadata = loadMetadata();
    return NextResponse.json({ data: metadata });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
