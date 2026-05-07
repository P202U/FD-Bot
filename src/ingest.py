import os
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from utils import Config


def convert_to_markdown(docx_path):
    """Uses Docling to extract structured text and tables."""
    print(f"....Converting {docx_path} to Markdown...")
    converter = DocumentConverter()
    result = converter.convert(docx_path)
    md_content = result.document.export_to_markdown()

    with open(Config.KNOWLEDGE_BASE_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"....Saved clean Markdown to: {Config.KNOWLEDGE_BASE_MD}")
    return md_content


def semantic_chunking(md_content):
    """Splits text by headers to keep financial sections intact."""
    print("....Performing Semantic Chunking...")
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    chunks = splitter.split_text(md_content)
    print(f"....Created {len(chunks)} logical chunks.")
    return chunks


def create_vector_index(chunks):
    """Converts chunks to vectors and saves them locally."""
    print(f"....Building FAISS Index using {Config.EMBEDDING_MODEL}...")

    embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(Config.FAISS_INDEX_PATH)
    print(f"....Local 'Library' indexed at: {Config.FAISS_INDEX_PATH}")


def run_pipeline(filename):
    docx_input = os.path.join(Config.DATA_DIR, filename)

    if not os.path.exists(docx_input):
        print(f"....Error: Place your file in {Config.DATA_DIR} first!")
        return

    md_text = convert_to_markdown(docx_input)
    chunks = semantic_chunking(md_text)
    create_vector_index(chunks)
    print("\n.... Ingest complete")


if __name__ == "__main__":
    run_pipeline("FD_Advisory_Report_Section1_2.docx")
