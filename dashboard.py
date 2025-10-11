"""Dash application for visualizing MK-One live metrics."""
from __future__ import annotations

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import requests
import plotly.graph_objs as go

# --- Configuration ---
DATA_SOURCE = "http://127.0.0.1:5000/mkone_stream"   # example local API
REFRESH_INTERVAL_MS = 3000  # update every 3 seconds

# --- Dash setup ---
app = dash.Dash(__name__)
app.title = "MK-One Live Dashboard"

app.layout = html.Div([
    html.H1("MK-One Quantum Stream Dashboard", style={"textAlign": "center"}),

    dcc.Graph(id="theta_graph"),
    dcc.Graph(id="loss_graph"),
    dcc.Graph(id="coherence_graph"),

    dcc.Interval(id="update_timer", interval=REFRESH_INTERVAL_MS, n_intervals=0)
])


# --- Callbacks ---
@app.callback(
    [Output("theta_graph", "figure"),
     Output("loss_graph", "figure"),
     Output("coherence_graph", "figure")],
    [Input("update_timer", "n_intervals")]
)
def update_graphs(n: int):
    """Fetch metrics from the data source and update the graphs."""
    try:
        # Option A: pull from live API
        response = requests.get(DATA_SOURCE, timeout=2)
        response.raise_for_status()
        data = pd.DataFrame(response.json())

        # Option B (fallback): read from a local CSV if no server
        # data = pd.read_csv("mkone_metrics.csv")

    except Exception as exc:  # pragma: no cover - network errors handled at runtime
        print("Data source error:", exc)
        data = pd.DataFrame(
            columns=["timestamp", "quantum_theta", "loss_value", "coherence_index"]
        )

    fig_theta = go.Figure(go.Scatter(
        x=data.get("timestamp"),
        y=data.get("quantum_theta"),
        mode="lines+markers",
        name="θ"
    ))
    fig_theta.update_layout(title="Quantum θ Evolution")

    fig_loss = go.Figure(go.Scatter(
        x=data.get("timestamp"),
        y=data.get("loss_value"),
        mode="lines+markers",
        name="Loss"
    ))
    fig_loss.update_layout(title="Loss Over Time")

    fig_coh = go.Figure(go.Scatter(
        x=data.get("timestamp"),
        y=data.get("coherence_index"),
        mode="lines+markers",
        name="Coherence"
    ))
    fig_coh.update_layout(title="Coherence Index")

    return fig_theta, fig_loss, fig_coh


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
