import os
import json
import tempfile
from datetime import datetime
import pystac
from shapely.geometry import shape, mapping
import fiona  # for reading GeoJSON

# Input vector file path (GeoJSON)
geojson_path = "/home/vishnu/corestack_STAC/data/gobindpur_swb3.geojson"

# Read geometry from GeoJSON
with fiona.open(geojson_path, "r") as src:
    geom = shape(src[0]['geometry'])
    bbox = list(geom.bounds)
    geometry = mapping(geom)

# Create STAC Catalog
catalog = pystac.Catalog(id="gobindpur-catalog", description="Catalog for Gobindpur SWB3 GeoJSON")

# Create STAC Item
item = pystac.Item(
    id="gobindpur-geojson",
    geometry=geometry,
    bbox=bbox,
    datetime=datetime.utcnow(),
    properties={}
)

# Add Asset (the GeoJSON itself)
item.add_asset(
    key="vector-data",
    asset=pystac.Asset(
        href=geojson_path,
        media_type=pystac.MediaType.GEOJSON
    )
)

# Add item to catalog
catalog.add_item(item)

# Visualize catalog hierarchy
catalog.describe()

# Save the catalog to a temporary directory
tmp_dir = tempfile.TemporaryDirectory()
catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

# Print the generated catalog and item JSON
print("\nCatalog JSON:")
with open(catalog.self_href) as f:
    print(f.read())

print("\nItem JSON:")
with open(item.self_href) as f:
    print(f.read())

# Cleanup temp directory (optional if you want to keep output)
# tmp_dir.cleanup()

