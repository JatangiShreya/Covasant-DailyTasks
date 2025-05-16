Google Cloud Document AI Usage Documentation
Overview
This script processes documents using Google Cloud Document AI to extract:

1)Text (OCR Parsing)

2)Layout (Text positions, Tables)

3)Form Fields (Key-Value pairs from forms)

Setup Instructions
Before using the Document AI API, ensure you have the following set up:

Steps:

1.Install the SDK:pip install google-cloud-documentai
2.Enable the Document AI API in your Google Cloud Project through the Google Cloud Console
3.Create a Processor:
In the Google Cloud Console, navigate to Document AI and create a processor for OCR, Layout, or Form Parsing.
Get the Processor ID for the created processor.
4.Authenticate API requests using a Service Account Key. Set the environment variable:
set GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account_key.json"

1. OCR Parser
Purpose: Extracts text content from scanned documents or images (PDF, JPEG, PNG).

code Snippet:

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


command to run:python ocr_parser.py sample2.pdf

output:

INFO:root:Reading file: sample2.pdf
INFO:root:OCR processing complete.

===== Extracted Text =====

Invoice Number: 12345
Invoice Date: 2025-01-01
Due Date: 2025-01-15
Total Amount: $500.00
Billing Address: 123 Main St, City, Country


2. Layout Parser
Purpose: Extracts the document's structure, including text positions and tables.

code:
import os
import sys
import logging
from google.cloud import documentai_v1 as documentai

PROJECT_ID = "smart-road-460003-i1"
LOCATION = "us"  
PROCESSOR_ID = "98106e8f06c9c0df" 

def parse_layout_document(file_path):
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
        raise Exception("Unsupported file type.")

    
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    
    try:
        result = client.process_document(request=request)
        document = result.document
    except Exception as e:
        logging.error(f"Error during field extraction: {e}")
        return

    print("\n=== Full Text ===\n")
    print(document.text)

   
    print("\n=== Form Fields (Key-Value Pairs) ===\n")
    if document.entities:
        for entity in document.entities:
            try:
                key = entity.text_anchor.text_segments[0]
                print(f"{entity.type_}: {entity.mention_text} (confidence: {entity.confidence:.2f})")
            except Exception as e:
                logging.warning(f"Skipping entity extraction due to error: {e}")
    else:
        print("No entities found.")

  
    print("\n=== Tables ===\n")
    if document.pages:
        for page in document.pages:
            if page.tables:
                for table_idx, table in enumerate(page.tables):
                    print(f"\nTable {table_idx + 1}:")
                    for row_idx, row in enumerate(table.header_rows + table.body_rows):
                        row_text = []
                        for cell in row.cells:
                            cell_text = extract_text(cell.layout.text_anchor, document)
                            row_text.append(cell_text.strip())
                        print(" | ".join(row_text))
            else:
                print("No tables found on this page.")
    else:
        print("No pages found in the document.")

def extract_text(text_anchor, document):
    """Extract text content using text segments."""
    response = ""
    for segment in text_anchor.text_segments:
        start = segment.start_index
        end = segment.end_index
        response += document.text[start:end]
    return response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_file = sys.argv[1]
    parse_layout_document(input_file)


command:python layout_parser.py sample2.pdf

3. Form Parser
Purpose: Extracts key-value pairs from structured forms like invoices or receipts.

code Snippet:
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
command:python form_parser.py sample3.pdf

output:
INFO:root:Processing file: sample3.pdf
INFO:root:Field extraction complete.
Document text: FakeDoc M.D.
HEALTH INTAKE FORM
Please fill out the questionnaire carefully. The information you provide will be used to complete
your health profile and will be kept confidential.
Date:
9/14/19
Name:
Sally Walker
DOB: 09/04/1986
Address: 24 Barney Lane
City: Towaco
State: NJ Zip: 07082
Email: Sally, walker@cmail.com
_Phone #: (906) 917-3486
Gender: F
Marital Status:
Single Occupation: Software Engineer
Referred By: None
Emergency Contact: Eva Walker Emergency Contact Phone: (906)334-8926
Describe your medical concerns (symptoms, diagnoses, etc):
Ranny nose, mucas in thwat, weakness,
aches, chills, tired
Are you currently taking any medication? (If yes, please describe):
Vyvanse (25mg) daily for attention.