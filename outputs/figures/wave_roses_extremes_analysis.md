# Wave Climate Analysis — Da Nang Bay (2014–2024)

### Results Summary: Wave Roses & Extreme Value Analysis

_ERA5 reanalysis | Notebook: `notebooks/wave_roses_extremes.ipynb`_

---

## 1. Dataset Overview

Before generating any figures, the ERA5 wave dataset was loaded and spatially averaged over all valid ocean grid points within the study domain (15–17°N, 107–109°E). Land grid points are masked as NaN in ERA5 wave variables and excluded from the spatial mean automatically via `skipna=True`.

| Parameter               | Value                   |
| ----------------------- | ----------------------- |
| Valid hourly records    | 96,432                  |
| Record period           | 2014-01-01 → 2024-12-31 |
| Hs range (spatial mean) | 0.19 – 5.74 m           |
| MWD range               | 7.8° – 347.5°           |

**Note on spatial averaging:** The Hs values reported here represent the spatial mean over ocean grid points. The validation script previously identified a maximum Hs of 7.90 m in the raw gridded data — the lower maximum seen here (5.74 m) reflects the smoothing effect of spatial averaging. Both values are physically realistic for the South China Sea.

---

## 2. Annual Wave Rose

**Figure:** `wave_rose_annual.png`

### What this figure is trying to show

The annual wave rose summarises the full 10-year wave climate at Da Nang Bay in a single polar diagram. Each petal represents a 22.5° directional sector. Petal length shows how frequently waves arrive from that direction (as a percentage of total time). The colour of each segment within a petal represents the Hs bin, from calm conditions (0–0.5 m, white) to energetic swell (4.0–8.0 m, dark blue).

### Key findings

**Dominant direction — ENE (060°–080°)**
The longest and darkest petal points toward the east-northeast, confirming that the NE monsoon swell is the dominant feature of the Da Nang Bay wave climate. This is physically consistent with the geometry of the South China Sea — during the NE monsoon (October to March), winds blow persistently from the northeast across a long fetch over open water before reaching the Vietnamese coast.

**High energy concentration**
The darkest blue segments (Hs 3.0–4.0 m and 4.0–8.0 m) are concentrated almost exclusively in the ENE sector. This means not only are the most frequent waves from this direction, but the largest waves are also from this direction. This has direct implications for coastal structure orientation and port downtime — any structure exposed to the northeast has both the most frequent and most energetic wave exposure.

**Secondary signal — SSE (150°–170°)**
A smaller, lower-energy cluster of petals is visible in the south-southeast sector. This represents the SW monsoon season, when wind-driven seas approach from the south. These waves are notably shorter, lower, and more dispersed in direction than the NE monsoon swell.

**Calm sectors**
The western, northwestern and southwestern quadrants are near-empty, reflecting the sheltering effect of the Vietnamese mainland and the Annamite Mountain Range to the west.

---

## 3. Seasonal Wave Roses

**Figure:** `wave_roses_seasonal.png`

### What this figure is trying to show

Splitting the wave rose by monsoon season isolates the two distinct meteorological regimes that drive the Da Nang wave climate. The NE monsoon (October–March, blue) and SW monsoon (May–September, orange) are plotted side by side on the same scale, making the contrast immediately visible to any reader.

### Season definitions

| Season     | Months          | n (hours) |
| ---------- | --------------- | --------- |
| NE Monsoon | October – March | 48,120    |
| SW Monsoon | May – September | 40,392    |
| Transition | April           | ~7,920    |

### Key findings

#### NE Monsoon (October–March)

| Statistic | Value  |
| --------- | ------ |
| Mean Hs   | 1.41 m |
| P90 Hs    | 2.51 m |

The NE monsoon rose shows an extremely narrow, energetic petal pointing ENE — almost all wave energy arrives from a single directional window of approximately 40°. This directional persistence is characteristic of monsoon-driven swell, where sustained winds blow from a consistent direction over thousands of kilometres of open water. The presence of dark blue segments (Hs > 3.0 m) confirms that the largest and most energetically significant waves of the year occur during this season. This is the dominant design-controlling wave climate for any coastal infrastructure in Da Nang Bay.

#### SW Monsoon (May–September)

