from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route("/top-tags")
def top_tags():
    df = pd.read_csv("stackoverflow_questions_copy.csv", on_bad_lines='skip')
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=["Time", "Tags"])
    df['Year'] = df['Time'].dt.year

    total_per_year = df.groupby("Year").size()
    tag_year_counts = df.groupby(["Tags", "Year"]).size().unstack(fill_value=0)
    relative = tag_year_counts.divide(total_per_year, axis=1) * 100

    top_tags = df['Tags'].value_counts().head(10).index
    filtered = relative.loc[top_tags]

    chart_data = {
        "labels": list(filtered.columns),  # years
        "datasets": []
    }

    colors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
        "#FF9F40", "#E7E9ED", "#00A86B", "#FF4500", "#4682B4"
    ]

    for i, tag in enumerate(filtered.index):
        chart_data["datasets"].append({
            "label": tag,
            "data": list(filtered.loc[tag]),
            "borderColor": colors[i],
            "backgroundColor": colors[i],
            "fill": False,
            "tension": 0.3
        })

    return jsonify(chart_data)

if __name__ == "__main__":
    app.run(debug=True)
