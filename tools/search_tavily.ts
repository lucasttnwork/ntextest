// tools/search_tavily.ts
// Uso: importar e chamar webSearch("sua pergunta")
// Requer TAVILY_API_KEY no .env

import fetch from "node-fetch";

type TavilyResult = {
  query: string;
  results: Array<{ url: string; title: string; content: string }>;
};

export async function webSearch(q: string, max = 5): Promise<TavilyResult> {
  const apiKey = process.env.TAVILY_API_KEY;
  if (!apiKey) throw new Error("TAVILY_API_KEY ausente no .env");
  const r = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      query: q,
      max_results: max,
      include_answer: false,
      include_raw_content: false
    })
  });
  if (!r.ok) {
    const text = await r.text();
    throw new Error(`Tavily API error: ${r.status} ${text}`);
  }
  return r.json() as Promise<TavilyResult>;
}
