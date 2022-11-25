from typing import List

import plotly.graph_objects as go


def plot_skyplot(sat_positions: List) -> go.Figure:
    sat_name = []
    elevations = []
    azymutes = []
    for name, el, az in sat_positions:
        elevations.append(el)
        azymutes.append(az)
        sat_name.append(name)
    fig2 = go.Figure()
    for i in range(len(sat_positions)):
        fig2.add_trace(
            go.Scatterpolar(
                r=[elevations[i]],
                theta=[azymutes[i]],
                text=[sat_name[i]],
                mode="text",
                name=f"{sat_name[i]}",
                showlegend=True,
                textfont={"color": "red", "family": "Open Sans", "size": 20},
            )
        )
    fig2.update_layout(
        polar=dict(
            angularaxis=dict(
                thetaunit="degrees", dtick=45, rotation=90, direction="clockwise"
            ),
            radialaxis=dict(range=[90, 1]),
        ),
        height=700,
    )

    return fig2
