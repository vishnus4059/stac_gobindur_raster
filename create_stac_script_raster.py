import os
import json
import rasterio  # For reading raster metadata
from shapely.geometry import box, mapping
import pystac
from datetime import datetime

# Input raster file (GeoTIFF)
raster_path = "/home/vishnu/corestack_STAC/data/gobindpur_lulc_2023_2024.tif"

# Read raster to get bounding box
with rasterio.open(raster_path) as src:
    bounds = src.bounds
    bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
    geometry = mapping(box(*bbox))

# Create STAC Catalog
catalog = pystac.Catalog(
    id="gobindpur-lulc-catalog",
    description="Catalog for Gobindpur LULC 2023-24 GeoTIFF"
)

# Create STAC Item
item = pystac.Item(
    id="gobindpur-lulc",
    geometry=geometry,
    bbox=bbox,
    datetime=datetime.utcnow(),
    properties={}
)

# Add raster asset
item.add_asset(
    key="raster-data",
    asset=pystac.Asset(
        href=raster_path,
        media_type=pystac.MediaType.COG  # use MediaType.GEOTIFF if not Cloud-Optimized
    )
)

# Add item to catalog
catalog.add_item(item)

# Save to output directory (inside your repo)
output_dir = "/home/vishnu/corestack_STAC/output_catalog_lulc"
catalog.normalize_hrefs(output_dir)
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

print(f"\n✅ Catalog and item created successfully at: {output_dir}")
print(f"Root catalog: {os.path.join(output_dir, 'catalog.json')}")

