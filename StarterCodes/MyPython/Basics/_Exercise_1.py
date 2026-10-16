# Exercise: Create a Class

# Create a class named Document.

# It should have:

# * document_id
# * filename
# * status

# Requirements:

# 1. Initialize all three attributes in __init__().
# 2. Set the default status to "pending".
# 3. Add a method named mark_processed().
# 4. Add a method named is_processed() that returns True if the document has been processed and False otherwise.


# Example Uses:
# document = Document(1, "guide.pdf")
# print(document.is_processed())  # False
# document.mark_processed()
# print(document.is_processed())  # True


class Document:
    def __init__(self, document_id: int, filename: str, status = "pending") -> None:
        self.document_id = document_id
        self.filename = filename
        self.status = status

    def mark_processed(self) -> None:
        self.status = "processed"

    def is_processed(self) -> bool:
        if self.status == "processed":
            return True
        else:
            return False

document = Document(1, "guide.pdf")
print(document.is_processed())
document.mark_processed()
print(document.is_processed())