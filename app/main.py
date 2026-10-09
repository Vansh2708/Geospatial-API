import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, status
import shapely.geometry

from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS
from app.models import FileMetadata, FileStatus, FeatureInfo
from app.schemas import FileUploadResponse, FileInfoResponse, FileMeasurementsResponse
from app.storage import save_file_metadata, get_file_metadata
from app.services.file_parser import parse_geospatial_file
from app.services.measurement import calculate_geospatial_measurements

app = FastAPI(
    title="Geospatial File Measurement API",
    description="API for extracting features and calculating projected measurements from Shapefiles (.zip) and KML files.",
    version="1.0.0"
)

@app.post("/api/files/", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file extension. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    metadata = FileMetadata(filename=file.filename, file_type=file_ext)
    saved_path = UPLOAD_DIR / f"{metadata.id}{file_ext}"

    try:
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Parse vector data using GeoPandas
        gdf = parse_geospatial_file(saved_path, file.filename)

        metadata.feature_count = len(gdf)
        metadata.crs = gdf.crs.to_string() if gdf.crs else "EPSG:4326"

        # Build feature list for JSON serialization
        features_list = []
        for idx, row in gdf.iterrows():
            # Conversion to GeoJSON dict via shapely.geometry.mapping
            if row.geometry and not row.geometry.is_empty:
                geom_geojson = shapely.geometry.mapping(row.geometry)
            else:
                geom_geojson = {}
            
            # Clean feature properties for JSON
            props = row.drop(["geometry"]).to_dict()
            props = {k: str(v) for k, v in props.items()}

            features_list.append(
                FeatureInfo(
                    feature_id=str(row.get("feature_id", idx)),
                    geometry_type=row.geometry.geom_type if row.geometry else "Unknown",
                    geometry=geom_geojson,
                    crs=metadata.crs,
                    properties=props
                )
            )

        metadata.features = features_list

        # Calculate geospatial measurements
        metadata.measurements = calculate_geospatial_measurements(gdf)
        metadata.status = FileStatus.COMPLETED

    except Exception as e:
        metadata.status = FileStatus.FAILED
        metadata.error = str(e)
        save_file_metadata(metadata)
        raise HTTPException(status_code=422, detail=f"File processing failed: {str(e)}")

    save_file_metadata(metadata)

    return FileUploadResponse(
        id=metadata.id,
        filename=metadata.filename,
        status=metadata.status,
        message="File processed and measurements calculated successfully."
    )

@app.get("/api/files/{file_id}", response_model=FileInfoResponse)
async def get_file_info(file_id: str):
    metadata = get_file_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File metadata not found.")
    return metadata

@app.get("/api/files/{file_id}/measurements", response_model=FileMeasurementsResponse)
async def get_file_measurements(file_id: str):
    metadata = get_file_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File metadata not found.")
    return metadata