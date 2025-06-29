from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import OCR_AGENT_PADDLE

file_path = "./documents"
base_file_name = "layout-parser-paper"

def main():
    paddle_elements = partition_pdf(
        filename=f"{file_path}/{base_file_name}.pdf",
        strategy="hi_res",
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True,
        ocr_agent=OCR_AGENT_PADDLE,
        )

    tesseract_elements = partition_pdf(
        filename=f"{file_path}/{base_file_name}.pdf",
        strategy="hi_res",
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True,
        )

    # put in json for comparison
    for paddle_element, tesseract_element in zip(paddle_elements, tesseract_elements):
        if paddle_element.text != tesseract_element.text:
            print(f"paddle: {paddle_element.text}")
            print(f"tesseract: {tesseract_element.text}")
            print("-------------")

if __name__ == "__main__":
    main()