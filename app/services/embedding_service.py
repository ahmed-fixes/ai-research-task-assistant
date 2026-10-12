from pathlib import Path

from sentence_transformers import SentenceTransformer

CACHE_DIR = (
Path.home()
/ ".cache"
/ "huggingface"
/ "hub"
/ "models--sentence-transformers--all-MiniLM-L6-v2"
/ "snapshots"
)

snapshot_folders = [
folder
for folder in CACHE_DIR.iterdir()
if folder.is_dir()
]

if not snapshot_folders:
    raise FileNotFoundError(
    "all-MiniLM-L6-v2 model was not found in the Hugging Face cache."
    )

MODEL_PATH = snapshot_folders[0]

model = SentenceTransformer(
str(MODEL_PATH),
local_files_only=True
)

def generate_embedding(text: str) -> list[float]:

    
    embedding = model.encode(text)

    return embedding.tolist()
