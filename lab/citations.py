"""Check bracketed source labels against passages retrieved for this request."""
import re


def citation_warnings(answer, hits):
    allowed_sources = {hit["source"] for hit in hits}
    citations = re.findall(r"\[([^\[\]]+)\]", answer)
    # Accept both [identity.md#1] and [source: identity.md#1].
    citations = [re.sub(r"^source\s*:\s*", "", label.strip(), flags=re.IGNORECASE)
                 for label in citations]
    if not citations:
        return ["No source citations found. An abstention may be appropriate; review the answer."]
    invalid_sources = sorted({label for label in citations if label not in allowed_sources})
    if invalid_sources:
        return ["Citation labels not found in retrieved sources: " + ", ".join(invalid_sources)]
    return []
