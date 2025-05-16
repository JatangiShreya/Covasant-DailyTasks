
import sys
import os
import logging
from google.cloud import documentai_v1 as documentai


PROJECT_ID = "smart-road-460003-i1"   
LOCATION = "us"                    
PROCESSOR_ID = "4048e73eea949b98"    


def parse_ocr(file_path):   
    logging.info(f"Reading file: {file_path}")
    
    # It is used to setup secure connection to google cloud document ai secure
    # and also for reads authentication credentials from .json file
    
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
    
    # file sending to google cloud
    result = client.process_document(request=request)
    doc = result.document
    logging.info("OCR processing complete.")
    print("\n===== Extracted Text =====\n")
    
    # Here is the final extracted text
    print(doc.text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_file = sys.argv[1]
    parse_ocr(input_file)

