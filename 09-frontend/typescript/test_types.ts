/**
 * =============================================================================
 * RAG Technology Testing Lab — Technology 18: TypeScript
 * =============================================================================
 *
 * 1. TECHNOLOGY OVERVIEW:
 *    TypeScript provides static type checking on top of JavaScript. In a RAG
 *    frontend UI, TypeScript guarantees:
 *    - Strict type validation between backend API models and frontend components.
 *    - Type safety for citation bounding box coordinates passed to PDF.js.
 *    - Discriminated union handling for asynchronous retrieval states (idle/loading/success/error).
 *    - Multilingual language tags ('en' | 'km' | 'mixed').
 *
 * 2. EXECUTION INSTRUCTIONS:
 *    npx tsc --noEmit
 * =============================================================================
 */

export type DocumentLanguage = "en" | "km" | "mixed";

export interface BoundingBox {
  readonly x0: number;
  readonly y0: number;
  readonly x1: number;
  readonly y1: number;
}

export interface Citation {
  readonly docId: string;
  readonly pageNumber: number;
  readonly chunkId: string;
  readonly snippet: string;
  readonly language: DocumentLanguage;
  readonly bbox?: BoundingBox;
}

export interface RAGQueryRequest {
  question: string;
  topK: number;
  language?: DocumentLanguage;
  filters?: Record<string, string | number | boolean>;
}

export type RAGQueryState =
  | { status: "idle" }
  | { status: "loading"; startedAt: number }
  | { status: "success"; query: string; answer: string; citations: Citation[]; latencyMs: number }
  | { status: "error"; message: string; errorCode: number };

/**
 * Filter citations by target language with strict generic typing.
 */
export function filterCitationsByLanguage<T extends Citation>(
  citations: readonly T[],
  targetLanguage: DocumentLanguage
): T[] {
  return citations.filter((c) => c.language === targetLanguage);
}

/**
 * Validates a citation bounding box geometry.
 */
export function isValidBoundingBox(bbox: BoundingBox): boolean {
  return bbox.x1 > bbox.x0 && bbox.y1 > bbox.y0;
}

// =============================================================================
// COMPILE-TIME VERIFICATION SAMPLES
// =============================================================================

const sampleEnglishCitation: Citation = {
  docId: "DOC-EN-001",
  pageNumber: 1,
  chunkId: "DOC-EN-001-p1-c001",
  snippet: "Retrieval-Augmented Generation grounds LLM answers with retrieved context.",
  language: "en",
  bbox: { x0: 40.0, y0: 115.0, x1: 555.0, y1: 320.0 },
};

const sampleKhmerCitation: Citation = {
  docId: "DOC-KM-002",
  pageNumber: 2,
  chunkId: "DOC-KM-002-p2-c001",
  snippet: "ប្រព័ន្ធ RAG ជួយបង្កើនគុណភាពនៃចម្លើយរបស់បញ្ញាសិប្បនិម្មិត។",
  language: "km",
};

const citationsList: readonly Citation[] = [sampleEnglishCitation, sampleKhmerCitation];

// Test generic filtering
const khmerOnly = filterCitationsByLanguage(citationsList, "km");
console.log(`TypeScript Test: Verified ${khmerOnly.length} Khmer citation(s).`);

// Test state transition with discriminated union
const currentState: RAGQueryState = {
  status: "success",
  query: "តើអ្វីជា RAG?",
  answer: "RAG គឺជាស្ថាបត្យកម្មដែលរួមបញ្ចូលការស្វែងរកឯកសារយោងជាមួយនឹង LLM។",
  citations: [sampleKhmerCitation],
  latencyMs: 145,
};

if (currentState.status === "success") {
  console.log(`Query Answer: ${currentState.answer} (${currentState.citations.length} citation)`);
}
