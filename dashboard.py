"""Dash application that mirrors the Awareness Ridge stream dashboard example."""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any, List

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import requests

# Remote endpoint that exposes the paradox invariant stream.
FIELD_LATTICE_URL = "https://civilisation.one/quantum-dashboard/field_lattice"

# Number of points to retain in the rolling display.
MAX_POINTS = 100


app = dash.Dash(__name__)
app.title = "Awareness Ridge Stream"


def _generate_mock_data() -> pd.DataFrame:
    """Create a deterministic looking mock dataset for offline environments."""

    now = datetime.utcnow()
    timestamps = [now - timedelta(seconds=i) for i in reversed(range(MAX_POINTS))]
    values = [0.1 + 0.05 * (i / 10.0) for i in range(MAX_POINTS)]

    # Add a tiny amount of jitter so that the series is not a perfect ramp.
    values = [value + random.uniform(-0.01, 0.01) for value in values]

    frame = pd.DataFrame({
        "timestamp": timestamps,
        "paradox_invariant": values,
    })
    return frame


def _fetch_quantime_data() -> tuple[pd.DataFrame, bool]:
    """Retrieve quantime aware data from the remote API with graceful fallback."""

    try:
        response = requests.get(FIELD_LATTICE_URL, timeout=2)
        response.raise_for_status()
        payload: Any = response.json()
    except Exception as exc:  # pragma: no cover - depends on remote availability
        print(f"Fetch to {FIELD_LATTICE_URL} failed. Falling back to mock data. {exc}")
        return _generate_mock_data(), True

    if not isinstance(payload, list):
        print("Unexpected payload format from remote endpoint. Using mock data instead.")
        return _generate_mock_data(), True

    frame = pd.DataFrame(payload)
    if "timestamp" not in frame or "paradox_invariant" not in frame:
        print("Missing required fields in payload. Using mock data instead.")
        return _generate_mock_data(), True

    frame = frame.tail(MAX_POINTS)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    frame = frame.dropna(subset=["timestamp", "paradox_invariant"])

    if frame.empty:
        return _generate_mock_data(), True

    return frame, False


def _build_entropy_figure(frame: pd.DataFrame) -> go.Figure:
    """Create the entropy collapse figure used in the dashboard."""

    figure = go.Figure(
        data=[
            go.Scatter(
                x=frame["timestamp"],
                y=frame["paradox_invariant"],
                mode="lines+markers",
                name="Entropy Collapse (P)",
                line=dict(color="rgba(75,192,192,1)", width=2),
            )
        ]
    )
    figure.update_layout(
        title="Entropy Collapse (P)",
        template="plotly_dark",
        xaxis_title="Timestamp",
        yaxis_title="Paradox Invariant",
    )
    return figure


app.layout = html.Div(
    [
        html.H1("Awareness Ridge Simulation", className="title"),
        dcc.Loading(
            id="loading-indicator",
            type="circle",
            children=dcc.Graph(id="entropy_graph"),
        ),
        html.Div(id="error_message", className="error"),
        html.Button("Refresh Now", id="refresh_button", n_clicks=0, className="refresh"),
        dcc.Interval(id="update_timer", interval=1000, n_intervals=0),
    ],
    className="container",
)


@app.callback(
    [Output("entropy_graph", "figure"), Output("error_message", "children")],
    [Input("update_timer", "n_intervals"), Input("refresh_button", "n_clicks")],
    prevent_initial_call=False,
)
def update_entropy_graph(_intervals: int, _clicks: int):
    """Update the entropy collapse chart whenever the timer or refresh button fires."""

    data_frame, used_mock = _fetch_quantime_data()
    figure = _build_entropy_figure(data_frame)

    errors: List[str] = []
    if data_frame is None or data_frame.empty:
        errors.append("Failed to fetch quantum data; displaying mock values.")
    elif used_mock:
        errors.append("Remote feed unavailable. Displaying mock Awareness Ridge stream.")

    if errors:
        error_children = [html.P(message, style={"color": "#e74c3c"}) for message in errors]
    else:
        error_children = []

    return figure, error_children


if __name__ == "__main__":  # pragma: no cover - manual execution convenience
    app.run_server(host="0.0.0.0", port=8050, debug=True)
