An embedding represents text as a numeric vector. Semantic search ranks document vectors by similarity to a query vector. Similarity does not establish accuracy or authority.

Retrieval augmented generation retrieves relevant passages, adds them to model context, and asks a language model to generate an answer. Retrieval alone is not generation.

Indirect prompt injection places malicious instructions in retrieved documents or tool outputs. Treat these sources as untrusted data and enforce authorization outside the language model.
