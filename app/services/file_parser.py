import zipfile
import tempfile
from pathlib import Path
import geopandas as gpd
import fiona

# Enable KML driver support in Fiona
fiona.drvsupport.supported_drivers['KML'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

def parse_geospatial_file(file_path: Path, filename: str) -> gpd.GeoDataFrame:
    """
    Parses zipped Shapefiles or KML files into a GeoPandas GeoDataFrame.
    """
    ext = file_path.suffix.lower()

    if ext == ".zip":
        with tempfile.TemporaryDirectory() as tmp_dir:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir)

            shp_files = list(Path(tmp_dir).rglob("*.shp"))
            if not shp_files:
                raise ValueError("No .shp file found inside the uploaded zip archive.")
            
            gdf = gpd.read_file(shp_files[0])

    elif ext == ".kml":
        try:
            gdf = gpd.read_file(file_path, driver="KML")
        except Exception:
            gdf = gpd.read_file(file_path, driver="LIBKML")
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    if "feature_id" not in gdf.columns:
        gdf["feature_id"] = [str(i) for i in range(len(gdf))]

    return gdf