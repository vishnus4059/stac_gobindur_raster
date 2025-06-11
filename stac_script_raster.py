import os
import rasterio
from shapely.geometry import box, mapping
import pystac
from datetime import datetime

# === Input and Output Paths ===
tif_path = "/home/vishnu/corestack_STAC/data/gobindpur_lulc_2023_2024.tif"
qgis_style = "/home/vishnu/corestack_STAC/data/style_file.qml"
output_dir = "/home/vishnu/corestack_STAC/output_catalog_lulc"

# === Step 1: Extract Spatial Info ===
with rasterio.open(tif_path) as src:
    bounds = src.bounds
    bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
    geometry = mapping(box(*bbox))

# === Step 2: Create STAC Catalog ===
catalog = pystac.Catalog(
    id="gobindpur-lulc-catalog",
    description="Catalog for Gobindpur LULC 2023-24 TIFF + QGIS Style"
)

# === Step 3: Create STAC Item ===
item = pystac.Item(
    id="gobindpur-lulc",
    geometry=geometry,
    bbox=bbox,
    datetime=datetime.utcnow(),
    properties={}
)

# === Step 4: Add TIFF Asset ===
item.add_asset(
    key="raster-data",
    asset=pystac.Asset(
        href="data/gobindpur_lulc_2023_2024.tif",
        media_type=pystac.MediaType.GEOTIFF,
        roles=["data"],
        title="LULC Raster (GeoTIFF)"
    )
)

# === Step 5: Add QGIS Style Asset (optional) ===
if os.path.exists(qgis_style):
    item.add_asset(
        key="qgis-style",
        asset=pystac.Asset(
            href="data/style_file.qml.qml",
            title="QGIS Style (QML)",
            media_type="application/xml",
            roles=["style"]
        )
    )
else:
    print("⚠️ QGIS style file not found, skipping style asset.")

# === Step 6: Finalize Catalog ===
catalog.add_item(item)
catalog.normalize_hrefs(output_dir)
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

print("\n✅ STAC Catalog created successfully!")
print(f"📂 Location: {output_dir}")
print(f"📄 Root catalog: {os.path.join(output_dir, 'catalog.json')}")
