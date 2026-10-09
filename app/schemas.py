from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.models import FileStatus, FeatureInfo, MeasurementInfo

class FileUploadResponse(BaseModel):
    id: str
    filename: str
    status: FileStatus
    message: str

class FileInfoResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    status: FileStatus
    feature_count: int
    crs: Optional[str]
    features: List[FeatureInfo]
    error: Optional[str]

class FileMeasurementsResponse(BaseModel):
    id: str
    filename: str
    status: FileStatus
    measurements: List[MeasurementInfo]