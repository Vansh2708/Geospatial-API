# Geospatial File Measurement API

A production-ready FastAPI application designed to parse vector geospatial files (Zipped Shapefiles `.zip` and Keyhole Markup Language `.kml`), extract feature geometries and metadata, and calculate projected spatial measurements (Area in $m^2$/$km^2$ for Polygons; Length in $m$/$km$ for LineStrings).

The API handles coordinate system detection and automatically reprojects geographic coordinate reference systems (e.g., `EPSG:4326`) into the optimal local UTM zone for accurate metric measurements.

---

## Key Features

- **Multi-Format Vector Support:** Parses `.kml` files and `.zip` archives containing ESRI Shapefile components (`.shp`, `.shx`, `.dbf`, `.prj`).
- **Dynamic Reprojection Engine:** Automatically detects geographic coordinate reference systems and calculates the optimal UTM (Universal Transverse Mercator) zone based on geometry centroids for accurate metric distance and area calculations.
- **Robust Feature Parsing:** Converts complex Shapely geometries into GeoJSON-compliant structures with cleaned feature attributes.
- **Graceful Geometry Handling:** Explicitly supports `Polygon`, `MultiPolygon`, `LineString`, and `MultiLineString`, while gracefully handling non-measurable types (`Point`, `MultiPoint`) without throwing application errors.
- **In-Memory Metadata Persistence:** Retains uploaded file status, parsed features, and calculated metrics across API sessions.

---

## Project Structure

```text
Geospatial-API/
├── app/
│   ├── __init__.py
│   ├── config.py           # Application settings & constants
│   ├── main.py             # FastAPI entry point & API route handlers
│   ├── models.py           # Core Pydantic data models & Enums
│   ├── schemas.py          # Request and Response schemas
│   ├── storage.py          # In-memory metadata storage layer
│   └── services/
│       ├── __init__.py
│       ├── crs_transformer.py  # UTM zone estimation & reprojection
│       ├── file_parser.py      # Zip/KML parsing via GeoPandas & Fiona
│       └── measurement.py     # Area and length metric calculations
├── uploads/                # Temporary disk storage for uploaded files
├── environment.yml         # Conda environment definition
├── requirements.txt        # Pip dependencies reference
└── README.md

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd Geospatial-API
   ```

2. **Create and activate the Conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate geo_env
   ```

3. **Run the FastAPI server:**
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

4. **Access API Documentation:**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.
