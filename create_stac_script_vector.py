import os
from datetime import datetime
import pystac
from shapely.geometry import shape, mapping
import fiona  # for reading GeoJSON

geojson_path = "/home/vishnu/corestack_STAC/data/gobindpur_swb3.geojson"

output_dir = "/home/vishnu/corestack_STAC/output_catalog"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

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

# Describe the catalog (prints basic info)
catalog.describe()

# Normalize HREFs and save catalog
catalog.normalize_hrefs(output_dir)
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

# Print the generated catalog and item JSON
print("\nCatalog JSON:")
with open(catalog.self_href) as f:
    print(f.read())

print("\nItem JSON:")
with open(item.self_href) as f:
    print(f.read())

print(f"\n✅ STAC catalog and item saved in: {output_dir}")

