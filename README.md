# Manchester United 2024–25 · Post-Season Performance Analysis

> **Why did Manchester United finish 15th, 32 points off a Champions League place?**  
> A full data-science investigation — from raw scraping to regression modelling to an interactive narrative dashboard.

🔗 **[Live App →](https://man-united-post-season-performance-analysis.streamlit.app/)**  
📊 **Data Source:** [Understat – EPL 2024–25](https://understat.com/league/EPL/2024)  
🛠 **Stack:** Python · Pandas · Scikit-learn · Plotly · Streamlit

---

## Table of Contents

- [Project Overview](#project-overview)
- [What Is xG? (Non-Technical Primer)](#what-is-xg-non-technical-primer)
- [Repository Structure](#repository-structure)
- [Methodology — End to End](#methodology--end-to-end)
  - [Stage 1 · Data Collection](#stage-1--data-collection)
  - [Stage 2 · Data Cleaning & Feature Engineering](#stage-2--data-cleaning--feature-engineering)
  - [Stage 3 · Top 4 Benchmarking](#stage-3--top-4-benchmarking)
  - [Stage 4 · Gap Analysis](#stage-4--gap-analysis)
  - [Stage 5 · Linear Regression Impact Model](#stage-5--linear-regression-impact-model)
  - [Stage 6 · Performance vs Expectation](#stage-6--performance-vs-expectation)
  - [Stage 7 · Player-Level Diagnosis](#stage-7--player-level-diagnosis)
  - [Stage 8 · Interactive Simulation](#stage-8--interactive-simulation)
- [Key Findings](#key-findings)
- [The Dashboard — App Walkthrough](#the-dashboard--app-walkthrough)
- [Tech Stack & Design Decisions](#tech-stack--design-decisions)
- [Limitations & Caveats](#limitations--caveats)
- [Getting Started](#getting-started)

---

## Project Overview

Manchester United's 2024–25 Premier League campaign ended in historic failure — 15th place, 42 points, 32.5 behind the Top 4 threshold. But *why*? Was it bad luck, poor tactics, individual failures, or something deeper?

This project answers that question the same way modern clubs do: with data.

Using expected goals (xG) and expected goals against (xGA) data from [Understat](https://understat.com/league/EPL/2024) for three consecutive Premier League seasons (2022–23, 2023–24, 2024–25), this analysis:

1. **Defines the standard** — what attacking and defensive performance actually qualifies a team for the Top 4
2. **Quantifies the gap** — how far United fell short on both sides of the ball
3. **Models the cost in points** — using a linear regression trained across all 20 PL clubs to translate performance gaps into point losses
4. **Isolates structural vs efficiency failures** — separating "they didn't create enough chances" from "they wasted the chances they did create"
5. **Diagnoses individual contributors** — which players underperformed their xG and who carried the attacking burden
6. **Simulates the fix** — an interactive model that projects how improvements in attack or defense translate to a Top 4 finish

The result is a premium, narrative-driven analytics product — not just a notebook, but a live web application built for both technical and non-technical stakeholders.

---

## What Is xG? (Non-Technical Primer)

**Expected Goals (xG)** is the probability that a given shot results in a goal, calculated from historical data across thousands of similar shots. Factors include:

- Distance from goal
- Angle of the shot
- Whether it was a header or a foot shot
- Assist type (through ball, cross, etc.)
- Whether the player was under pressure

A tap-in from six yards out might carry an xG of 0.85 — very likely to score. A long-range speculative effort might carry an xG of 0.03.

**Why it matters:** xG removes luck. A team that creates 2.5 xG per match is generating high-quality chances regardless of whether the goalkeeper makes three incredible saves on any given day. Over 38 matches, xG is a far more reliable predictor of a team's true quality than actual goals scored.

**xGA (Expected Goals Against)** applies the same logic defensively — how much danger was the team exposed to, irrespective of whether those chances were converted.

**xPTS (Expected Points)** extends this further: using the xG and xGA of every match, it simulates the most likely points outcome, stripping away goalkeeper heroics and goalkeeping errors to reveal the "true" underlying points a team deserved.

---

## Repository Structure

```
├── 01_data_cleaning.ipynb      # Raw data ingestion, cleaning, and feature engineering
├── 02_analysis.ipynb           # All analytical stages: benchmarking, regression, diagnosis
├── app.py                      # Streamlit dashboard application
├── clean_teams.csv             # Processed team-level data (3 seasons, all 20 clubs)
├── clean_players.csv           # Processed player-level data (filtered >900 mins)
├── 22-23.csv                   # Raw team data — 2022–23 season
├── 23-24.csv                   # Raw team data — 2023–24 season
├── 24-25.csv                   # Raw team data — 2024–25 season
└── league-players.csv          # Raw player data — 2024–25 season
```

---

## Methodology — End to End

### Stage 1 · Data Collection

**Source:** [Understat](https://understat.com/league/EPL/2024) — one of the most respected publicly available football analytics databases, providing shot-level xG data for all top European leagues.

**What was collected:**

| Dataset | Granularity | Contents |
|---|---|---|
| Team data (3 seasons) | Season-level per club | Matches, wins, draws, losses, goals, xG, xGA, xPTS, points, table rank |
| Player data (2024–25) | Individual player | Minutes played, goals, assists, xG, team affiliation |

Three seasons of team data were collected to build a robust regression dataset. A single-season regression on 20 data points risks overfitting; pooling three seasons gives 60 observations (3 × 20 clubs), producing more stable and generalisable coefficients.

---

### Stage 2 · Data Cleaning & Feature Engineering

**Notebook:** `01_data_cleaning.ipynb`

**Team data cleaning:**

- Standardised column names across seasons (e.g., `loses` → `losses` for consistency)
- Added a `season` label to each row before concatenating all three seasons into a single unified dataset (`df_teams`)
- Verified data types to ensure numeric columns were not silently stored as strings

**Feature engineering — team level:**

| New Feature | Formula | Purpose |
|---|---|---|
| `xG_per_match` | `xG / matches` | Normalises attacking output for fair cross-team comparison |
| `xGA_per_match` | `xGA / matches` | Normalises defensive exposure |
| `xG_diff` | `xG - xGA` | Net expected goal differential — a proxy for dominance |

Dividing by matches played is essential. A team that played 38 matches and generated 80 xG looks identical to a team that generated 80 xG in 40 matches — but they performed differently. Per-match rates remove this distortion.

**Player data cleaning:**

- Renamed ambiguous columns (`min` → `minutes`, `a` → `assists`)
- Applied a **minimum minutes threshold of 900** — approximately 10 full matches — to eliminate small-sample noise from players with 1–2 appearances
- Resolved multi-team assignment issues: several players appeared for two clubs during the season (e.g., loan moves). A manual mapping dictionary handled edge cases where name or team string contained comma-separated entries, taking the primary team only
- Name normalisation: all player names were lowercased, stripped of whitespace, and mapped back to their canonical display form to prevent silent merge failures

**Feature engineering — player level:**

| New Feature | Formula | Purpose |
|---|---|---|
| `goal_contribution` | `goals + assists` | Combined attacking output |
| `contribution_per_90` | `(goal_contribution / minutes) × 90` | Rate-normalised output |
| `finishing_diff` | `goals − xG` | Finishing efficiency: positive = overperformer, negative = wasted chances |

**Data integrity check:**

A cross-validation step compared the teams present in the player dataset against those in the team dataset. Relegated clubs (who appear in team history but not the current player data) and loanees (who appear in player data under multiple teams) were identified and resolved before any analysis ran.

---

### Stage 3 · Top 4 Benchmarking

**Notebook:** `02_analysis.ipynb`

Before diagnosing failure, the analysis defines success. The 2024–25 Top 4 — Liverpool, Arsenal, Manchester City, Chelsea — set the performance standard:

| Metric | Top 4 Average |
|---|---|
| xG per match | **2.06** |
| xGA per match | **1.25** |
| Points | **74.5** |

**Key observation:** City (1.39 xGA/match) and Chelsea (1.42 xGA/match) both finished Top 4 despite well-above-average defensive exposure. This reveals a structural insight that shapes the entire analysis:

> *Attack is the primary driver of Top 4 qualification. Defensive performance is more flexible — an elite attack can compensate for a leaky defense, but no level of defensive excellence compensates for failing to create chances.*

---

### Stage 4 · Gap Analysis

Manchester United's 2024–25 per-match profile is compared directly against the Top 4 benchmark:

| Metric | Man United | Benchmark | Gap |
|---|---|---|---|
| xG per match | 1.498 | 2.060 | **−0.562** |
| xGA per match | 1.598 | 1.246 | **+0.352** |
| Points | 42 | 74.5 | **−32.5** |

United were off the pace on *both* sides of the ball, but the attacking shortfall is 60% larger in magnitude than the defensive one. This is not primarily a defensive crisis — it is an attacking one.

**Season-scale extrapolation:**

- Attacking gap of −0.562 xG/match × 38 matches = **~21 goals' worth of missing chances**
- Defensive gap of +0.352 xGA/match × 38 matches = **~13 extra chances conceded**

---

### Stage 5 · Linear Regression Impact Model

**Notebook:** `02_analysis.ipynb`

To translate the per-match gaps into concrete point values, a **multivariate linear regression** was trained on all 60 team-season observations (20 clubs × 3 seasons):

```
Points = β₀ + β₁·(xG_per_match) + β₂·(xGA_per_match)
```

**Fitted coefficients:**

| Term | Coefficient | Interpretation |
|---|---|---|
| Intercept | 46.36 | Baseline points with zero xG/xGA |
| xG per match | **+26.57** | Every +0.1 xG/match adds ~2.66 points |
| xGA per match | **−22.63** | Every −0.1 xGA/match adds ~2.26 points |

Both coefficients are substantial and directionally correct (more attacking output → more points; more chances conceded → fewer points). Attacking output carries slightly higher marginal impact per unit.

**Applying the model to United's gap:**

```
Points lost (attack)  = −0.562 × 26.57 = −14.94 pts
Points lost (defense) = +0.352 × −22.63 = −7.96 pts
────────────────────────────────────────────────────
Model-explained deficit                   = −22.9 pts
```

The model explains **22.9 of the 32.5-point deficit** — approximately **70% of the total underperformance** has a direct, structural, quantifiable cause.

**Why pooled regression over three seasons?**

Using a single season (20 observations) risks unstable coefficients — one outlier club can swing the model significantly. Three seasons gives 60 observations, dramatically reducing this risk and making the coefficients more representative of the true relationship between xG/xGA and points across the full distribution of Premier League clubs.

---

### Stage 6 · Performance vs Expectation

The remaining ~10 points are explained by *efficiency* — the gap between what United's underlying performance predicted and what actually happened:

| Metric | Value | Interpretation |
|---|---|---|
| Goals − xG (finishing) | **−12.91** | United wasted 13 goals' worth of chances |
| GA − xGA (defense) | **−6.73** | United conceded 7 *fewer* goals than expected |
| Actual pts − xPTS | **−10.24** | Results lagged underlying performance |

Two competing forces are at work here:

**🔴 Attacking execution failure:** The squad generated 56.9 xG across the season but scored only 44 goals. This is not just bad luck — a gap this large over 38 matches reflects a genuine conversion problem at the squad level.

**🟢 Defensive execution strength:** Despite high xGA (the team was exposed to plenty of danger), they conceded only 58 goals against an expectation of 60.7. This is a genuine positive — André Onana and the defensive unit performed *above* expectation when it mattered.

**Full picture, combined:**

| Layer | Type | Impact |
|---|---|---|
| Attacking xG gap | Structural | −14.9 pts |
| Defensive xGA gap | Structural | −8.0 pts |
| Finishing variance | Efficiency | ~−10 pts |
| **Total** | | **~−32.9 pts** |

---

### Stage 7 · Player-Level Diagnosis

With the structural problem established (attack), the player data identifies *why* United's xG was low and *which players* were responsible for the conversion failures.

**Goal contribution concentration:**

65% of all goal contributions (goals + assists) came from just four players — Bruno Fernandes, Amad Diallo, Marcus Rashford, and Alejandro Garnacho. This extreme concentration means a single injury or dip in form removes a disproportionate share of the team's entire attacking output.

**Finishing efficiency rankings (goals minus xG):**

| Player | Goals | xG | Diff | Assessment |
|---|---|---|---|---|
| Alejandro Garnacho | 6 | 9.44 | **−3.44** | Major underperformer |
| Bruno Fernandes | 8 | 9.89 | −1.89 | Below expectation |
| Rasmus Højlund | 4 | 5.87 | −1.87 | Concerning for primary striker |
| Joshua Zirkzee | 3 | 5.22 | −2.22 | Failed to deliver |
| Amad Diallo | 8 | 4.75 | **+3.25** | Elite overperformer |
| Marcus Rashford | 6 | 4.99 | +1.01 | Positive finisher |

**Striker problem:** Højlund — the designated #9 — converted just 4 goals from 5.87 xG. A striker converting at or above their xG rate adds approximately 5+ points across a full season. His goal contribution rate of 0.177 per 90 minutes is extremely low for a first-choice centre-forward at a club with Champions League ambitions.

**Diogo Dalot:** Generated 1.70 xG from a full-back position — a significant attacking contribution — but scored 0 goals. This represents 1.7 wasted expected goals from a non-attacking position, compounding the overall finishing problem.

---

### Stage 8 · Interactive Simulation

The regression model is operationalised as an interactive tool in the dashboard. Users can set:

- **Attack improvement** — increase in xG per match (+0.00 to +0.80)
- **Defense improvement** — reduction in xGA per match (−0.00 to −0.60)

The model projects the resulting points total and classifies the outcome as:

| Result | Threshold | Verdict |
|---|---|---|
| 🟢 Top 4 achieved | ≥74 projected points | Champions League |
| 🟡 Borderline | 69–73 projected points | Possible but fragile |
| 🔴 Still short | <69 projected points | Outside looking in |

This gives club decision-makers (or curious fans) a direct, quantified answer to: *"If we buy a striker who adds +0.3 xG per match, does that get us there?"*

---

## Key Findings

### 1. United's problem is primarily structural, not variance-driven
70% of the 32.5-point deficit is explained by their fundamental per-match xG and xGA levels — not bad luck or form runs. The architecture of the team was not built to compete for Top 4.

### 2. Attack is the dominant lever, not defense
The attacking shortfall (−14.9 pts) is nearly double the defensive exposure (−8.0 pts). Investment in defensive consolidation alone cannot close the gap.

### 3. Poor finishing amplifies an already-weak attack
Even for the chances United did create, they converted them poorly — 12.9 goals below expectation. This is an execution problem layered on top of a volume problem.

### 4. Defensive execution is a genuine positive
United's goalkeeping and defensive unit conceded 6.7 fewer goals than expected — a meaningful and consistent positive that the raw table position obscures.

### 5. The squad is dangerously concentrated
Four players account for 65% of all goal output. The Fernandes dependency is particularly acute — 18 of United's 49 total goal contributions ran through one player.

### 6. The striker position was the single most costly individual failure
Højlund's conversion rate from xG means United effectively "lost" a full striker's worth of goals across the season. A conversion-efficient #9 adds ~5 points annually at United's current xG volume.

---

## The Dashboard — App Walkthrough

The app is structured as a **long-form narrative analytics report** with eight sequential sections, each building on the last:

| Section | Title | What It Shows |
|---|---|---|
| 00 · Hero | "Why United missed the Top 4" | Framing, methodology badges, key questions |
| 01 · The Standard | Benchmark analysis | Scatter plot of all 6 teams: xG vs xGA per match |
| 02 · The Gap | United vs Benchmark | Grouped horizontal bar chart comparing both sides |
| 03 · Quantifying the Cost | Regression model output | Waterfall chart: benchmark → attack penalty → defense penalty → projected points |
| 04 · The Hidden Layer | Performance vs expectation | Finishing deficit, defensive efficiency, points variance |
| 05 · Inside the Squad | Player contribution | Horizontal bar chart, finishing efficiency table |
| 06 · The Verdict | Full diagnosis | Donut chart (structural vs efficiency), numbered root causes |
| 07 · What Would It Take | Simulation | Interactive sliders → projected points + verdict |
| 08 · What Needs to Change | Recommendations | Prioritised investment case for the rebuild |

**Design philosophy:** The app is designed to be fully readable by a non-technical audience — a director of football, a journalist, or a fan — while containing enough methodological depth to satisfy a data scientist. Every chart is annotated with interpretive callouts so the insight is never left implicit.

---

## Tech Stack & Design Decisions

| Component | Tool | Why |
|---|---|---|
| Data analysis | **Pandas** | Industry standard for tabular data manipulation |
| Machine learning | **Scikit-learn** (`LinearRegression`) | Transparent, interpretable model appropriate for the problem |
| Visualisation | **Plotly** (Graph Objects) | Full customisation, interactive tooltips, consistent dark-theme rendering |
| Application | **Streamlit** | Rapid deployment, Python-native, no frontend engineering required |
| Styling | **Custom CSS + DM Serif / DM Sans fonts** | Editorial, premium aesthetic — differentiated from standard Streamlit apps |
| Hosting | **Streamlit Community Cloud** | Zero-infrastructure deployment, live at public URL |

**On the choice of Linear Regression:**  
A more complex model (Random Forest, XGBoost) would likely achieve higher R² — but at the cost of interpretability. The primary goal of this project is to *explain* the point deficit, not to maximise predictive accuracy. A linear model produces coefficients that can be directly communicated: "every +0.1 xG per match adds 2.66 points." That kind of direct attribution is what makes the simulation section meaningful.

**On the dark editorial design:**  
The app deliberately diverges from the default Streamlit aesthetic. Manchester United's brand (deep red, black) was the visual starting point. The typography hierarchy — display serif headings, sans-serif body copy, monospaced stat values — mirrors the design language of premium sports journalism products. This was a deliberate product decision: the analysis deserves a presentation that matches its depth.

---

## Limitations & Caveats

**1. xG is an input, not ground truth.**  
Understat's xG model is excellent but not official. Different providers (Opta, StatsBomb) use different shot-quality models and may produce slightly different values.

**2. The regression model is descriptive, not causal.**  
The model quantifies *how much* United's xG gap cost them in points — it does not claim to explain *why* United had a low xG. Causality requires more granular data (pressing intensity, tactical shape, injury impact).

**3. Three seasons pool distinct squads and managers.**  
Pooling 2022–23 (Ten Hag season 1), 2023–24 (Ten Hag season 2), and 2024–25 (Amorim) introduces managerial and squad heterogeneity. This is acceptable for building a generalised PL-wide model but means the coefficients reflect league-wide relationships, not United-specific ones.

**4. Player data covers only the 2024–25 season.**  
The player diagnosis is cross-sectional. A multi-season player dataset would allow regression-to-mean analysis and separate true underperformers from one-season variance.

**5. The ~10-point unexplained residual.**  
The model explains 70% of the deficit. The remaining 30% involves match-level variance (close-game results, set-piece outcomes, referee decisions) that xG cannot fully capture.

---

## Getting Started

**To run locally:**

```bash
git clone https://github.com/your-username/man-united-analysis.git
cd man-united-analysis

pip install -r requirements.txt

streamlit run app.py
```

**Requirements:**

```
streamlit
pandas
numpy
plotly
scikit-learn
```

**To explore the analysis:**

Open `01_data_cleaning.ipynb` first, then `02_analysis.ipynb`. All intermediate CSVs (`clean_teams.csv`, `clean_players.csv`) are included so the notebooks run without re-scraping.

---

*Data: Understat · Model: Linear Regression (R²~0.85, 60 observations) · Season: 2024–25 Premier League*  
*Built with Streamlit + Plotly · Deployed on Streamlit Community Cloud*
