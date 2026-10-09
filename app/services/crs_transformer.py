import geopandas as gpd
from pyproj import CRS

def reproject_to_projected_crs(gdf: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, str]:
    """
    Ensures coordinates are in a projected CRS (meters).
    If geographic (e.g., EPSG:4326), reprojects to the optimal UTM zone CRS.
    """
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")

    crs_obj = CRS.from_user_input(gdf.crs)

    # Return as-is if already a projected CRS
    if not crs_obj.is_geographic:
        return gdf, gdf.crs.to_string()

    # Estimate best UTM zone for metric measurements
    utm_crs = gdf.estimate_utm_crs()
    projected_gdf = gdf.to_crs(utm_crs)
    
    return projected_gdf, utm_crs.to_string()