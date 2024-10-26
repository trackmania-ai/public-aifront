# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/overlay_session.ipynb.

# %% auto 0
__all__ = ['session_overlay']

# %% ../../nbs/overlay_session.ipynb 1
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from .default import background_color, table
from .medal import medal_icon, pb_with_icon, racetime2str
from dash import dcc, html
from fastcore.foundation import L, Self

# %% ../../nbs/overlay_session.ipynb 2
medal_colors = dict(
    author="rgb(0, 119, 17)",
    gold="rgb(221, 187, 68)",
    silver="rgb(136, 153, 153)",
    bronze="rgb(153, 102, 68)",
    no_medal="white",
    unfinished="rgb(242, 71, 64)",
)

medal_labels = dict(
    author="Author",
    gold="Gold",
    silver="Silver",
    bronze="Bronze",
    no_medal="No medal",
    unfinished="Unfinished",
)

font = dict(
    size=16,
    family='Lato,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
)


def session_medal_figure(sessions):
    fig = go.Figure()
    first = len(sessions) == 1
    for medal, color in medal_colors.items():
        y = list(map(lambda o: o["finishes"][medal], sessions.values()))
        x = list(sessions.keys())
        if first:
            y *= 2
            x = None
        fig.add_trace(
            go.Scatter(
                y=y,
                x=x,
                mode="lines",
                line=dict(width=0.5, color=color),
                fillcolor=color,
                stackgroup="one",
                name=medal_labels[medal],
            )
        )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=font,
        template="plotly_dark",
        xaxis=dict(showgrid=False, showticklabels=not first),
        yaxis=dict(showgrid=False),
        margin=dict(pad=10, l=0, r=0, b=0, t=0),
        height=176,
    )
    return fig


def summary(medals, stats):
    nb_round = sum(stats["finishes"].values())
    return (
        *[
            [
                f"{count} ",
                html.Span(
                    f" {count/nb_round*100:.1f} %",
                    style={"font-size": ".7em", "color": "lightskyblue"},
                ),
            ]
            for count in stats["finishes"].values()
        ],
        str(nb_round),
        pb_with_icon(medals, stats["best"]),
    )

# %% ../../nbs/overlay_session.ipynb 3
def session_overlay(data):
    headers = [
        "",
        [html.Span("#", className="me-2"), medal_icon("unfinished")],
        [html.Span("#", className="me-2"), medal_icon("no_medal")],
        [html.Span("#", className="me-2"), medal_icon("bronze")],
        [html.Span("#", className="me-2"), medal_icon("silver")],
        [html.Span("#", className="me-2"), medal_icon("gold")],
        [html.Span("#", className="me-2"), medal_icon("author")],
        "# Round",
        "Personal Best",
    ]
    medals = data["config"]["map"]["medals"]
    session_stats = data["stats"]["sessions"][str(data["stats"]["current_session"])]
    rows = [
        [
            f"Session {data['stats']['current_session']}",
            *summary(medals, session_stats),
        ],
        ["Map overall", *summary(medals, data["stats"]["overall"])],
    ]
    graph_name = html.P(
        "Result per session",
        className="p-0",
    )
    graph_fig = dcc.Graph(
        figure=session_medal_figure(data["stats"]["sessions"]),
        config={"displayModeBar": False},
        className="p-0 m-0",
    )
    return dbc.Badge(
        [
            html.P("Result count", className="p-0 pt-2"),
            table(headers, rows),
            graph_name,
            graph_fig,
        ],
        color=background_color,
        style={"border-radius": "1rem"},
    )