from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
import os
import dotenv
from unstructured.partition.utils.constants import OCR_AGENT_PADDLE
from unstructured_inference.models.base import get_model
from unstructured_inference.inference.layout import DocumentLayout
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage
from langchain.schema.document import Document
from pydantic import BaseModel
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec, Pinecone

dotenv.load_dotenv()

file_path = "./documents"
base_file_name = "layout-parser-paper"

class ProcessedElement(BaseModel):
    text: str
    document_source: str
    page: int

def main():
    elements = partition_pdf(
        filename=f"{file_path}/{base_file_name}.pdf",
        strategy="hi_res",
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True,
        )

    print("Number of elements:", len(elements))

    processed_elements = process_elements(elements)

    docs = elements_to_langchain_docs_chunk_by_page(processed_elements)

    store_docs_into_vectorstore(docs)

def store_docs_into_vectorstore(docs):
    index_name = "my-docs"
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


    if not pc.has_index(index_name):
            pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    vectorstore = PineconeVectorStore.from_documents(index_name=index_name, 
                                                     documents=docs,
                                                          embedding=OpenAIEmbeddings(
                                                              api_key=os.getenv("OPENAI_API_KEY")))

def elements_to_langchain_docs_chunk_by_page(elements):
    prev_page = -1
    content = ""
    docs = []
    for processed_element in elements:
        if prev_page != processed_element.page and prev_page != -1:
            new_document = Document(page_content=content, metadata={"page": prev_page, "source": f"{file_path}/{base_file_name}.pdf"})
            docs.append(new_document)
            content = ""

        content += processed_element.text
        prev_page = processed_element.page


    # store the last element
    if prev_page != -1 and content != "":
        new_document = Document(page_content=content, metadata={"page": prev_page, "source": f"{file_path}/{base_file_name}.pdf"})
        docs.append(new_document)
    
    return docs    
    
def process_elements(elements):
    processed_elements = [] 

    for element in elements:
        text_content = element.text
        if element.metadata.image_base64 != None:
            print("Processing image on page", element.metadata.page_number)
            image_content = understand_image(element.metadata.image_base64)
            print(image_content)
            print(" -----------") 
            text_content += image_content

        processed_elements.append(
            ProcessedElement(
                text=text_content,
                document_source=f"{file_path}/{base_file_name}.pdf",
                page=element.metadata.page_number
            )
        )
    
    return processed_elements

def understand_image(base64_image):
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    # Create the image payload for GPT-4o
    image_message = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/png;base64,{base64_image}"
        }
    }

    # Compose the message with text + image
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": "Please describe the image, if the image is purely text please perform OCR (Optical Character Recognition). Return only the content without extra wording"},
                image_message
            ]
        )
    ]

    response = llm.invoke(messages)

    return response.content
    

if __name__ == "__main__":
    main()