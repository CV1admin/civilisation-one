"""Dash application for visualizing MK-One live metrics with interactive controls."""
from __future__ import annotations

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import requests

# --- Configuration ---
DATA_SOURCE = "http://127.0.0.1:5000/mkone_stream"
DEFAULT_REFRESH_MS = 3000
DEFAULT_ROLLING_WINDOW = 20


# --- Dash app setup ---
app = dash.Dash(__name__)
app.title = "MK-One Quantum Stream Dashboard"


app.layout = html.Div(
    [
        html.H1("MK-One Quantum Stream Dashboard", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("Rolling Window (samples):"),
                dcc.Slider(
                    id="window_slider",
                    min=5,
                    max=100,
                    step=5,
                    value=DEFAULT_ROLLING_WINDOW,
                    marks={i: str(i) for i in range(10, 110, 20)},
                ),
                html.Br(),
                html.Label("Refresh Interval (seconds):"),
                dcc.Slider(
                    id="refresh_slider",
                    min=1,
                    max=10,
                    step=1,
                    value=DEFAULT_REFRESH_MS // 1000,
                    marks={i: str(i) for i in range(1, 11)},
                ),
            ],
            style={"width": "80%", "margin": "auto"},
        ),
        html.Br(),
        dcc.Graph(id="theta_graph"),
        dcc.Graph(id="loss_graph"),
        dcc.Graph(id="coherence_graph"),
        dcc.Graph(id="stability_graph"),
        dcc.Graph(id="phase_heatmap"),
        dcc.Interval(id="update_timer", interval=DEFAULT_REFRESH_MS, n_intervals=0),
    ]
)


# --- Helpers ---
def _empty_figure(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        template="plotly_dark",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text="No data available",
                showarrow=False,
                font=dict(color="#AAAAAA", size=14),
            )
        ],
    )
    return fig


# --- Dynamic interval update ---
@app.callback(Output("update_timer", "interval"), Input("refresh_slider", "value"))
def update_interval(refresh_value: int) -> int:
    """Update the polling interval when the refresh slider changes."""
    return int(refresh_value) * 1000  # convert seconds to milliseconds


# --- Main graph update ---
@app.callback(
    [
        Output("theta_graph", "figure"),
        Output("loss_graph", "figure"),
        Output("coherence_graph", "figure"),
        Output("stability_graph", "figure"),
        Output("phase_heatmap", "figure"),
    ],
    Input("update_timer", "n_intervals"),
    State("window_slider", "value"),
)
def update_graphs(_n_intervals: int, rolling_window: int):
    """Fetch metrics from the data source and update the dashboard figures."""
    try:
        response = requests.get(DATA_SOURCE, timeout=2)
        response.raise_for_status()
        data = pd.DataFrame(response.json())
    except Exception as exc:  # pragma: no cover - relies on runtime data source
        print("Data source error:", exc)
        data = pd.DataFrame()

    required_columns = ["timestamp", "quantum_theta", "loss_value", "coherence_index"]
    for column in required_columns:
        if column not in data:
            data[column] = np.nan

    if data.empty:
        return [
            _empty_figure("Quantum θ Evolution"),
            _empty_figure("Loss Over Time"),
            _empty_figure("Coherence Index"),
            _empty_figure("Stability Index"),
            _empty_figure("Quantum Phase-Space: θ vs Coherence"),
        ]

    data = data[required_columns].copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    numeric_cols = [col for col in required_columns if col != "timestamp"]
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(subset=["timestamp"]).sort_values("timestamp")

    if data.empty:
        return [
            _empty_figure("Quantum θ Evolution"),
            _empty_figure("Loss Over Time"),
            _empty_figure("Coherence Index"),
            _empty_figure("Stability Index"),
            _empty_figure("Quantum Phase-Space: θ vs Coherence"),
        ]

    # --- Compute rolling correlation and stability ---
    rolling_corr = (
        data["coherence_index"].rolling(rolling_window, min_periods=2).corr(data["loss_value"])
    )
    stability_index = 0.5 * (1 - rolling_corr.clip(-1, 1))

    # --- Create figures ---
    fig_theta = go.Figure(
        go.Scatter(
            x=data["timestamp"],
            y=data["quantum_theta"],
            mode="lines+markers",
            name="θ",
        )
    )
    fig_theta.update_layout(title="Quantum θ Evolution", template="plotly_dark")

    fig_loss = go.Figure(
        go.Scatter(
            x=data["timestamp"],
            y=data["loss_value"],
            mode="lines+markers",
            name="Loss",
            line=dict(color="#d62728"),
        )
    )
    fig_loss.update_layout(title="Loss Over Time", template="plotly_dark")

    fig_coherence = go.Figure(
        go.Scatter(
            x=data["timestamp"],
            y=data["coherence_index"],
            mode="lines+markers",
            name="Coherence",
            line=dict(color="#2ca02c"),
        )
    )
    fig_coherence.update_layout(title="Coherence Index", template="plotly_dark")

    fig_stability = go.Figure(
        go.Scatter(
            x=data["timestamp"],
            y=stability_index,
            mode="lines+markers",
            name="Stability Index",
            line=dict(color="#9467bd"),
        )
    )
    fig_stability.update_layout(
        title=f"Stability Index (window={rolling_window})",
        template="plotly_dark",
        yaxis=dict(range=[0, 1]),
    )

    # --- Phase heatmap: θ vs Coherence ---
    theta_values = data["quantum_theta"].to_numpy()
    coherence_values = data["coherence_index"].to_numpy()
    valid_mask = np.isfinite(theta_values) & np.isfinite(coherence_values)

    if not np.any(valid_mask):
        fig_heatmap = _empty_figure("Quantum Phase-Space: θ vs Coherence")
    else:
        heatmap, xedges, yedges = np.histogram2d(
            theta_values[valid_mask],
            coherence_values[valid_mask],
            bins=(40, 40),
            density=True,
        )
        fig_heatmap = go.Figure(
            data=go.Heatmap(
                x=xedges[:-1],
                y=yedges[:-1],
                z=heatmap.T,
                colorscale="Viridis",
                colorbar=dict(title="Density"),
            )
        )
        fig_heatmap.update_layout(
            title="Quantum Phase-Space: θ vs Coherence",
            template="plotly_dark",
            xaxis_title="Quantum θ",
            yaxis_title="Coherence Index",
        )

    return fig_theta, fig_loss, fig_coherence, fig_stability, fig_heatmap


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
