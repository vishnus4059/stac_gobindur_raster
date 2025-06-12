import os
import rasterio
from shapely.geometry import box, mapping
import pystac
from datetime import datetime

# === Input Paths (Static) ===
tif_path = "/home/vishnu/corestack_STAC/data/gobindpur_lulc_2023_2024.tif"
qgis_style_path = "/home/vishnu/corestack_STAC/data/style_file.qml"

# === Output Structure ===
output_dir = "/home/vishnu/corestack_STAC/output_catalog_lulc"
item_id = "gobindpur-lulc"
item_dir = os.path.join(output_dir, item_id)
os.makedirs(item_dir, exist_ok=True)

# === Step 1: Read Spatial Info from TIFF ===
with rasterio.open(tif_path) as src:
    bounds = src.bounds
    bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
    geometry = mapping(box(*bbox))

# === Step 2: Create Catalog ===
catalog = pystac.Catalog(
    id="gobindpur-lulc-catalog",
    description="STAC Catalog for Gobindpur LULC 2023-24 TIFF with QGIS Style"
)

# === Step 3: Create Item ===
item = pystac.Item(
    id=item_id,
    geometry=geometry,
    bbox=bbox,
    datetime=datetime.utcnow(),  # default datetime, may be updated below
    properties={}
)

# === Step 4: Add time range from TIFF metadata ===
with rasterio.open(tif_path) as src:
    meta_tags = src.tags()
    date_str = meta_tags.get("TIFFTAG_DATETIME")
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            item.properties["start_datetime"] = dt.isoformat() + "Z"
            item.properties["end_datetime"] = dt.isoformat() + "Z"
            item.datetime = dt
            print(f"📅 Temporal metadata added: {dt}")
        except Exception as e:
            print(f"❌ Failed to parse TIFFTAG_DATETIME: {e}")
    else:
        print("⚠️ No datetime info found in TIFF metadata.")

# === Step 5: Add Assets ===
item.add_asset(
    key="raster-data",
    asset=pystac.Asset(
        href="../../data/gobindpur_lulc_2023_2024.tif",
        media_type=pystac.MediaType.GEOTIFF,
        roles=["data", "download"],
        title="Gobindpur LULC Raster (GeoTIFF)"
    )
)

# Optional: Add QGIS style if available
if os.path.exists(qgis_style_path):
    item.add_asset(
        key="qgis-style",
        asset=pystac.Asset(
            href="../../data/style_file.qml",
            title="QGIS Style File (QML)",
            media_type="application/xml",
            roles=["style", "download"]
        )
    )
else:
    print("⚠️ QML file not found. Skipping style asset.")

# === Step 6: Save Catalog ===
catalog.add_item(item)
catalog.normalize_hrefs(output_dir)
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

# Rename item file to item_id.json
default_item_path = os.path.join(item_dir, "item.json")
custom_item_path = os.path.join(item_dir, f"{item_id}.json")
if os.path.exists(default_item_path):
    os.rename(default_item_path, custom_item_path)

# === Final Output ===
print("\n✅ STAC catalog created with external data reference!")
print(f"📄 catalog.json: {os.path.join(output_dir, 'catalog.json')}")
print(f"📄 item JSON: {custom_item_path}")
print(f"🗂️ Assets referenced from: ../../data/")

