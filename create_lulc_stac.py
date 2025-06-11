import json
from pathlib import Path
from datetime import datetime
from shapely.geometry import shape
import pystac

geojson_path = Path("data/gobindpur_swb3.geojson")
output_dir = Path(".")

with open(geojson_path) as f:
    geojson = json.load(f)

geometry = geojson['features'][0]['geometry']
bbox = list(shape(geometry).bounds)

catalog = pystac.Catalog(
    id="lulc-catalog",
    description="STAC Catalog for LULC GeoJSON"
)

collection = pystac.Collection(
    id="lulc-collection",
    description="Collection for LULC data",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([bbox]),
        temporal=pystac.TemporalExtent([[datetime.utcnow(), None]])
    ),
    license="proprietary"
)

catalog.add_child(collection)

item = pystac.Item(
    id="lulc-item",
    geometry=geometry,
    bbox=bbox,
    datetime=datetime.utcnow(),
    properties={}
)

item.add_asset(
    "lulc-geojson",
    pystac.Asset(
        href=str(geojson_path),
        media_type="application/geo+json",
        roles=["data"],
        title="LULC GeoJSON Layer"
    )
)

collection.add_item(item)

catalog.normalize_and_save(str(output_dir), catalog_type=pystac.CatalogType.SELF_CONTAINED)

print("STAC Catalog, Collection, and Item created successfully.")

