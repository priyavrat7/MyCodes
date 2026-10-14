# List
documents = ["a.pdf", "b.txt", "c.pdf"]

# Filter only pdf documents using for loop
pdf_documents = []
for document in documents:
    if document.endswith(".pdf"):
        pdf_documents.append(document)

print(pdf_documents)

# Filter using list comprehension

pdf_documents1 = [
    document
    for document in documents
    if document.endswith(".pdf")
]
print(pdf_documents1)





# Exercise:  Given a list of dictionaries, return the filenames of
# successfully processed documents
print(f"\nEXERCISE\n") # Expected output = ['a.pdf', 'c.pdf']
documents = [
    {"filename": "a.pdf", "status": "processed"},
    {"filename": "b.pdf", "status": "failed"},
    {"filename": "c.pdf", "status": "processed"}
]

print(documents)

print(f"\nSOLUTION\n")

print(documents[0].get("filename")) # If "filename" is missing: It returns None
print(documents[0]["filename"]) # If "filename" is missing: It will throw a KeyError and instantly crash program

processed_pdf = []

for document in documents:
    print(f"DEBUG: {document.get("status")}")
    if document.get("status") == "processed":
        processed_pdf.append(document.get("filename"))
    
print(processed_pdf)

# Another approach using list compression
processed_pdf1 = [
    document.get("filename")
    for document in documents
    if document.get("status") == "processed"
]

print(pdf_documents1)