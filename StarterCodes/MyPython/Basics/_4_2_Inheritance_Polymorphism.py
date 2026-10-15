# Inheritance: It allows one class to reuse or extend the behavior of another class.
class EmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError

class LocalEmbeddingProvider(EmbeddingProvider):
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]

class MockEmbeddingProvider(EmbeddingProvider):
    def embed(self, text: str) -> list[float]:
        return [0.0, 0.0, 0.0]

provider = LocalEmbeddingProvider()

vector = provider.embed("How do i request access?")

print(f"Vector by local embedding provider: {vector}")

# Polymorphism: It means that the different objects can expose the same operation while 
# implementing it differently

providers = [
    LocalEmbeddingProvider(),
    MockEmbeddingProvider()
]

for provider in providers:
    vector = provider.embed("Explain RAG")
    print(f"Vector is {vector}, by {provider}")