import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Updated function to include VaR, ES, and Expected Return lines
def plot_histogram_with_risk_lines(returns, var, es):
    if isinstance(returns, pd.DataFrame):
        returns = returns.squeeze()

    df = pd.DataFrame({'Returns': returns})
    fig = px.histogram(df, x='Returns', nbins=50,
                       #title="Histogram of Returns with VaR, ES, and Expected Return",
                       labels={'Returns': 'Return'},
                       color_discrete_sequence=['skyblue'])

    # Calculate expected return
    expected_return = returns.mean()

    # Add vertical lines for VaR, ES, and Expected Return
    fig.add_vline(x=-var, line_dash="dash", line_color="red", annotation_text="VaR", annotation_position="top left")
    fig.add_vline(x=-es, line_dash="dot", line_color="orange", annotation_text="ES", annotation_position="top left")
    fig.add_vline(x=expected_return, line_dash="solid", line_color="green", annotation_text="Expected Return", annotation_position="top")

    fig.update_layout(bargap=0.1)
    return fig


# =========================
# Candlestick Plotter
# =========================
def plot_candlestick(
    prices_df: pd.DataFrame,
    symbol: str | None = None,
    interval: str | None = None,
    add_volume: bool = True,
    height: int = 450,
    template: str = "plotly_white",
) -> go.Figure:
    """
    Create a candlestick chart (with optional volume panel).

    Parameters
    ----------
    prices_df : pd.DataFrame
        DataFrame indexed by datetime with columns: Open, High, Low, Close, (optional) Volume.
    symbol : str | None
        Ticker symbol to show in the title (optional).
    interval : str | None
        Interval label (e.g., 'Daily', 'Weekly', 'Monthly') to show in the title (optional).
    add_volume : bool
        If True and 'Volume' exists, adds a volume bar panel.
    height : int
        Figure height in pixels.
    template : str
        Plotly template (e.g., 'plotly_white', 'plotly_dark').

    Returns
    -------
    go.Figure
        Plotly figure object.
    """
    if prices_df is None or prices_df.empty:
        raise ValueError("prices_df is empty.")

    df = prices_df.copy()

    # Ensure datetime index
    if not isinstance(df.index, (pd.DatetimeIndex, pd.PeriodIndex)):
        df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Normalize column names
    col_map = {c.lower(): c for c in df.columns}
    def _get(col_name: str) -> str:
        return col_map[col_name.lower()] if col_name.lower() in col_map else None

    open_col  = _get("Open")
    high_col  = _get("High")
    low_col   = _get("Low")
    close_col = _get("Close")
    vol_col   = _get("Volume")

    if any(c is None for c in [open_col, high_col, low_col, close_col]):
        raise ValueError("Missing required OHLC columns: Open, High, Low, Close")

    # Convert numeric columns
    for c in [open_col, high_col, low_col, close_col, vol_col]:
        if c and df[c].dtype.kind not in "biufc":
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Figure spec
    show_volume = add_volume and (vol_col in df.columns)
    if show_volume:
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
            row_heights=[0.72, 0.28], specs=[[{"type": "xy"}], [{"type": "bar"}]]
        )
    else:
        fig = make_subplots(rows=1, cols=1, specs=[[{"type": "xy"}]])

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df[open_col],
            high=df[high_col],
            low=df[low_col],
            close=df[close_col],
            name="OHLC",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350",
            increasing_fillcolor="#26a69a",
            decreasing_fillcolor="#ef5350",
        ),
        row=1, col=1
    )

    # Volume panel
    if show_volume:
        colors = ["#26a69a" if c >= o else "#ef5350" for o, c in zip(df[open_col], df[close_col])]
        fig.add_trace(
            go.Bar(x=df.index, y=df[vol_col], marker_color=colors, name="Volume", opacity=0.7),
            row=2, col=1
        )
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
    else:
        fig.update_yaxes(title_text="Price", row=1, col=1)

    # Range selector + slider
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                #dict(count=1, label="1m", step="month", stepmode="backward"),
                #dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date",
        row=1, col=1
    )
    # ✅ Auto-scale Y-axis
    fig.update_yaxes(autorange=True, row=1, col=1)

    # Layout
    title_parts = [p for p in [symbol, interval] if p]
    title_text = " — ".join(title_parts) + (" Candlestick" if title_parts else "Candlestick")

    fig.update_layout(
        template=template,
        title=title_text,
        legend=dict(orientation="h", yanchor="bottom", y=1.10, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=60, b=40),
        height=height,
        xaxis_rangeslider_thickness=0.06,
    )

    return fig


