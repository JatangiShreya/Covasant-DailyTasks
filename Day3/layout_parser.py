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
