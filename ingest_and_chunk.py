from unstructured.partition.pdf import partition_pdf

def ingest_and_chunk_by_title(filename, max_characters):
    elements = partition_pdf(
            filename=filename,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_output_dir="images",
            chunking_strategy="by_title",
            max_characters = max_characters
            )
    
    print("Number of elements:", len(elements))

def ingest_and_chunk_basic(filename, hardmax, softmax):
    elements = partition_pdf(
            filename=filename,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_output_dir="images",
            chunking_strategy="basic",
            new_after_n_chars = softmax,
            max_characters = hardmax
            )
    
    print("Number of elements:", len(elements))
