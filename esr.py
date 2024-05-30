import numpy as np
import yaml


# def linep2dp(x: np.ndarray, y: list, yn="", title="", xaxis_title="x", yaxis_title="y") -> None:
#     """Multi-line 2D plot using plotly.
#
#     :param x: x-axis values.
#     :param yv: y-axis values.
#     :param yn: y-axis names.
#     :param title: Title of the plot.
#     :param xaxis_title: Title of the x-axis.
#     :param yaxis_title: Title of the y-axis.
#     """
#     import plotly.graph_objects as go
#
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=yn))
#     fig.update_layout(title=title, xaxis_title=xaxis_title, yaxis_title=yaxis_title)
#     fig.show()
def linep2dp(x: np.ndarray, y: list, yn="", title="", xaxis_title="x", yaxis_title="y", color="#9BB0C1") -> None:
    """Multi-line 2D plot using plotly.

    :param x: x-axis values.
    :param y: y-axis values.
    :param yn: y-axis names.
    :param title: Title of the plot.
    :param xaxis_title: Title of the x-axis.
    :param yaxis_title: Title of the y-axis.
    """
    import plotly.graph_objects as go
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=yn,
                             line=dict(width=2, color=color), marker=dict(size=7, line=dict(width=1))))

    # Update layout for a cleaner look
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        template="plotly_white",
        font=dict(family="Helvetica, Arial, sans-serif", size=12, color="black"),
        margin=dict(l=60, r=60, t=50, b=50),
        hovermode="closest",
        xaxis=dict(showline=True, showgrid=True, linecolor='black', linewidth=1, mirror=True),
        yaxis=dict(showline=True, showgrid=True, linecolor='black', linewidth=1, mirror=True)
    )

    # Show plot
    fig.show()


if __name__ == "__main__":
    with_current_flag = False
    if with_current_flag:
        append_date_text = "58-48"
        append_text = "TOP_25mA"
    else:
        append_date_text = "46-03"
        append_text = "ref"
    X = np.load(f"data/without_current/ESR_Continuous_2024-03-07-17-{append_date_text}_PCB_{append_text}_50x50.npy")
    X = np.sum(X[0] / X[1], axis=1)

    with open(f"data/without_current/ESR_Continuous_2024-03-07-17-{append_date_text}_PCB_{append_text}_50x50.yaml", "r") as f:
        cfg = yaml.safe_load(f)
        frq = cfg["frequency_values"]  # frequency values in Hz

    print(f"X: {X.shape}")
    print(f"frq: {len(frq)}")

    linep2dp(
        [f * 1e-9 for f in frq],
        X[:, 0, 0],
        title="ESR Spectrum in pixel (0,0)",
        xaxis_title="Frequency [GHz]",
        yaxis_title="Intensity",
    )
