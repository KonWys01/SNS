import plotly.graph_objects as go


def plot_skyplot(sat_positions):
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
                mode='text',
                name=f'{sat_name[i]}',
                showlegend=True,
                textfont={'color': 'red', 'family': 'Open Sans', 'size': 20}
            )
        )
    fig2.update_layout(polar=dict(
            angularaxis=dict(
                thetaunit="degrees",
                dtick=45,
                rotation=90,
                direction='clockwise'),
            radialaxis=dict(
                range=[90, 1])
        ),
        height=700,
    )

    return fig2


if __name__ == '__main__':
    sat_positions = [['PG01', 10, 180], ['PG02', 60, 0], ['PG03', 45, 45], ['aaa', 10, 20]]
    sat_positions = [['1', 77.62711378329583, 170.6895434437375], ['3', 61.56419691979273, -85.51834314139667], ['4', 25.06866189540274, -155.15494409715765], ['17', 35.17277739297688, -62.550905805895134], ['19', 21.889469975387186, -41.95253939394922], ['21', 50.69945839707221, 150.64876689258932], ['22', 42.82713316370344, 58.90587851638184], ['30', 26.6411800981361, 96.1308329350198], ['31', 25.914291728489115, 50.70929132249552]]

    fig = plot_skyplot(sat_positions)
    fig.show()