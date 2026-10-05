# Security notes

## Trust boundaries

User question → local embedding model → retrieved document paragraphs → prompt preview.
Documents are data, not trusted instructions. The lab has no external LLM call, shell tool execution, or autonomous actions. The initial installation/model download uses the network; inference runs locally.

## Risks and limits

- Retrieval can surface malicious or incorrect content. A high cosine score measures similarity, not trustworthiness.
- The JSON wrapper and prompt instruction help describe the boundary but are not an injection-proof defense. Real deployments need tool authorization, least privilege, tenant-aware retrieval access checks, and independent output validation.
- Never place credentials, customer records, or private project sources in the public sample corpus. Embeddings and logs can expose sensitive information too.
- `.gitignore` prevents accidental staging of common secret files; it does not scan for secrets or remove previously committed secrets.
- Model and Python dependencies introduce supply-chain risk. The lab disables remote model code and records exact installed package versions. The model revision is not pinned; this is a learning lab, not a production reproducibility guarantee.
- The English model and tiny corpus have limited coverage. Top-k always returns nearest items, even for unrelated questions. No confidence threshold has been calibrated.

## Safe experiment

Run `python -m lab.semantic_search "How does a firewall filter traffic?" --top-k 3 --rag --include-attack`.
Observe whether the malicious fixture is retrieved. Retrieval is not itself successful injection: no language model is asked to obey it here.
Inspect which text is reference data and which instructions belong to the application. Never treat a prompt-only policy as a complete security boundary.
