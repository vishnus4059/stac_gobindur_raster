import os
import json
import pystac
from datetime import datetime, timezone
from shapely.geometry import shape, mapping
from shapely.geometry.base import BaseGeometry

def get_geometry_and_bbox_from_geojson(geojson_path) -> (dict, list):
    """Read GeoJSON and extract geometry and bbox."""
    with open(geojson_path) as f:
        gj = json.load(f)

    # Assuming GeoJSON has either a FeatureCollection or a single Feature
    if gj['type'] == 'FeatureCollection':
        # Combine all features geometries into one unified geometry (optional)
        geometries = [shape(feature['geometry']) for feature in gj['features']]
        unified_geom = geometries[0]
        for geom in geometries[1:]:
            unified_geom = unified_geom.union(geom)
        geometry = mapping(unified_geom)
        bbox = list(unified_geom.bounds)  # (minx, miny, maxx, maxy)
    elif gj['type'] == 'Feature':
        geometry = gj['geometry']
        geom_shape = shape(geometry)
        bbox = list(geom_shape.bounds)
    else:
        raise ValueError(f"Unsupported GeoJSON type: {gj['type']}")

    return geometry, bbox


def main():
    geojson_path = '/home/vishnu/corestack_STAC/data/gobindpur_swb3.geojson'  # your geojson file path

    # Get geometry and bbox from geojson
    geometry, bbox = get_geometry_and_bbox_from_geojson(geojson_path)
    print("Geometry:", geometry)
    print("BBox:", bbox)

    datetime_utc = datetime.now(tz=timezone.utc)

    # Create catalog
    catalog = pystac.Catalog(
        id='gobindpur-catalog',
        description='STAC catalog for gobindpur_swb3 GeoJSON layer'
    )

    # Create item for the GeoJSON vector data
    item = pystac.Item(
        id='gobindpur_swb3',
        geometry=geometry,
        bbox=bbox,
        datetime=datetime_utc,
        properties={}
    )

    catalog.add_item(item)

    # Print catalog JSON
    print(json.dumps(catalog.to_dict(), indent=4))

    # Save catalog and item json files
    output_dir = 'stac_output_geojson'
    catalog.normalize_and_save(root_href=output_dir)
    print(f"Catalog saved to: {output_dir}")

if __name__ == '__main__':
    main()

