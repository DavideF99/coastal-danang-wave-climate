"""
validate_merged_data.py
-----------------------
Validation checks for the merged ERA5 wind and wave datasets.
Run this after merge_datasets.py to confirm the outputs are complete and physically sensible.

Run from project root:
    python tests/validate_merged_data.py
"""

import sys
import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
MERGED_DIR = Path("data/merged")
WAVE_FILE  = MERGED_DIR / "era5_waves_2014_2024.nc"
WIND_FILE  = MERGED_DIR / "era5_wind_2014_2024.nc"

# Expected values
DATE_START     = "2014-01-01 00:00"
DATE_END       = "2024-12-31 23:00"
EXPECTED_STEPS = int(pd.date_range(DATE_START, DATE_END, freq="h").size)  # 96,432
LAT_BOUNDS     = (15.0, 17.0)   # ERA5 domain
LON_BOUNDS     = (107.0, 109.0)
MAX_SWH        = 20.0           # m  — physical upper limit for SCS
MAX_WIND       = 80.0           # m/s — physical upper limit

# ── Validation functions ───────────────────────────────────────────────────────

def check_file_exists(path: Path) -> bool:
    if not path.exists():
        print(f"  [FAIL] File not found: {path}")
        return False
    print(f"  [OK]   Found: {path}")
    return True


def check_time_coverage(ds: xr.Dataset) -> bool:
    """Check time range, total step count and gaps > 1 hour."""
    passed = True

    t_start = pd.Timestamp(ds.time.values[0])
    t_end   = pd.Timestamp(ds.time.values[-1])
    n_steps = len(ds.time)

    print(f"  Time range  : {t_start.strftime('%Y-%m-%d %H:%M')}  →  "
          f"{t_end.strftime('%Y-%m-%d %H:%M')}")

    # Step count
    if n_steps == EXPECTED_STEPS:
        print(f"  Step count  : {n_steps:,} ✓")
    else:
        diff = EXPECTED_STEPS - n_steps
        print(f"  [WARN] Step count {n_steps:,} differs from expected "
              f"{EXPECTED_STEPS:,} by {diff:,} steps")
        passed = False

    # Time gaps
    deltas = np.diff(ds.time.values).astype("timedelta64[h]").astype(int)
    gaps   = np.where(deltas > 1)[0]
    if len(gaps) == 0:
        print(f"  Time gaps   : none ✓")
    else:
        print(f"  [WARN] {len(gaps)} gap(s) > 1 hour:")
        for g in gaps[:5]:
            t = pd.Timestamp(ds.time.values[g])
            print(f"           after {t.strftime('%Y-%m-%d %H:%M')} "
                  f"({deltas[g]}h gap)")
        passed = False

    return passed


def check_spatial_domain(ds: xr.Dataset) -> bool:
    """Check lat/lon bounds match the expected ERA5 domain."""
    passed = True

    lat_min, lat_max = float(ds.latitude.min()), float(ds.latitude.max())
    lon_min, lon_max = float(ds.longitude.min()), float(ds.longitude.max())

    print(f"  Lat range   : {lat_min:.2f}°N  →  {lat_max:.2f}°N")
    print(f"  Lon range   : {lon_min:.2f}°E  →  {lon_max:.2f}°E")

    if lat_min > LAT_BOUNDS[0] or lat_max < LAT_BOUNDS[1]:
        print(f"  [WARN] Lat range outside expected {LAT_BOUNDS}")
        passed = False
    if lon_min > LON_BOUNDS[0] or lon_max < LON_BOUNDS[1]:
        print(f"  [WARN] Lon range outside expected {LON_BOUNDS}")
        passed = False

    if passed:
        print(f"  Spatial domain ✓")

    return passed


def check_variables(ds: xr.Dataset, is_wave: bool = False) -> bool:
    """Per-variable NaN percentage and basic statistics."""
    passed = True

    # Wave variables are only defined over ocean so land points are NaN.
    # ~50% NaN is expected for this domain straddling the Vietnamese coast.
    nan_threshold = 60.0 if is_wave else 5.0

    print(f"  Variables   :")
    for var in ds.data_vars:
        data  = ds[var].values
        n_nan = int(np.sum(np.isnan(data)))
        pct   = 100 * n_nan / data.size
        v_min = float(np.nanmin(data))
        v_max = float(np.nanmax(data))
        v_mean= float(np.nanmean(data))

        flag = "⚠  high NaN%" if pct > nan_threshold else "✓"
        if pct > nan_threshold:
            passed = False

        print(f"    {var:<10}  min={v_min:>10.3f}  max={v_max:>10.3f}"
              f"  mean={v_mean:>8.3f}  NaN={pct:.1f}%  {flag}")

    return passed


def check_physical_plausibility(ds: xr.Dataset) -> bool:
    """Check that key variables stay within physically realistic bounds."""
    passed = True

    if "swh" in ds.data_vars:
        max_hs = float(np.nanmax(ds["swh"].values))
        if max_hs > MAX_SWH:
            print(f"  [WARN] Max SWH = {max_hs:.2f} m exceeds limit of {MAX_SWH} m")
            passed = False
        else:
            print(f"  Max SWH     : {max_hs:.2f} m ✓")

    if "u10" in ds.data_vars and "v10" in ds.data_vars:
        wind_speed = np.sqrt(ds["u10"].values**2 + ds["v10"].values**2)
        max_ws = float(np.nanmax(wind_speed))
        if max_ws > MAX_WIND:
            print(f"  [WARN] Max wind speed = {max_ws:.2f} m/s exceeds limit of {MAX_WIND} m/s")
            passed = False
        else:
            print(f"  Max wind    : {max_ws:.2f} m/s ✓")

    return passed


def validate(path: Path, label: str, is_wave: bool = False) -> bool:
    """Run all checks on a single merged dataset. Returns True if all pass."""
    print(f"\n{'─' * 55}")
    print(f"  VALIDATING — {label}")
    print(f"{'─' * 55}")

    if not check_file_exists(path):
        return False

    ds = xr.open_dataset(path)

    results = [
        check_time_coverage(ds),
        check_spatial_domain(ds),
        check_variables(ds, is_wave=is_wave),
        check_physical_plausibility(ds),
    ]

    overall = all(results)
    status  = "ALL CHECKS PASSED ✓" if overall else "SOME CHECKS FAILED ⚠"
    print(f"\n  {status}")
    ds.close()
    return overall


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  ERA5 Validation — Da Nang Wave Climate")
    print("=" * 55)

    wave_ok = validate(WAVE_FILE, "ERA5 Waves", is_wave=True)   # ← True
    wind_ok = validate(WIND_FILE, "ERA5 Wind",  is_wave=False)  # ← False

    print(f"\n{'=' * 55}")
    print(f"  SUMMARY")
    print(f"{'=' * 55}")
    print(f"  Waves : {'PASS ✓' if wave_ok else 'FAIL ⚠'}")
    print(f"  Wind  : {'PASS ✓' if wind_ok else 'FAIL ⚠'}")

    # Exit with a non-zero code if any check failed
    # This makes the script CI-friendly if you add GitHub Actions later
    if not (wave_ok and wind_ok):
        sys.exit(1)


if __name__ == "__main__":
    main()