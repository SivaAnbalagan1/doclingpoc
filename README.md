# DoclingPOC

## Testing Docling

This project demonstrates how to use the Docling Python package to extract text and structured data from PDF documents.

### Usage

1. Place your PDF files in the `inputfiles` folder.
2. Run the script (e.g., `extractdocling.py`) to process the PDFs using Docling.
3. Extracted text and JSON results will be saved in the `outputfiles` folder.

### Requirements
- Python 3.8+
- `docling` Python package

### Example
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter(model_path="./models/docling-model")
result = converter.convert("inputfiles/sample.pdf")
text_output = result.document.export_to_text()
json_output = result.document.export_to_dict()

# Save outputs
with open("outputfiles/sample.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(text_output)

import json
with open("outputfiles/sample.json", "w", encoding="utf-8") as json_file:
    json.dump(json_output, json_file, ensure_ascii=False, indent=2)
```

### Notes
- Make sure the Docling model is downloaded and available locally for offline execution.
- Adjust the model path as needed for your environment.
