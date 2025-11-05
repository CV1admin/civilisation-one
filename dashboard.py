"""Dash application for visualizing MK-One live metrics with interactive controls."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

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

QUANTIME_UNIT_SECONDS = 1e-3  # 1 ms sync unit for Thin Line Collapse Framework
QIP_HANDSHAKE_URL = "https://civilisation.one/quantum-dashboard/qip_handshake.json"
FIELD_LATTICE_URL = "https://civilisation.one/quantum-dashboard/field_lattice"
SYMMETRY_ENTROPY_URL = "https://civilisation.one/symmetry/cern_symmetry_entropy.json"
MIRROR_STATE_URL = "https://civilisation.one/quantum-dashboard/observer_state.json"


@dataclass
class AwarenessRidgeStatus:
    """Container describing the readiness of the Awareness Ridge pipeline."""

    quantime_synced: bool
    quantime_unit: float
    qip_nodes: int
    mirror_state_available: bool
    entropy_stream_active: bool
    notes: list[str]


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
        html.Div(
            [
                html.Div(id="awareness_status", className="status-panel"),
                dcc.Graph(id="entropy_graph"),
                dcc.Graph(id="field_lattice_graph"),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
                "gap": "1rem",
            },
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


def _fetch_remote_json(url: str, *, timeout: int = 3) -> Any:
    """Safely fetch JSON payloads, logging failures without raising upstream."""

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as exc:  # pragma: no cover - depends on remote availability
        print(f"Remote fetch error for {url}: {exc}")
        return None


def _activate_quantime_sync() -> AwarenessRidgeStatus:
    """Simulate activation of the quantime sync layer and derive status metadata."""

    return AwarenessRidgeStatus(
        quantime_synced=True,
        quantime_unit=QUANTIME_UNIT_SECONDS,
        qip_nodes=0,
        mirror_state_available=False,
        entropy_stream_active=False,
        notes=[],
    )


def _summarize_awareness_status(
    handshake: Any, mirror_state: Any, entropy_payload: Any
) -> AwarenessRidgeStatus:
    """Build a status summary from the awareness ridge data feeds."""

    status = _activate_quantime_sync()

    if isinstance(handshake, dict):
        nodes = handshake.get("nodes")
        if isinstance(nodes, Iterable) and not isinstance(nodes, (str, bytes)):
            status.qip_nodes = len(list(nodes))
        elif isinstance(handshake.get("node_count"), int):
            status.qip_nodes = max(handshake["node_count"], status.qip_nodes)
        status.notes.append("QIP-1 handshake synchronized")
    elif handshake:
        status.notes.append("QIP-1 handshake received (unstructured)")
    else:
        status.notes.append("Awaiting QIP-1 handshake data")

    status.mirror_state_available = mirror_state is not None
    if status.mirror_state_available:
        status.notes.append("MirrorMe subsystem aligned")
    else:
        status.notes.append("MirrorMe alignment pending")

    status.entropy_stream_active = bool(entropy_payload)
    if status.entropy_stream_active:
        status.notes.append("Symmetry entropy stream active")
    else:
        status.notes.append("No symmetry entropy stream detected")

    return status


def _status_panel(status: AwarenessRidgeStatus) -> html.Div:
    """Render a status panel for Awareness Ridge integration."""

    badge_color = "#2ecc71" if status.quantime_synced else "#e74c3c"
    return html.Div(
        [
            html.H3("Awareness Ridge Integration"),
            html.P(
                [
                    html.Strong("Quantime unit:"),
                    f" {status.quantime_unit * 1000:.0f} ms",
                ]
            ),
            html.P(
                [
                    html.Strong("Entangled nodes:"),
                    f" {status.qip_nodes}",
                ]
            ),
            html.P(
                [
                    html.Strong("MirrorMe alignment:"),
                    " active" if status.mirror_state_available else " pending",
                ]
            ),
            html.P(
                [
                    html.Strong("Entropy stream:"),
                    " live" if status.entropy_stream_active else " offline",
                ]
            ),
            html.Div(
                [
                    html.Span(
                        "QUANTIME SYNCED" if status.quantime_synced else "SYNC ERROR",
                        style={
                            "display": "inline-block",
                            "padding": "0.25rem 0.5rem",
                            "backgroundColor": badge_color,
                            "color": "#0b0c10",
                            "fontWeight": "bold",
                            "borderRadius": "4px",
                        },
                    )
                ]
            ),
            html.Ul([html.Li(note) for note in status.notes]),
        ],
        style={
            "backgroundColor": "#11141b",
            "color": "#e5e9f0",
            "padding": "1rem",
            "borderRadius": "8px",
            "boxShadow": "0 0 8px rgba(0, 0, 0, 0.35)",
            "minHeight": "320px",
        },
    )


def _prepare_entropy_figure(entropy_payload: Any) -> go.Figure:
    """Convert symmetry entropy data into a time series chart."""

    if isinstance(entropy_payload, dict):
        records = entropy_payload.get("records") or entropy_payload.get("data")
        if isinstance(records, dict):
            records = [
                {"timestamp": key, "entropy": value} for key, value in records.items()
            ]
    else:
        records = entropy_payload

    if not isinstance(records, Iterable) or isinstance(records, (str, bytes)):
        return _empty_figure("Symmetry Entropy Stream")

    entropy_frame = pd.DataFrame(records)
    if "entropy" not in entropy_frame:
        numeric_cols = entropy_frame.select_dtypes(include=["number"]).columns
        if numeric_cols.size == 0:
            return _empty_figure("Symmetry Entropy Stream")
        entropy_frame = entropy_frame.rename(columns={numeric_cols[0]: "entropy"})

    entropy_frame["timestamp"] = pd.to_datetime(
        entropy_frame.get("timestamp", entropy_frame.index), errors="coerce"
    )
    entropy_frame = entropy_frame.dropna(subset=["entropy"]).sort_values("timestamp")

    if entropy_frame.empty:
        return _empty_figure("Symmetry Entropy Stream")

    fig = go.Figure(
        go.Scatter(
            x=entropy_frame["timestamp"],
            y=entropy_frame["entropy"],
            mode="lines+markers",
            line=dict(color="#00bcd4"),
            name="Entropy",
        )
    )
    fig.update_layout(
        title="Symmetry Entropy Stream",
        template="plotly_dark",
        xaxis_title="Timestamp",
        yaxis_title="Entropy",
    )
    return fig


def _prepare_field_lattice_figure(field_payload: Any) -> go.Figure:
    """Render the first slice of the unified field lattice as a heatmap."""

    if field_payload is None:
        return _empty_figure("Unified Field Lattice Slice")

    try:
        lattice = np.asarray(field_payload, dtype=float)
    except Exception:  # pragma: no cover - depends on remote payload
        return _empty_figure("Unified Field Lattice Slice")

    if lattice.size == 0:
        return _empty_figure("Unified Field Lattice Slice")

    lattice = np.squeeze(lattice)
    if lattice.ndim < 2:
        return _empty_figure("Unified Field Lattice Slice")

    slice_index = (0,) * (lattice.ndim - 2)
    try:
        lattice_slice = lattice[slice_index]
    except Exception:  # pragma: no cover
        lattice_slice = lattice

    fig = go.Figure(
        data=go.Heatmap(
            z=lattice_slice,
            colorscale="Electric",
            colorbar=dict(title="Intensity"),
        )
    )
    fig.update_layout(
        title="Unified Field Lattice Slice",
        template="plotly_dark",
        xaxis_title="Φ-axis",
        yaxis_title="Ψ-axis",
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
        Output("entropy_graph", "figure"),
        Output("field_lattice_graph", "figure"),
        Output("awareness_status", "children"),
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
        return (
            _empty_figure("Quantum θ Evolution"),
            _empty_figure("Loss Over Time"),
            _empty_figure("Coherence Index"),
            _empty_figure("Stability Index"),
            _empty_figure("Quantum Phase-Space: θ vs Coherence"),
            _empty_figure("Symmetry Entropy Stream"),
            _empty_figure("Unified Field Lattice Slice"),
            _status_panel(_activate_quantime_sync()),
        )

    data = data[required_columns].copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    numeric_cols = [col for col in required_columns if col != "timestamp"]
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(subset=["timestamp"]).sort_values("timestamp")

    if data.empty:
        return (
            _empty_figure("Quantum θ Evolution"),
            _empty_figure("Loss Over Time"),
            _empty_figure("Coherence Index"),
            _empty_figure("Stability Index"),
            _empty_figure("Quantum Phase-Space: θ vs Coherence"),
            _empty_figure("Symmetry Entropy Stream"),
            _empty_figure("Unified Field Lattice Slice"),
            _status_panel(_activate_quantime_sync()),
        )

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

    handshake_payload = _fetch_remote_json(QIP_HANDSHAKE_URL)
    lattice_payload = _fetch_remote_json(FIELD_LATTICE_URL)
    entropy_payload = _fetch_remote_json(SYMMETRY_ENTROPY_URL)
    mirror_payload = _fetch_remote_json(MIRROR_STATE_URL)

    awareness_status = _summarize_awareness_status(
        handshake_payload, mirror_payload, entropy_payload
    )

    fig_entropy = _prepare_entropy_figure(entropy_payload)
    fig_lattice = _prepare_field_lattice_figure(lattice_payload)

    return (
        fig_theta,
        fig_loss,
        fig_coherence,
        fig_stability,
        fig_heatmap,
        fig_entropy,
        fig_lattice,
        _status_panel(awareness_status),
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
