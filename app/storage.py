from typing import Dict, Optional
from app.models import FileMetadata

# In-memory storage for file metadata
_STORAGE: Dict[str, FileMetadata] = {}

def save_file_metadata(metadata: FileMetadata) -> None:
    _STORAGE[metadata.id] = metadata

def get_file_metadata(file_id: str) -> Optional[FileMetadata]:
    return _STORAGE.get(file_id)