# Encaptulation: Grouping related state and behaviour together and 
# controlling how internal state is accessed or modified.
class Document:
    def __init__(self, filename: str):
        self.filename = filename
        self._status = "pending"

    def mark_processed(self) -> None:
        self._status = "processed"

    def get_status(self) -> str:
        return self._status

document = Document(
    "policies.pdf"
)
print(f"Current status is: {document.get_status()}\n")
print(f"Document is being processed\n")
document.mark_processed()
print(f"Current status is: {document.get_status()}\n")