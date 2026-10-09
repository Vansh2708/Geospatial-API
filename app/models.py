import uuid
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class FileStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class FeatureInfo(BaseModel):
    feature_id: str
    geometry_type: str
    geometry: Dict[str, Any]
    crs: str
    properties: Dict[str, Any]

class MeasurementInfo(BaseModel):
    feature_id: str
    geometry_type: str
    status: str
    area_sq_m: Optional[float] = None
    area_sq_km: Optional[float] = None
    length_m: Optional[float] = None
    length_km: Optional[float] = None
    projected_crs: Optional[str] = None
    message: Optional[str] = None

class FileMetadata(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_type: str
    status: FileStatus = FileStatus.PENDING
    feature_count: int = 0
    crs: Optional[str] = None
    error: Optional[str] = None
    features: List[FeatureInfo] = []
    measurements: List[MeasurementInfo] = []