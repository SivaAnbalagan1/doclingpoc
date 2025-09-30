---
license: apache-2.0
tags:
- mlx
language:
- en
base_model:
- ibm-granite/granite-docling-258M
pipeline_tag: image-text-to-text
library_name: transformers
---

# granite-docling-258M-mlx

<div style="display: flex; align-items: center;">
    <img src="https://huggingface.co/ibm-granite/granite-docling-258M/resolve/main/granite_docling.png" alt="Granite Docling Logo" style="width: 200px; height: auto; margin-right: 20px;">
    <div>
        <p>Granite Docling is a multimodal Image-Text-to-Text model engineered for efficient document conversion. It preserves the core features of Docling while maintaining seamless integration with <a href="https://docling-project.github.io/docling ">DoclingDocuments</a> to ensure full compatibility. </p>
    </div>
</div>


This model was converted to MLX format from [`ibm-granite/granite-docling-258M`](https://huggingface.co/ibm-granite/granite-docling-258M) using mlx-vlm version **0.3.3**.
Refer to the [original model card](https://huggingface.co/ibm-granite/granite-docling-258M) for more details on the model.

💡 This MLX model is optimized to run efficiently on Apple Silicon Macs.

## How to use this model with Docling

If you run through [🐥Docling](https://github.com/docling-project/docling), it will automatically choose the MLX version of the Granite-Docling model. 
You can select it with the CLI options shown below:

```sh
# Convert to HTML and Markdown:
docling --to html --to md --pipeline vlm --vlm-model granite_docling "https://arxiv.org/pdf/2501.17887" # accepts files, urls or directories

# Convert to HTML including layout visualization:
docling --to html_split_page --show-layout --pipeline vlm --vlm-model granite_docling "https://arxiv.org/pdf/2501.17887"
```

<p align="center">
<img src="https://huggingface.co/ibm-granite/granite-docling-258M/resolve/main/assets/granite_docling_split_page.png" alt="GraniteDocling result in split page view" width="900"/>
</p>

## How to use this model with bare mlx-vlm

You can also run plain mlx-vlm to generate predictions.

To run with the `mlx-vlm` CLI, use this command:

```sh
pip install mlx_vlm 
python -m mlx_vlm.generate --model ibm-granite/granite-docling-258M-mlx --max-tokens 4096 --temperature 0.0 --prompt "Convert this page to docling." --image <path_to_image>
```

To run with the `mlx-vlm` python SDK, parse the output as a `DoclingDocument` and export to various formats (e.g. Markdown, HTML), please refer to the code below.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "docling-core",
#     "mlx-vlm", 
#     "pillow",
#     "transformers",
# ]
# ///

import webbrowser
from pathlib import Path

from docling_core.types.doc import ImageRefMode
from docling_core.types.doc.document import DocTagsDocument, DoclingDocument
from mlx_vlm import load, stream_generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from transformers.image_utils import load_image

# Configuration
MODEL_PATH = "ibm-granite/granite-docling-258M-mlx"
PROMPT = "Convert this page to docling."
SHOW_IN_BROWSER = True

# Sample images (pick one...)
# SAMPLE_IMAGE = "https://huggingface.co/ibm-granite/granite-docling-258M/resolve/main/assets/new_arxiv.png"
# SAMPLE_IMAGE = "https://ibm.biz/docling-page-with-list"
SAMPLE_IMAGE = "https://ibm.biz/docling-page-with-table"

# Load model and processor
print("Loading model...")
model, processor = load(MODEL_PATH)
config = load_config(MODEL_PATH)

# Prepare input image and prompt
print("Preparing input...")
pil_image = load_image(SAMPLE_IMAGE)
formatted_prompt = apply_chat_template(processor, config, PROMPT, num_images=1)

# Generate DocTags output
print("Generating DocTags...\n")
output = ""
for token in stream_generate(
    model, processor, formatted_prompt, [pil_image], max_tokens=4096, verbose=False
):
    output += token.text
    print(token.text, end="")
    if "</doctag>" in token.text:
        break

print("\n\nProcessing output...")

# Create DoclingDocument from generated DocTags
doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([output], [pil_image])
doc = DoclingDocument.load_from_doctags(doctags_doc, document_name="Sample Document")

# Export to different formats
print("\nMarkdown output:\n")
print(doc.export_to_markdown())

# Save as HTML with embedded images
output_path = Path("./output.html") 
doc.save_as_html(output_path, image_mode=ImageRefMode.EMBEDDED)
print(f"\nHTML saved to: {output_path}")

# Open in browser
if SHOW_IN_BROWSER:
    webbrowser.open(f"file:///{str(output_path.resolve())}")    
```