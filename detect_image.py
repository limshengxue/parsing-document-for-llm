from unstructured.partition.pdf import partition_pdf

def detect_image(filename):
    elements = partition_pdf(
            filename=filename,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            )
    
    print("Number of elements:", len(elements))

    # extract image to payload will not work with chunking including basic/by_title

    for element in elements:
        if element.metadata.image_base64 is not None:
            print("Page", element.metadata.page_number, "has image")