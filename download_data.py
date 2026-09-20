import os
import yaml
import cdsapi

def load_config(config_path="config.yaml"):
    """خواندن تنظیمات محدوده فارس و مدل‌ها"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_model_grid(config, model_name):
    """پیدا کردن نوع گرید مربوط به هر مدل"""
    for item in config["models"]:
        if item["name"] == model_name:
            return item["grid"]
    raise ValueError(f"مدل '{model_name}' در تنظیمات تعریف نشده است.")

def main():
    config = load_config()

    # خواندن کلید و آدرس API از متغیرهای محیطی
    cds_url = os.environ.get("CDSAPI_URL", "https://cds.climate.copernicus.eu/api")
    cds_key = os.environ.get("CDSAPI_KEY")

    if not cds_key:
        print("❌ خطا: متغیر CDSAPI_KEY تنظیم نشده است!")
        print("لطفاً کلید خود را به عنوان متغیر محیطی تنظیم کنید.")
        return

    # انتخاب مدل (پیش‌فرض: EC-Earth3)
    # گزینه‌ها: EC-Earth3 یا MPI-ESM1-2-HR یا NorESM2-MM
    chosen_model = os.environ.get("SELECTED_MODEL", "EC-Earth3")
    grid_type = get_model_grid(config, chosen_model)

    print(f"🚀 شروع دانلود برای استان فارس با مدل: {chosen_model}")
    print(f"📍 محدوده مختصات فارس: {config['bounding_box']}")

    client = cdsapi.Client(url=cds_url, key=cds_key)

    for scenario in config["scenarios"]:
        output_filename = f"fars_{chosen_model}_{scenario}.zip"
        print(f"\n📦 ارسال درخواست برای سناریو: {scenario} ...")

        request_params = {
            "temporal_resolution": "monthly",
            "experiment": scenario,
            "level": "single_levels",
            "variable": config["variables"],
            "model": chosen_model,
            "grid": grid_type,
            "year": ["2030", "2050", "2080"],
            "month": ["01", "04", "07", "10"],
            "area": config["bounding_box"],  # [North, West, South, East]
            "format": "zip",
        }

        try:
            client.retrieve("projections-cmip6", request_params).download(output_filename)
            print(f"✅ فایل ذخیره شد: {output_filename}")
        except Exception as e:
            print(f"⚠️ خطا در دانلود سناریو {scenario}: {e}")

if __name__ == "__main__":
    main()
