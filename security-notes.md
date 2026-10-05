# Security notes

## Trust boundaries

User question → local embedding model → retrieved document paragraphs → prompt preview or local Ollama generation.
Documents are data, not trusted instructions. With `--generate`, the question and retrieved passages are sent to the loopback Ollama chat API using separate system/user roles. The lab has no shell tool execution or autonomous actions. The initial installation/model downloads use the network; embedding and answer inference run locally. Model files are stored outside the Git repository.

## Risks and limits

- Retrieval can surface malicious or incorrect content. A high cosine score measures similarity, not trustworthiness.
- The JSON wrapper and prompt instruction help describe the boundary but are not an injection-proof defense. Real deployments need tool authorization, least privilege, tenant-aware retrieval access checks, and independent output validation.
- Never place credentials, customer records, or private project sources in the public sample corpus. Embeddings and logs can expose sensitive information too.
- `.gitignore` prevents accidental staging of common secret files; it does not scan for secrets or remove previously committed secrets.
- Model and Python dependencies introduce supply-chain risk. The lab disables remote model code and records exact installed package versions. The model revision is not pinned; this is a learning lab, not a production reproducibility guarantee.
- The English model and tiny corpus have limited coverage. Top-k always returns nearest items, even for unrelated questions. No confidence threshold has been calibrated.

## Safe experiment

Run `python -m lab.semantic_search "How does a firewall filter traffic?" --top-k 3 --rag --include-attack`.
Observe whether the malicious fixture is retrieved. Retrieval alone is not successful injection. Add `--generate` to inspect how the local model responds to that context; this experiment is not a comprehensive security evaluation.
Inspect which text is reference data and which instructions belong to the application. Never treat a prompt-only policy as a complete security boundary.

The client uses a fixed loopback endpoint, ignores system HTTP proxies, and rejects model names containing `cloud`. These choices reduce accidental remote use; they do not attest to the integrity or configuration of the installed Ollama server. No tools are passed to the model. Keep Ollama bound to loopback and do not expose it publicly.

Citation label validation compares bracketed labels with source IDs retrieved for the current request. Unknown or missing labels produce advisory warnings; the answer is not rewritten or blocked. Numeric labels are not mapped to sources automatically. A matching ID can still cite malicious content or accompany an unsupported claim. Factual correctness, evidence support, and injection resistance are not automatically verified.
