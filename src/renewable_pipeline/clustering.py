import pandas as pd
from sklearn.cluster import KMeans


def cluster(processed_dir):
    data = pd.read_csv(processed_dir / "004processed_data.csv")
    features = ["co2_per_capita", "renewable_growth_rate", "emissions_intensity"]
    data = data.dropna(subset=features).copy()
    model = KMeans(
        n_clusters=4, init="k-means++", n_init=10, max_iter=300, tol=1e-4, random_state=42
    )
    data["cluster_label"] = model.fit_predict(data[features])
    summary = data.groupby("cluster_label", as_index=False).agg(
        avg_co2=("co2", "mean"), avg_renewable_share=("renewable_share", "mean")
    )
    summary.to_csv(processed_dir / "013cluster_summary.csv", index=False)
