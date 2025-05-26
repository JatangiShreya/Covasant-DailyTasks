"""from multiple text files need to extract PII data using gemini model"""
import os
import re
import io
import csv
import requests
import pandas as pd
from typing import Optional, Literal, Tuple
from dotenv import load_dotenv
from docling.document_converter import DocumentConverter
load_dotenv()
def create_custom_prompt(system_prompt: str, document_text: str) -> str:
    """
    Creates a formatted prompt combining system prompt and document text.
    """
    return f"{system_prompt}\n\nUser: {document_text}\nAssistant:"
    
def extract_text_from_document(file_path: str) -> str:
    """
    Extract text from a document using docling.
    
    Args:
        file_path (str): Path to the document file
        
    Returns:
        str: Extracted text from the document
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
def process_ai_response(response: str) -> Tuple[str, pd.DataFrame]:
    """
    Process the AI model response to extract CSV data and convert to DataFrame.
    
    Args:
        response (str): The raw response from the AI model
        
    Returns:
        Tuple[str, pd.DataFrame]: The raw response and the DataFrame
    """
    csv_match = re.search(r'```csv\s*([\s\S]*?)\s*```', response)
    if not csv_match:
        print("Could not find CSV data in the response.")
        return response, pd.DataFrame()

    csv_content = csv_match.group(1).strip()
    f = io.StringIO(csv_content)
    reader = csv.reader(f, skipinitialspace=True)
    rows = list(reader)

    if not rows:
        return response, pd.DataFrame()

    header = rows[0]
    data = rows[1:]
    df = pd.DataFrame(data, columns=header)
    return response, df

def process_document_with_ai(system_prompt: str, file_path: str, model_type: Literal["llama3", "gpt4o", "gemini-1.5-flash"] = "llama3", api_key: Optional[str] = None) -> Tuple[str, pd.DataFrame]:
    """
    Extract text from a document using docling and process it with the specified AI model.
    
    Args:
        system_prompt (str): The system prompt that defines the AI's behavior
        file_path (str): Path to the document file to process
        model_type (str): The type of model to use ("llama3" or "gpt4o" or "gemini-1-chat")
        api_key (Optional[str]):GEMINI API key, required for gemini-1-chat 
    
    Returns:
        Tuple[str, pd.DataFrame]: The model's response and the extracted DataFrame
    """
    document_text = extract_text_from_document(file_path)
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    params = {"key": api_key}
    payload = {
        "model": model_type,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": document_text}
        ]
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        raise Exception(f"Gemini API Error: {response.status_code} {response.text}")
    result = response.json()
    raw_response = result["choices"][0]["message"]["content"]
    return process_ai_response(raw_response)
def main():
    system_prompt = """You are an NER model designed for PII (Personally Identifiable Information) extraction. Your task is to contextually detect entities belonging to the following labels:  
    [first_name, last_name, date, SSN, email, Phone_number, health_condition/diagnosis, account_number, address, credit-card-number]  
    ### **Output Format Guidelines:**
    - **Strict CSV Format**: Always wrap the output in a proper CSV format.
    - **Wrap Text With Commas**: If a field (e.g., address) contains a comma, wrap the entire value in double quotes (e.g., `"123 Main St, Springfield"`).
    - **Null for Missing Data**: If an entity is missing, output `"null"` instead of leaving it blank.
    - **No Extra Whitespace**: Strip unnecessary spaces from extracted entities.
    - **Consistent Column Order**: Maintain the exact order of labels for every output.
    - **Wrap Output Properly**: Always enclose the CSV output within triple backticks (` ```csv ... ``` `) to ensure correct parsing.
    ### **Example Output**
    ```csv
    first_name,last_name,date,SSN,email,Phone_number,health_condition/diagnosis,account_number,address,credit-card-number
    John,Doe,null,123-45-6789,john.doe@example.com,null,null,null,null,null
    ``"""
    print("=== Document PII Extraction ===\n")
    print("1. Process a document file")
    print("2. Process all documents in a folder")
    print("3. Exit")
    print("Select AI model: ")
    print("1. Gemini")
    model_choice = input("Enter your choice (1) for model selection:")
    if model_choice == "1":
        model_type = "gemini-1.5-flash"
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
            api_key = input("Enter your OpenAI API key manually: ")
    while True:
        choice = input("\nEnter your choice (1-3) from above options: ")
        if choice == "1":
            file_path = input("Enter the path to the document file: ")
            try:
                raw_response, df = process_document_with_ai(system_prompt, file_path, model_type, api_key)
                print("\nRaw Extracted PII Data:\n", raw_response)
                if not df.empty:
                    print("\nExtracted Data as DataFrame:")
                    print(df)
                    save_option = input("\nDo you want to save this data to a CSV file? (y/n): ")
                    if save_option.lower() == 'y':
                        output_path = input("Enter the output file path (e.g., extracted_data.csv): ")
                        df.to_csv(output_path, index=False,quoting=csv.QUOTE_ALL,encoding='utf-8')
                        print(f"Data saved ")
                else:
                    print("\nCould not parse the response into a DataFrame. Check the raw output above.")
            except Exception as e:
                print(f"Error: {e}") 
        elif choice == "2":
            folder_path = input("Enter the folder path containing documents: ")
            combined_df = pd.DataFrame()
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if not os.path.isfile(file_path):
                    continue 
                try:
                    print(f"\nProcessing file: {filename}")
                    raw_response, df = process_document_with_ai(system_prompt, file_path, model_type, api_key)
                    if not df.empty:
                        combined_df = pd.concat([combined_df, df], ignore_index=False)
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")
            if not combined_df.empty:
                print("\nCombined DataFrame from all documents:")
                print(combined_df)
                save_path = input("\nEnter filename to save combined data (e.g., all_pii_data.csv): ")
                combined_df.to_csv(save_path, index=False)
                print(f"Data saved")
            else:
                print("No valid PII data was extracted from any files.")
        elif choice == "3":
            print("Exiting program.")
            break    
        else:
            print("Invalid choice. Please enter 1, 3.")
if __name__ == "__main__":
    main()
            
