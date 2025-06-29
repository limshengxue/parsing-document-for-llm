from unstructured.partition.pdf import partition_pdf

def detect_image(filename):
    elements = partition_pdf(
            filename=filename,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            max_characters=1000,
            new_after_n_chars=200,
            )

    print("Number of elements:", len(elements))
    for element in elements:
        if element.metadata.image_base64 is not None:
            print("Page", element.metadata.page_number, "has image")