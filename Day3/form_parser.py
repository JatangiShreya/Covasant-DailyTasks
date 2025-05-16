import os
import sys
import logging
from google.cloud import documentai_v1 as documentai

PROJECT_ID = "smart-road-460003-i1"
LOCATION = "us"  
PROCESSOR_ID = "7dd54b3023133fe7" 

def parse_form_or_invoice(file_path):
    logging.info(f"Processing file: {file_path}")
    
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
    
    with open(file_path, "rb") as file:
        file_content = file.read()
  
    if file_path.endswith(".pdf"):
        mime_type = "application/pdf"
    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        mime_type = "image/jpeg"
    else:
        logging.error("Only PDF and image files are supported.")
        return
  
    document = {
        "content": file_content,
        "mime_type": mime_type,
    }  
    request = {"name": name, "raw_document": document}
    try:
        result = client.process_document(request=request)  
        doc = result.document
        logging.info("Field extraction complete.")
        print(f"Document text: {doc.text}")    
        print("\n===== Extracted Fields =====")
        print(doc.entities)
        for entity in doc.entities:
            print(f"Entity type: {entity.type_}, Mention text: {entity.mention_text}")
    except Exception as e:
        logging.error(f"Error during field extraction: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_file = sys.argv[1]
    parse_form_or_invoice(input_file)
