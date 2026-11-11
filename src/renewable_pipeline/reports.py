import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def write_reports(processed_dir, reports_dir):
    processed = pd.read_csv(processed_dir / "004processed_data.csv")
    merged = pd.read_csv(processed_dir / "003merged_data.csv")
    write_global_trends(processed, processed_dir, reports_dir)
    write_emissions_bubble_chart(merged, processed_dir, reports_dir)
    write_country_comparison(merged, processed_dir, reports_dir)


def write_global_trends(data, processed_dir, reports_dir):
    trends = data.groupby("year", as_index=False).agg(
        total_co2=("co2", "sum"), avg_renewable_share=("renewable_share", "mean")
    )
    trends.to_csv(processed_dir / "009global_trends.csv", index=False)

    figure = Figure(figsize=(12, 6))
    FigureCanvasAgg(figure)
    emissions_axis = figure.subplots()
    share_axis = emissions_axis.twinx()
    lines = emissions_axis.plot(
        trends["year"], trends["total_co2"], color="blue", marker="o", label="Total CO2 Emissions"
    )
    lines += share_axis.plot(
        trends["year"], trends["avg_renewable_share"],
        color="orange", marker="s", label="Avg Renewable Share (%)",
    )
    emissions_axis.set(xlabel="Year", ylabel="Total CO2 Emissions (100 million tons)")
    share_axis.set_ylabel("Avg Renewable Share (%)")
    emissions_axis.set_title("Global CO2 Emissions and Renewable Share Trends (Dual Line Chart)")
    emissions_axis.grid(True, linestyle="--", alpha=0.5)
    emissions_axis.legend(handles=lines, loc="upper left")
    figure.savefig(reports_dir / "global_trends.png")


def write_emissions_bubble_chart(data, processed_dir, reports_dir):
    snapshot = data.loc[data["year"] == 2024].copy()
    snapshot["bubble_size"] = snapshot["co2_per_capita"] * 15
    columns = [
        "country", "year", "co2", "co2_per_capita", "renewable_share",
        "population", "gdp", "region", "bubble_size",
    ]
    snapshot[columns].to_csv(processed_dir / "010map_data.csv", index=False)

    figure = Figure(figsize=(10, 8))
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    points = axis.scatter(
        snapshot["gdp"], snapshot["co2"], s=snapshot["bubble_size"],
        c=snapshot["renewable_share"], cmap="viridis", alpha=0.6, edgecolors="grey",
    )
    figure.colorbar(points, ax=axis).set_label("Renewable Share (%)")
    axis.set(xlabel="GDP", ylabel="Total CO2 Emissions (hundred million tons)")
    axis.set_title("2024 CO2 Emissions vs GDP (Bubble=Per Capita Emissions, Color=Renewable Share)")
    axis.grid(True, linestyle="--", alpha=0.5)
    axis.set_axisbelow(True)
    for spine in axis.spines.values():
        spine.set_visible(True)
    figure.savefig(reports_dir / "map_2024.png", dpi=300, bbox_inches="tight")


def write_country_comparison(data, processed_dir, reports_dir):
    countries = ["Country_001", "Country_002", "Country_003"]
    comparison = data.loc[data["country"].isin(countries)].sort_values(["country", "year"])
    comparison.to_csv(processed_dir / "011combo_data.csv", index=False)

    figure = Figure(figsize=(12, 6))
    FigureCanvasAgg(figure)
    emissions_axis = figure.subplots()
    share_axis = emissions_axis.twinx()
    lines = []
    for index, (country, color) in enumerate(zip(countries, ("gold", "blue", "green")), start=1):
        series = comparison.loc[comparison["country"] == country]
        lines += emissions_axis.plot(
            series["year"], series["co2"], color=color, marker="o", label=f"C{index} CO2"
        )
        lines += share_axis.plot(
            series["year"], series["renewable_share"],
            color=color, marker="s", linestyle="--", label=f"C{index} Share",
        )
    emissions_axis.set(xlabel="Year", ylabel="Total CO2 Emissions (hundred million tons)")
    share_axis.set_ylabel("Renewable Share (%)")
    emissions_axis.set_title("CO2 Emissions and Renewable Share Trends (2000-2024)")
    emissions_axis.legend(handles=lines, loc="upper left", fontsize="small")
    emissions_axis.grid(True, linestyle="--", alpha=0.3)
    emissions_axis.set_axisbelow(True)
    figure.savefig(reports_dir / "combo_chart.png", dpi=300, bbox_inches="tight")
