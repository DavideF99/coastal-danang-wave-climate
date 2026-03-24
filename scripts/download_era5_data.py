# download_era5_danang.py
import cdsapi
from pathlib import Path

client = cdsapi.Client()

# ── Configuration ──────────────────────────────────────────────
YEARS   = [str(y) for y in range(2014, 2025)]
MONTHS  = [f"{m:02d}" for m in range(1, 13)]
DAYS    = [f"{d:02d}" for d in range(1, 32)]
HOURS   = [f"{h:02d}:00" for h in range(24)]
AREA    = [17, 107, 15, 109]   # N, W, S, E

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# ───────────────────────────────────────────────────────────────

total   = len(YEARS) * len(MONTHS)
current = 0

for year in YEARS:
    for month in MONTHS:
        current += 1
        tag = f"{year}-{month}"
        print(f"\n[{current}/{total}]  Processing {tag}")

        # ── 1. Wave variables ──────────────────────────────────
        wave_out = OUTPUT_DIR / f"era5_wave_{year}_{month}.nc"
        if wave_out.exists():
            print(f"  ⏭  Wave {tag} already exists, skipping.")
        else:
            print(f"  🌊  Fetching wave data for {tag}…")
            client.retrieve(
                "reanalysis-era5-single-levels",
                {
                    "product_type": "reanalysis",
                    "variable": [
                        "significant_height_of_combined_wind_waves_and_swell",
                        "mean_wave_period",
                        "mean_wave_direction",
                    ],
                    "year":  year,
                    "month": month,
                    "day":   DAYS,
                    "time":  HOURS,
                    "area":  AREA,
                    "format": "netcdf",
                },
                str(wave_out),
            )
            print(f"  ✅  Saved {wave_out.name}")

        # ── 2. Wind variables ──────────────────────────────────
        wind_out = OUTPUT_DIR / f"era5_wind_{year}_{month}.nc"
        if wind_out.exists():
            print(f"  ⏭  Wind {tag} already exists, skipping.")
        else:
            print(f"  💨  Fetching wind data for {tag}…")
            client.retrieve(
                "reanalysis-era5-single-levels",
                {
                    "product_type": "reanalysis",
                    "variable": [
                        "10m_u_component_of_wind",
                        "10m_v_component_of_wind",
                    ],
                    "year":  year,
                    "month": month,
                    "day":   DAYS,
                    "time":  HOURS,
                    "area":  AREA,
                    "format": "netcdf",
                },
                str(wind_out),
            )
            print(f"  ✅  Saved {wind_out.name}")

print("\n🎉  All downloads complete.")