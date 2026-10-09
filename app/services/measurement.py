from typing import List
import geopandas as gpd
from app.models import MeasurementInfo
from app.services.crs_transformer import reproject_to_projected_crs

def calculate_geospatial_measurements(gdf: gpd.GeoDataFrame) -> List[MeasurementInfo]:
    """
    Calculates projected measurements (Area for Polygons, Length for LineStrings).
    """
    projected_gdf, proj_crs_str = reproject_to_projected_crs(gdf)
    measurements: List[MeasurementInfo] = []

    for idx, row in projected_gdf.iterrows():
        geom = row.geometry
        feature_id = str(row.get("feature_id", idx))

        if geom is None or geom.is_empty:
            measurements.append(
                MeasurementInfo(
                    feature_id=feature_id,
                    geometry_type="None",
                    status="FAILED",
                    message="Empty or invalid geometry"
                )
            )
            continue

        geom_type = geom.geom_type

        if geom_type in ["Polygon", "MultiPolygon"]:
            area_m2 = float(geom.area)
            measurements.append(
                MeasurementInfo(
                    feature_id=feature_id,
                    geometry_type=geom_type,
                    area_sq_m=round(area_m2, 2),
                    area_sq_km=round(area_m2 / 1_000_000, 4),
                    projected_crs=proj_crs_str,
                    status="SUCCESS"
                )
            )

        elif geom_type in ["LineString", "MultiLineString"]:
            length_m = float(geom.length)
            measurements.append(
                MeasurementInfo(
                    feature_id=feature_id,
                    geometry_type=geom_type,
                    length_m=round(length_m, 2),
                    length_km=round(length_m / 1_000, 4),
                    projected_crs=proj_crs_str,
                    status="SUCCESS"
                )
            )

        elif geom_type in ["Point", "MultiPoint"]:
            measurements.append(
                MeasurementInfo(
                    feature_id=feature_id,
                    geometry_type=geom_type,
                    projected_crs=proj_crs_str,
                    status="SKIPPED",
                    message="Point geometry has no area or length metric."
                )
            )

        else:
            measurements.append(
                MeasurementInfo(
                    feature_id=feature_id,
                    geometry_type=geom_type,
                    status="UNSUPPORTED",
                    message=f"Measurement for geometry type '{geom_type}' is not supported."
                )
            )

    return measurements