import faiss
import numpy as np
import os
import json

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

        self.index_path = "faiss.index"
        self.metadata_path = "metadata.json"

        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        self.load()

    def add_vector(self, vector: list[float], metadata: dict):
        vector_array = np.array([vector], dtype="float32")

        self.index.add(vector_array)

        self.metadata.append(metadata)
        self.save()

    def save(self):
        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "w") as file:
            json.dump(self.metadata, file)


    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as file:
                self.metadata = json.load(file)
        print("Loaded FAISS vectors:", self.index.ntotal)
        print("Loaded metadata:", len(self.metadata))

    def search(self, query_vector: list[float], k: int = 3):
        query_array = np.array([query_vector], dtype="float32")

        actual_k = min(k, self.index.ntotal)

        if actual_k == 0:
            return [], []

        distances, indices = self.index.search(query_array, actual_k)

        results = []

        for index in indices[0]:
            if index != -1 and index < len(self.metadata):
                results.append(self.metadata[index])

        return distances[0], results

    def get_indexes_by_document(self, document_id: str):
        indexes = []

        for index, metadata in enumerate(self.metadata):
                if metadata["document_id"] == document_id:
                    indexes.append(index)

        return indexes



    def delete_document(self, document_id: str):
        indexes_to_delete = self.get_indexes_by_document(document_id)

        if not indexes_to_delete:
            return False

        remaining_vectors = []
        remaining_metadata = []

        for index, metadata in enumerate(self.metadata):
            if index not in indexes_to_delete:
                vector = self.index.reconstruct(index)

                remaining_vectors.append(vector)
                remaining_metadata.append(metadata)

        self.index = faiss.IndexFlatL2(self.index.d)

        if remaining_vectors:
            vectors_array = np.array(remaining_vectors, dtype="float32")
            self.index.add(vectors_array)

        self.metadata = remaining_metadata
        self.save()
        return True    