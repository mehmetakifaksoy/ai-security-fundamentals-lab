# AI Security Fundamentals Lab

A hands-on Python lab for embeddings, cosine similarity, semantic search, and RAG context preparation. Includes a synthetic prompt injection experiment. No API key or paid service is required.

## How it works

```text
Text → tokenizer/model → embedding vector
Question + document vectors → cosine similarity → nearest paragraphs
Retrieved paragraphs + question → prompt/messages → local LLM answer (Ollama)
```

This version runs real embedding inference and retrieval. `--rag` previews a prompt; `--generate` sends separate system/user messages to a local Ollama model and prints its answer. Retrieval and generation are separate steps.

## 1. Open the project in VS Code

To clone the repository using Windows PowerShell:

```powershell
git clone https://github.com/mehmetakifaksoy/ai-security-fundamentals-lab.git
cd ai-security-fundamentals-lab
code .
```

If the project already exists in your home directory:

```powershell
cd "$HOME\ai-security-fundamentals-lab"
code .
```

In VS Code, select **Terminal → New Terminal**. With the Python extension installed, press `Ctrl+Shift+P`, select **Python: Select Interpreter**, and choose `.venv\Scripts\python.exe` after creating the environment below. Open files in the Explorer panel.

Run all commands below from the project directory. Paths beginning with `.\` are relative to your terminal's current directory.

## 2. Create a virtual environment and install dependencies

Use Python 3.12 for the validated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

`.venv` isolates this project's packages. `requirements.txt` declares the direct dependency; `requirements-lock.txt` records all package versions from the validated environment. On Linux/macOS, use `.venv/bin/python`. Activation is optional because these commands explicitly select the environment's interpreter.

## 3. Compare sentence embeddings

Before running the example, predict which sentence will be closest to the firewall sentence.

```powershell
.\.venv\Scripts\python.exe -m lab.embedding_similarity
```

The `sentence-transformers/all-MiniLM-L6-v2` model encodes three sentences as 384-dimensional vectors. For normalized vectors, the dot product equals cosine similarity. A score is not a probability: `0.8` does not mean 80% accuracy.

The first run downloads the model from the internet. Later runs use cached model files. Dependencies and model files may occupy several hundred MB of disk space. Download and loading messages are expected.

Validated example output (small differences may occur across environments or model revisions):

```text
Embedding shape: (3, 384)
1 vs 2: cosine=0.6039
1 vs 3: cosine=0.0393
2 vs 3: cosine=0.0336
```

## 4. Search the sample documents

```powershell
.\.venv\Scripts\python.exe -m lab.semantic_search "How can I prevent account takeover?"
```

Documents are split into paragraphs at blank lines (chunking). The question and paragraphs are encoded with the same model. The two nearest paragraphs are returned with scores and source IDs. This small corpus stays in memory; no vector database is needed.

## 5. Prepare RAG context and explore trust boundaries

```powershell
.\.venv\Scripts\python.exe -m lab.semantic_search "What is prompt injection?" --rag
.\.venv\Scripts\python.exe -m lab.semantic_search "How does a firewall filter traffic?" --top-k 3 --rag --include-attack
```

The second command includes an intentionally malicious sample document. Relevant content can also contain untrusted instructions. The preview is a single string; a real LLM integration should send system and user instructions using their respective message roles and enforce permissions in the application. See [security-notes.md](security-notes.md) for the experiment's limits.

## Project structure

```text
lab/                      # Shared helpers and two runnable examples
data/knowledge/           # Public synthetic reference paragraphs
data/attack/              # Opt-in prompt injection fixture
tests/                    # Integration checks using the real embedding model
.vscode/settings.json     # Project interpreter preference
requirements*.txt         # Direct and locked dependencies
security-notes.md         # Risks, limitations, and trust boundaries
```

## Local answer generation with Ollama

Install [Ollama for Windows](https://ollama.com/download/windows), then open a new terminal so the `ollama` command is available. Alternatively:

```powershell
winget install --id Ollama.Ollama --exact
```

With Ollama running, download the local model once:

```powershell
ollama pull qwen2.5:3b
```

The model download is approximately 1.9 GB, separate from the Ollama installation. The lab was set up on a Windows computer with 16 GB RAM and an NVIDIA RTX 3060 Ti; speed and memory needs vary. If needed, try the smaller `qwen2.5:1.5b` model and pass `--model qwen2.5:1.5b`.

From the project directory, generate a source-grounded answer:

```powershell
.\.venv\Scripts\python.exe -m lab.semantic_search "How can I prevent account takeover?" --generate
```

Compare with the injection experiment:

```powershell
.\.venv\Scripts\python.exe -m lab.semantic_search "How does a firewall filter traffic?" --top-k 3 --include-attack --generate
```

Inspect whether the answer cites relevant sources and follows the malicious passage. A safe answer in one run does not prove injection resistance. Generated citations and claims are not automatically validated.

`lab/local_llm.py` calls `http://127.0.0.1:11434/api/chat` with no tools and no system HTTP proxy. No additional Python dependency is needed. This is a local API, not a paid cloud service. Generation uses temperature 0, a 4,096-token context, and a 384-token output limit. Model tags are mutable and generation is not guaranteed deterministic.

If Ollama is unavailable, start the application or run `ollama serve` in another terminal. If the model is missing, run `ollama pull qwen2.5:3b`. The client reports connection, timeout, and missing-model errors without silently switching to a cloud provider.

References: [Ollama chat API](https://docs.ollama.com/api/chat), [Windows setup](https://docs.ollama.com/windows), [Qwen2.5 3B model](https://ollama.com/library/qwen2.5:3b).

## 6. Track and publish changes

For a new local project without an existing Git repository or GitHub remote:

```powershell
git init -b main
git add .
git commit -m "Add AI security fundamentals learning lab"
gh repo create ai-security-fundamentals-lab --public --source . --remote origin --push
```

These commands require Git and an authenticated GitHub CLI session. Skip them if you cloned this repository or it is already initialized. For subsequent changes to your own repository:

```powershell
git status
git diff
git add lab/embedding_similarity.py
git commit -m "Explore additional sentence similarities"
git push
```

A commit records changes locally; a push sends commits to GitHub. `.gitignore` excludes the virtual environment, common cache/output directories, and `.env` files. Review your changes before staging them.

## Validation

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The checks verify embedding dimensions and relative similarity, retrieval of a relevant source, and source labels in the prompt. They do not establish resistance to prompt injection. The first test run may download the model.

## Learning exercises

1. Replace the banana sentence with another network-related sentence. Predict how the scores will change before running the example.
2. Add a Markdown document to `data/knowledge/` and ask a related question using different wording.
3. Ask for a recipe outside the corpus. Observe that nearest-neighbor retrieval still returns results.
4. Compare `--top-k 1` with `--top-k 3` to see how the amount of context changes.
5. Inspect the injection fixture. Where does the document switch from reference information to an attempted instruction?

Reference: [Sentence Transformers official quickstart](https://www.sbert.net/docs/quickstart.html).