| Statistic | Value  |
| --------- | ------ |
| Mean Hs   | 0.60 m |
| P90 Hs    | 0.89 m |

The SW monsoon rose is visually very different — petals are spread across a much wider directional window (roughly SSE to SSW, 120°–220°), and all segments are low-energy (predominantly Hs 0.5–1.5 m). This reflects locally generated wind-sea rather than long-period ocean swell. The Da Nang coastline receives limited SW monsoon wave energy because the South China Sea basin is much narrower in this fetch direction, and the bay itself provides some sheltering from the south.

#### Seasonal contrast summary

The difference between the two roses is the central narrative of this wave climate study. The NE monsoon produces waves that are roughly **2.4× higher on average**, **strongly unidirectional**, and capable of reaching **Hs > 4.0 m** — conditions that would halt most marine operations. The SW monsoon by comparison represents a largely benign wave environment suitable for offshore construction and vessel operations.

---

## 4. Extreme Value Analysis — Gumbel Distribution Fit

### What this analysis is trying to find out

Extreme value analysis answers the question: _how large could waves get over a design lifetime?_ Engineering structures such as breakwaters, jetties, and offshore platforms are designed to withstand waves of a given return period — typically 50 or 100 years. Because we only have 11 years of data, we cannot observe a 100-year wave directly. Instead, we fit a statistical distribution to the annual maximum Hs values and extrapolate beyond the record.

### Method — Gumbel (Type I Extreme Value) distribution

The Gumbel distribution is the standard choice for fitting annual maximum wave heights. It belongs to the family of extreme value distributions, which are theoretically justified for block maxima (the largest value in each year). The distribution is parameterised by a location parameter μ and a scale parameter σ, fitted using Maximum Likelihood Estimation (MLE) via `scipy.stats.gumbel_r`.

**Fitted parameters:**
| Parameter | Value |
|-----------|-------|
| Location (μ) | 3.6818 |
| Scale (σ) | 0.4851 |

### Annual maximum Hs — observed values

| Year     | Annual Max Hs (m) | Notes                                        |
| -------- | ----------------- | -------------------------------------------- |
| 2014     | 3.424             |                                              |
| 2015     | 3.189             | Lowest on record — quiet year                |
| 2016     | 3.640             |                                              |
| 2017     | 3.916             |                                              |
| 2018     | 3.784             |                                              |
| 2019     | 3.430             |                                              |
| 2020     | 5.742             | Highest on record — likely typhoon influence |
| 2021     | 4.043             |                                              |
| 2022     | 4.914             |                                              |
| 2023     | 3.472             |                                              |
| 2024     | 4.383             |                                              |
| **Mean** | **3.995**         |                                              |

The 2020 annual maximum of 5.74 m is notably elevated relative to other years, consistent with an intense typhoon passing within or near the ERA5 domain during that season. The remaining years cluster between 3.2 and 4.9 m, showing reasonable inter-annual variability.

---

## 5. Return Period Curve

**Figure:** `return_period_curve.png`

### What this figure is trying to show

The return period curve plots extrapolated Hs against return period on a logarithmic x-axis. A 100-year return period Hs does not mean a wave that occurs exactly once per century — it means the wave height that has a **1% probability of being exceeded in any given year**. The 90% bootstrap confidence intervals show the uncertainty in these estimates arising from the short 11-year record.

### Return period estimates

| Return Period (yr) | Hs (m) | 90% CI Lower (m) | 90% CI Upper (m) | CI Width (m) |
| ------------------ | ------ | ---------------- | ---------------- | ------------ |
| 2                  | 3.86   | 3.59             | 4.21             | 0.62         |
| 5                  | 4.41   | 3.89             | 4.98             | 1.09         |
| 10                 | 4.77   | 4.09             | 5.50             | 1.41         |
| 25                 | 5.23   | 4.33             | 6.17             | 1.84         |
| 50                 | 5.57   | 4.51             | 6.67             | 2.16         |
| 100                | 5.91   | 4.69             | 7.17             | 2.48         |

### Interpretation

**Quality of fit**
The empirical data points (plotted using Gringorten plotting positions, which are recommended for Gumbel distributions) sit close to the fitted curve across the full range of the record. This gives confidence that the Gumbel distribution is an appropriate model for this dataset.

