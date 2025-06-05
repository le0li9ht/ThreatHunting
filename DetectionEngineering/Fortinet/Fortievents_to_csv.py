import fitz  # PyMuPDF
import csv
import re

def extract_log_details(pdf_path):
    extracted_data = []
    accumulated_text = ""  # Stores text of two pages at a time

    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        num_pages = len(doc)
        
        for i in range(0, num_pages, 2):  # Read two pages at a time
            page_text = ""

            for j in range(2):  # Read the next two pages
                if i + j < num_pages:
                    text = doc[i + j].get_text("text") or " ".join(block[4] for block in doc[i + j].get_text("blocks"))
                    page_text += text + "\n"
            
            accumulated_text += page_text  # Add new pages to existing text
            
            # Look for starting condition (new Message ID)
            while True:
                match = re.search(r"Message ID:\s*(\d+)", accumulated_text)
                if not match:
                    break  # No more new entries in current text
                
                start_index = match.start()  # Start of the log entry
                log_text = accumulated_text[start_index:]  # Cut from new Message ID onwards
                
                # Extract log details
                message_id = re.search(r"Message ID:\s*(\d+)", log_text)
                message_desc = re.search(r"Message Description:\s*([\w_]+)", log_text)
                message_meaning = re.search(r"Message Meaning:\s*(.+)", log_text)
                log_type = re.search(r"Type:\s*(\w+)", log_text)
                category = re.search(r"Category:\s*(\w+)", log_text)
                severity = re.search(r"Severity:\s*(\w+)", log_text)

                # Ensure all fields are found before storing
                if message_id and message_desc and message_meaning and log_type and category and severity:
                    extracted_data.append([
                        message_id.group(1),
                        message_desc.group(1),
                        message_meaning.group(1),
                        log_type.group(1),
                        category.group(1),
                        severity.group(1),
                    ])

                    # Remove processed part from accumulated text
                    accumulated_text = accumulated_text[match.end():]

                else:
                    break  # Wait for next pages to fill missing data

    return extracted_data

# Function to save extracted data to a CSV file
def save_to_csv(data, output_csv):
    headers = ["Message ID", "Message Description", "Message Meaning", "Type", "Category", "Severity"]

    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Example usage
pdf_path = input("Enter the path to the FortiOS Log Reference Guide PDF file: ")#"FortiOS_7.6.2_Log_Reference.pdf"  # Change this to your actual PDF file path
output_csv = input("Output csv file path: ")

log_data = extract_log_details(pdf_path)
if log_data:
    save_to_csv(log_data, output_csv)
    print(f"Data extracted and saved to {output_csv}")
else:
    print("No relevant data found in the PDF.")

