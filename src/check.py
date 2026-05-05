from rag import FinancialAssistant

assistant = FinancialAssistant()
index = assistant.vector_db

unique_sections = set()

# Iterate through all documents in the FAISS store
for doc_id, doc in index.docstore._dict.items():
    # Collect ALL header levels found in metadata
    h1 = doc.metadata.get("Header 1", "")
    h2 = doc.metadata.get("Header 2", "")
    h3 = doc.metadata.get("Header 3", "")

    # Combine them to see the full "path"
    full_path = " > ".join(filter(None, [h1, h2, h3]))
    if full_path:
        unique_sections.add(full_path)

print(f"Total Chunks in DB: {len(index.docstore._dict)}")
print("\nDetailed Section Map:")
for section in sorted(unique_sections):
    print(f"- {section}")
