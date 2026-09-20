import os
import yaml
import zipfile
import cdsapi

# خواندن تنظیمات
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

url = os.environ.get("CDSAPI_URL", "https://cds.climate.copernicus.eu/api/v2")
key = os.environ.get("CDSAPI_KEY", "")

if not key:
    raise ValueError("کلید CDSAPI_KEY یافت نشد. لطفا Secrets گیت‌هاب را بررسی کنید.")

c = cdsapi.Client(url=url, key=key)

# دانلود داده CMIP6 برای استان فارس
output_filename = "fars_cmip6_data.zip"

print("شروع دریافت داده از کوپرنیکوس...")
c.retrieve(
    'projections-cmip6',
    {
        'format': 'zip',
        'temporal_resolution': 'monthly',
        'experiment': 'ssp2_4_5',
        'variable': 'near_surface_air_temperature',
        'model': 'ec_earth3',
        'area': config['area'], # [31.5, 50.5, 27.0, 55.5]
        'date': '2021-01-01/2030-12-31',
    },
    output_filename
)

print(f"دانلود با موفقیت انجام شد: {output_filename}")
