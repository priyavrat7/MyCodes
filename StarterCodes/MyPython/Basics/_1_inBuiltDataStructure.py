# List
documents1 = ["docs1.pdf", "docs2.pdf", "docs3.pdf"]
documents1.append("docs4.pdf")
print(f"Document1 are {documents1}")

# Dictionary
documents2 = {
    "id": 1,
    "filename": "guide.pdf",
    "stauts": "processed"
}

print(f"Document2 are {documents2}")
print(documents2.get("id"))
print(documents2.get("filename"))
print(f"documents2.item() type is: {type(documents2.items())}")
print(f"Document2 are {documents2.items()}")

# Set
documents_types = {"pdf", "txt", "pdf"}
documents_types.add("csv")
print(f"Length of set is: {len(documents_types)}")
print(f"Documents types are: {documents_types}")

# Tuple
embedding_dimentions = (768,)
print(f"Type of embedding_dimentions = {type(embedding_dimentions)}")

tuple_values = (10, 20, 30, 20, 40, 50, 70)
print(tuple_values[0:5:2])
print(tuple_values[::-1]) # Reverse
print(tuple_values.index(70))
list_sorted = sorted(tuple_values)
print(list_sorted) # sorted list it will give
tuple_sorted = tuple(list_sorted)
print(tuple_sorted)
