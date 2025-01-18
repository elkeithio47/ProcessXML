# Optimized and Updated Script

import os
from lxml import etree
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import uuid

# Constants
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "process_xml_collection"
EMBEDDING_MODEL = "intfloat/e5-small"
BATCH_SIZE = 100  # Number of points per batch for upserts

def load_xml_files(directory):
    """Loads all XML files from a specified directory."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                try:
                    tree = etree.parse(file_path)
                    documents.append({"file_path": file_path, "tree": tree})
                    print(f"Loaded XML file: {file_path}")
                except etree.XMLSyntaxError as e:
                    print(f"Error parsing XML file: {file_path}, {e}")
    print(f"Total XML files loaded: {len(documents)}")
    return documents

def chunk_xml_document(doc):
    """Chunks an XML document based on <stage> or <action> tags."""
    chunks = []
    file_path = doc["file_path"]
    tree = doc["tree"]

    for element in tree.xpath("//process | //subsheet"):
        element_name = element.tag
        element_id = element.get("subsheetid") or element.get("preferredid") or str(uuid.uuid4())
        for child in element.xpath("./stage | ./action"):
            child_text = ' '.join(child.xpath(".//text()"))
            if child_text:
                metadata = {
                    "file_path": file_path,
                    "element_name": element_name,
                    "element_id": element_id,
                    "child_name": child.get("name") or str(uuid.uuid4()),
                    "child_type": child.tag,
                }
                chunks.append({"text": child_text, "metadata": metadata})

    print(f"Chunked document '{file_path}' into {len(chunks)} chunks.")
    return chunks

def generate_embeddings(chunks, model):
    """Generates embeddings for the text chunks."""
    embeddings = []
    total_chunks = len(chunks)
    print(f"Starting embedding generation for {total_chunks} chunks...")

    for i, chunk in enumerate(chunks, start=1):
        text = chunk["text"]
        vector = model.encode(text).tolist()
        embeddings.append({"vector": vector, "metadata": chunk["metadata"]})
        if i % 10 == 0 or i == total_chunks:
            print(f"Processed {i}/{total_chunks} chunks.")

    print("Completed embedding generation.")
    return embeddings

def initialize_qdrant_client():
    """Initializes the Qdrant client."""
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def create_qdrant_collection(client, collection_name):
    """Creates a Qdrant collection if it doesn't exist."""
    try:
        client.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
        print(f"Created collection '{collection_name}'.")

def upsert_data_to_qdrant(client, collection_name, embeddings):
    """Upserts the data (embeddings and metadata) to the Qdrant vector store."""
    print(f"Upserting data in batches of {BATCH_SIZE}...")
    for i in range(0, len(embeddings), BATCH_SIZE):
        batch = embeddings[i:i + BATCH_SIZE]
        points = [
            models.PointStruct(id=index, vector=emb["vector"], payload=emb["metadata"])
            for index, emb in enumerate(batch, start=i)
        ]
        try:
            client.upsert(collection_name=collection_name, points=points)
            print(f"Upserted batch {i // BATCH_SIZE + 1}/{-(-len(embeddings) // BATCH_SIZE)}.")
        except Exception as e:
            print(f"Error upserting batch {i // BATCH_SIZE + 1}: {e}")

def main():
    xml_directory = "./xml_files"
    xml_documents = load_xml_files(xml_directory)
    if not xml_documents:
        print("No XML documents found. Exiting.")
        return

    all_chunks = []
    for doc in xml_documents:
        all_chunks.extend(chunk_xml_document(doc))

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = generate_embeddings(all_chunks, embedding_model)

    qdrant_client = initialize_qdrant_client()
    create_qdrant_collection(qdrant_client, COLLECTION_NAME)
    upsert_data_to_qdrant(qdrant_client, COLLECTION_NAME, embeddings)

if __name__ == "__main__":
    main()
