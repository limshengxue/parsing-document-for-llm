from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
import os
import dotenv

from unstructured_inference.models.base import get_model
from unstructured_inference.inference.layout import DocumentLayout

model = get_model("yolox")

dotenv.load_dotenv()

file_path = "./documents"
base_file_name = "layout-parser-paper"

def main():
    elements = partition_pdf(
        filename=f"{file_path}/{base_file_name}.pdf",
        strategy="hi_res",
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True,
        max_characters=6000,
        new_after_n_chars=6000,
        )

    print("Number of elements:", len(elements))
    for element in elements:
        if element.metadata.image_base64 is not None:
            print("Page", element.metadata.page_number, "has image")

if __name__ == "__main__":
    main()