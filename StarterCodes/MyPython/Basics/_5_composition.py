# Composition: It means that, one object can contains or uses another object to 
# perform its work
class DocumentRepository:
    def save(self, filename: str) -> None:
        print(f"Saving {filename} to the database")

class DocumentService:
    def __init__(self, repository: DocumentRepository):
        print(f"DEBUG: {repository}\n")
        self.repository = repository
        print(f"DEBUG: {self.repository}\n")

    def process_document(self, filename: str) -> None:
        print(f"Processing {filename}")
        self.repository.save(filename)

repository = DocumentRepository()
service = DocumentService(repository)

service.process_document("guide.pdf")
