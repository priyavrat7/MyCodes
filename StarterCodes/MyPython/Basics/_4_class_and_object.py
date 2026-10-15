class Document:
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content

    def get_summary_input(self) -> str:
        print(f"self instance of this class is: {self}")
        return self.content[:100]

document = Document(
    filename = "guide.pdf",
    content = "This document explains the organization's security policies"
)
print(f"File name of the document whose object is document is: {document.filename}\n")
print(f"File content of the document whose object is document is: {document.content}\n")
print(f"Summary of this document is: {document.get_summary_input()}\n")
print(document.get_summary_input)