import pandas as pd
from scipy.stats import linregress


def summarize(features, processed_dir):
    measures = ["co2", "co2_per_capita", "renewable_share"]
    statistics = features.groupby("country")[measures].agg(["mean", "std", "max", "min"])
    statistics.columns = [f"{statistic}_{column}" for column, statistic in statistics.columns]
    statistics.reset_index().to_csv(processed_dir / "005processed_data.csv", index=False)

    merged = pd.read_csv(processed_dir / "003merged_data.csv")
    trends = []
    correlations = []
    for country, group in merged.groupby("country"):
        slope = linregress(group["year"], group["co2"]).slope
        correlation = group["renewable_share"].corr(group["co2"].pct_change())
        trends.append((country, slope))
        correlations.append((country, correlation))

    pd.DataFrame(trends, columns=["country", "slope"]).to_csv(
        processed_dir / "006country_data.csv", index=False
    )
    pd.DataFrame(correlations, columns=["country", "correlation"]).to_csv(
        processed_dir / "007correlation.csv", index=False
    )

    start = merged.loc[merged["year"] == 2020].set_index("country")
    end = merged.loc[merged["year"] == 2024].set_index("country")
    reductions = pd.DataFrame(
        {
            "change": end["co2"] - start["co2"],
            "avg_renewable_increase": end["renewable_share"] - start["renewable_share"],
        }
    )
    reductions.sort_values("change").head(5).reset_index().to_csv(
        processed_dir / "012top_reduction.csv", index=False
    )
