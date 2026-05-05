from docling.document_converter import DocumentConverter
import sys


def convert_docx_to_md(input_path, output_path):
    print(f"🚀 Converting {input_path}...")
    converter = DocumentConverter()
    result = converter.convert(input_path)

    # Export to markdown specifically to preserve table structures
    md_content = result.document.export_to_markdown()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ Success! Markdown saved to {output_path}")


if __name__ == "__main__":
    # Usage: python 1_extract.py my_finance.docx
    file_name = sys.argv[1] if len(sys.argv) > 1 else "data.docx"
    convert_docx_to_md(file_name, "knowledge.md")
