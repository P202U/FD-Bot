# 🏦 Financial FD-Bot (Gemma-RAG)

A local, privacy-first Retrieval-Augmented Generation (RAG) assistant designed to answer questions about Fixed Deposit (FD) advisory reports. Powered by **Gemma 4 e2b**, **Docling**, and **FAISS**.

## 🚀 Features

- **Vernacular Support:** Optimized for Hindi and English queries.
- **Citations:** Every answer includes source section headers (e.g., `[Section 1.4]`).
- **Privacy First:** Entirely offline execution via **Ollama** and local embeddings.
- **Structured Parsing:** Uses Docling for high-accuracy Markdown extraction from complex `.docx` tables.

## 🛠️ Tech Stack

- **LLM:** Gemma 4 e2b (via Ollama)
- **Orchestration:** LangChain
- **Vector DB:** FAISS
- **Embeddings:** HuggingFace (`sentence-transformers`)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

## 📂 Project Structure

```text
├── data/               # Raw .docx input files
├── processed/          # Markdown outputs from Docling
├── vector_store/       # Local FAISS index
├── src/
│   ├── utils.py        # Configuration & Constants
│   ├── ingest.py # Document -> Vector Store
│   ├── rag.py   # Search & LLM Logic
│   └── app.py          # Streamlit Chat UI
└── pyproject.toml      # Managed by uv
```

## 🏗️ Setup Instructions

### 1. Prerequisites

- Install [Ollama](https://ollama.ai/) and pull the model:
  ```bash
  ollama pull gemma4:e2b  # Or your specific model version
  ```
- Install `uv`:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Installation

Clone the repo and sync dependencies:

```bash
uv sync
```

### 3. Ingest Data

Place your `.docx` files in the `data/` folder, then run:

```bash
uv run src/phase1_ingest.py
```

### 4. Run the App

Launch the Streamlit interface:

```bash
uv run streamlit run src/app.py
```

## 🔍 How it Works

1. **Ingestion:** Docling converts `.docx` to Markdown. `MarkdownHeaderTextSplitter` creates chunks based on Section Headers to preserve financial context.
2. **Retrieval:** When you ask a question, the system performs an **MMR (Maximum Marginal Relevance)** search in the FAISS index to find the most relevant, non-redundant sections.
3. **Generation:** The context is passed to Gemma with a system prompt that enforces citations and language matching.

## 📝 License

MIT License - Internal Financial Advisory Tool.
