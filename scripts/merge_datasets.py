"""
merge_datasets.py
-----------------
Merges monthly ERA5 wind and wave NetCDF files into single combined datasets.

Inputs : data/raw/era5_wave_YYYY_MM.nc  (one per month, 2014-01 to 2024-12)
         data/raw/era5_wind_YYYY_MM.nc  (one per month, 2014-01 to 2024-12)
Outputs: data/merged/era5_waves_2014_2024.nc
         data/merged/era5_wind_2014_2024.nc

Run from project root:
    python scripts/merge_datasets.py
"""

import glob
import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
RAW_DIR    = Path("data/raw")
MERGED_DIR = Path("data/merged")
MERGED_DIR.mkdir(parents=True, exist_ok=True)

WAVE_OUT = MERGED_DIR / "era5_waves_2014_2024.nc"
WIND_OUT = MERGED_DIR / "era5_wind_2014_2024.nc"

DATE_START = "2014-01"
DATE_END   = "2024-12"

# ── Helper functions ───────────────────────────────────────────────────────────

def collect_files(prefix: str) -> list[Path]:
    """
    Collect and sort all monthly files matching a given prefix.
    e.g. prefix='era5_wave' matches era5_wave_2014_01.nc, era5_wave_2014_02.nc ...
    """
    pattern = str(RAW_DIR / f"{prefix}_*.nc")
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(
            f"No files found matching: {pattern}\n"
            f"Check that RAW_DIR is correct and files follow the naming convention."
        )
    return [Path(f) for f in files]


def check_file_coverage(files: list[Path], prefix: str) -> None:
    """
    Verify all expected monthly files are present between DATE_START and DATE_END.
    Prints a warning for any missing months rather than crashing.
    """
    expected_months = pd.period_range(start=DATE_START, end=DATE_END, freq="M")
    found_months = set()

    for f in files:
        parts = f.stem.split("_")   # ['era5', 'wave', '2014', '01']
        try:
            year, month = int(parts[-2]), int(parts[-1])
            found_months.add(pd.Period(f"{year}-{month:02d}", freq="M"))
        except (ValueError, IndexError):
            print(f"  [WARN] Could not parse date from filename: {f.name}")

    missing = [str(m) for m in expected_months if m not in found_months]
    if missing:
        print(f"  [WARN] {prefix} — missing {len(missing)} month(s): {missing}")
    else:
        print(f"  [OK]   {prefix} — all {len(expected_months)} months present")


def merge_monthly_files(files: list[Path], label: str) -> xr.Dataset:
    """
    Open and concatenate monthly NetCDF files along the time dimension.
    Drops duplicate timestamps that can appear at month boundaries.
    """
    print(f"\n  Loading {len(files)} {label} files ...")
    ds = xr.open_mfdataset(
        files,
        combine="by_coords",
        chunks={"valid_time": 500},
        # Drop expver and number — expver changes across ERA5 versions and
        # blocks concatenation; number is an ensemble index not needed here
        drop_variables=["expver", "number"],
    )

    # Rename valid_time → time for consistency throughout the project
    if "valid_time" in ds.dims:
        ds = ds.rename({"valid_time": "time"})

    # Drop duplicate time steps at month seams
    _, unique_idx = np.unique(ds.time.values, return_index=True)
    if len(unique_idx) < len(ds.time):
        n_dupes = len(ds.time) - len(unique_idx)
        print(f"  [WARN] Dropping {n_dupes} duplicate time step(s)")
        ds = ds.isel(time=unique_idx)

    ds = ds.sortby("time")
    return ds


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  ERA5 Dataset Merger — Da Nang Wave Climate")
    print("=" * 55)

    # ── Wave data ──────────────────────────────────────────
    print("\n[1/2] Merging wave files ...")
    wave_files = collect_files("era5_wave")
    check_file_coverage(wave_files, "era5_wave")
    ds_wave = merge_monthly_files(wave_files, "wave")

    print(f"\n  Saving → {WAVE_OUT}")
    ds_wave.to_netcdf(WAVE_OUT)
    print("  Waves saved ✓")

    # ── Wind data ──────────────────────────────────────────
    print("\n[2/2] Merging wind files ...")
    wind_files = collect_files("era5_wind")
    check_file_coverage(wind_files, "era5_wind")
    ds_wind = merge_monthly_files(wind_files, "wind")

    print(f"\n  Saving → {WIND_OUT}")
    ds_wind.to_netcdf(WIND_OUT)
    print("  Wind saved ✓")

    print("\n" + "=" * 55)
    print("  Merge complete. Output files:")
    print(f"    {WAVE_OUT}")
    print(f"    {WIND_OUT}")
    print("=" * 55)


if __name__ == "__main__":
    main()