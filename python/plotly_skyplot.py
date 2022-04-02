import plotly.graph_objects as go


def plot_skyplot(sat_positions):
    sat_name = []
    elevations = []
    azymutes = []
    for name, el, az in sat_positions:
        elevations.append(el)
        azymutes.append(az)
        sat_name.append(name)

    fig2 = go.Figure(data=
        go.Scatterpolar(
            r=elevations,
            theta=azymutes,
            text=sat_name,
            mode='text',
            name='Satelity',
            showlegend=True,
        ))
    fig2.update_layout(polar=dict(
            angularaxis=dict(
                thetaunit="degrees",
                dtick=45,
                rotation=90,
                direction='clockwise'),
            radialaxis=dict(
                range=[90, 1])
        ), width=700,
        height=700)
    # fig2.show()
    return fig2


if __name__ == '__main__':
    sat_positions = [['PG01', 10, 180], ['PG02', 60, 0], ['PG03', 45, 45], ['aaa', 10, 20]]
    fig = plot_skyplot(sat_positions)
    fig.show()