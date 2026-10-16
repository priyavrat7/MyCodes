def get_document(document_id: int) -> dict:
    try:
        if document_id <= 0:
            raise ValueError("Document ID must be positive number\n")

        return{
            "id":   document_id,
            "filename": "guide.pdf"
        }
    except ValueError as error:
        print(f"[EXCEPT]Invalid input: {error}")
        raise # To give the CALLER a chance to handle the exception

    # Finally block is always executed, whether an exception is raised or not, 
    # only exit in the case of sys.exit() or os._exit() can prevent the execution of finally block
    finally:
        print(f"[FINALLY]: Clean executed: get_document run finished.")

raw_input = input("Enter the document id number: ")

try:
    document_id = int(raw_input)
    document_dict = get_document(document_id)
    print(f"[CALLER] Document fetched successfully: {document_dict}")

except ValueError as e:
    print(f"[CALLER] Failed to fetch document due to invalid ID: {e}\n")