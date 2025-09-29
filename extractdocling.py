import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["DOCLING_SERVE_ARTIFACTS_PATH"] = "./docling/models"
os.environ["HF_HOME"] = "./docling/models"
os.environ["HF_HUB_CACHE"] = "./docling/models"
# os.environ["TRANSFORMERS_OFFLINE"] = "0"
# os.environ["HF_DATASETS_OFFLINE"] = "0"

from docling.document_converter import DocumentConverter


input_folder = "./inputfiles"
output_folder = "./outputfiles"

def process_pdfs_with_docling(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    converter = DocumentConverter()
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            result = converter.convert(input_path)
            # Export to plain text
            text_output = result.document.export_to_text()
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(output_folder, txt_filename)
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text_output)
            print(f"Saved Text: {txt_path}")
            # Export to JSON
            json_output = result.document.export_to_dict()
            json_filename = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(output_folder, json_filename)            
            import json
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(json_output, json_file, ensure_ascii=False, indent=2)
            print(f"Saved JSON: {json_path}")

if __name__ == "__main__":
    process_pdfs_with_docling(input_folder, output_folder)