**The 2020 event**
The 2020 annual maximum of 5.74 m plots slightly above the fitted Gumbel curve, consistent with it being an anomalously large event. It falls within the 90% confidence band, meaning it is not a statistical outlier — rather, it represents a relatively rare but plausible extreme in this wave climate.

**Widening confidence intervals**
The 90% CI width grows from 0.62 m at the 2-year return period to 2.48 m at the 100-year level. This reflects an important physical reality: the further we extrapolate beyond the length of our record (11 years), the more uncertain our estimates become. The 11-year record constrains the 10-year estimate reasonably well, but the 100-year estimate should be treated as indicative rather than definitive.

**Engineering design values**
For preliminary design purposes the point estimates and their confidence intervals suggest:

- A **breakwater or jetty** designed for a 50-year return period should be capable of withstanding Hs ≈ 5.6 m, with a conservative upper bound of 6.7 m
- A **100-year design condition** of Hs ≈ 5.9 m (upper CI 7.2 m) would apply to critical permanent infrastructure
- These values represent offshore conditions from the ERA5 grid — nearshore design values would require transformation using a numerical wave propagation model such as SWAN or MIKE 21 SW

### Limitations and caveats

**Record length:** With only 11 years of data, the 100-year return period estimate is a substantial extrapolation (extrapolating ~9× beyond the record length). A longer record of 30–50 years would significantly narrow the confidence intervals. For a final engineering design, ERA5 data should be supplemented with historical typhoon track analysis and, if available, buoy measurements for bias correction.

**ERA5 bias:** ERA5 is known to slightly underestimate peak wave heights during intense tropical cyclones due to the coarse spatial resolution of the atmospheric model (~31 km grid). The true 100-year Hs at Da Nang Bay may be somewhat higher than the 5.91 m point estimate. This should be noted in any engineering report that relies on these values for design.

**Spatial averaging:** Annual maxima were extracted from spatially averaged Hs, which reduces peak values. Analysis of individual grid point maxima would yield higher extreme estimates and is recommended for site-specific design.

---

## 6. Summary of Key Results

| Result                           | Value                    |
| -------------------------------- | ------------------------ |
| Dominant wave direction (annual) | ENE (060°–080°)          |
| NE monsoon mean Hs               | 1.41 m                   |
| NE monsoon P90 Hs                | 2.51 m                   |
| SW monsoon mean Hs               | 0.60 m                   |
| SW monsoon P90 Hs                | 0.89 m                   |
| 10-year return period Hs         | 4.77 m (CI: 4.09–5.50 m) |
| 50-year return period Hs         | 5.57 m (CI: 4.51–6.67 m) |
| 100-year return period Hs        | 5.91 m (CI: 4.69–7.17 m) |
| Gumbel location parameter μ      | 3.6818                   |
| Gumbel scale parameter σ         | 0.4851                   |

---

## 7. Relevance to Coastal Engineering Practice

The results of this analysis are directly applicable to a range of coastal engineering tasks at Da Nang Bay:

**Port and harbour operations** — the calm weather statistics derived from the NE/SW monsoon split inform vessel scheduling and marine construction windows. The SW monsoon (May–September) represents the primary operational window for offshore works, with mean Hs of 0.60 m and P90 of only 0.89 m.

**Structural design** — the return period table provides preliminary design wave heights for coastal structures. These would feed into a wave transformation model to account for refraction, shoaling and breaking over the nearshore bathymetry before being used in detailed structural design.

**Orientation of coastal structures** — the strong directional persistence of NE monsoon waves (ENE sector) means that breakwaters and port entrance channels should be aligned to maximise sheltering from this sector, as it controls both the frequency and magnitude of wave exposure throughout the year.

**Environmental impact assessment** — the seasonal contrast in wave energy informs assessments of sediment transport, coastal erosion and morphological change, which are strongly modulated by the monsoon cycle at this latitude.

---

_Generated as part of Da Nang Bay Wave Climate Assessment portfolio project._
_Data source: ERA5 hourly reanalysis (Copernicus CDS), 2014–2024._
_Bathymetry: GEBCO 2025, 15 arc-second resolution._
