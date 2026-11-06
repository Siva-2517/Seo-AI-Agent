export interface KeywordData {
  keyword: string;
  search_intent: string;
  relevance: string;
  competition: string;
  search_volume: string;
  data_confidence: string;
  source?: string;
  opportunity_score?: number;
}

export interface ExecutionLog {
  timestamp: string;
  agent: string;
  message: string;
  level: string;
}

export interface ExecutionStatus {
  execution_id: string;
  current_agent?: string;
  status: string;
  execution_logs: ExecutionLog[];
  started_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface FAQItem {
  question: string;
  answer: string;
}

export interface Blog {
  id: number;
  title: string;
  slug: string;
  meta_title: string;
  meta_description: string;
  h1: string;
  primary_keyword: string;
  secondary_keywords: string[];
  content: string;
  faq?: FAQItem[];
  validation_score: number;
  status: string;
  created_at: string;
}

export interface GenerationResponse {
  execution_id: string;
  status: string;
  message: string;
}

export interface ResearchResponse {
  execution_id: string;
  keywords: KeywordData[];
  selected_primary_keyword?: string;
  selected_secondary_keywords?: string[];
  selection_reasoning?: string;
}
