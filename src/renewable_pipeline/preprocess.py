import pandas as pd


def prepare(raw_data, processed_dir):
    data = pd.read_csv(raw_data)
    data["co2"] /= 10

    missing = data.isna().sum().rename_axis("columns").reset_index(name="missing_count")
    missing.to_csv(processed_dir / "001missing_summary.csv", index=False)

    cleaned = data.dropna()
    cleaned.to_csv(processed_dir / "002cleaned_data.csv", index=False)

    merged = pd.read_csv(processed_dir / "002cleaned_data.csv")
    merged = merged.groupby(["country", "year"], as_index=False).agg(
        {
            "co2": "mean",
            "co2_per_capita": "mean",
            "renewable_share": "mean",
            "population": "mean",
            "gdp": "mean",
            "region": "first",
        }
    )
    merged.to_csv(processed_dir / "003merged_data.csv", index=False)

    features = pd.read_csv(processed_dir / "003merged_data.csv")
    features["emissions_intensity"] = features["co2"] / features["gdp"]
    features["renewable_growth_rate"] = features.groupby("country")["renewable_share"].pct_change()
    for column in ("co2_per_capita", "renewable_growth_rate", "emissions_intensity"):
        values = features[column]
        features[f"{column}_zscore"] = (values - values.mean()) / values.std()

    features.to_csv(processed_dir / "004processed_data.csv", index=False)
    return features
