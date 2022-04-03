import plotly.graph_objects as go
import plotly.express as px

# fig = go.Figure(go.Scattergeo())
# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# fig = go.Figure(go.Scattergeo())
# fig.update_geos(projection_type="natural earth")
# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# fig = go.Figure(go.Scattergeo())
# fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

from math import pi
from math import tanh
from math import sin
from math import asin
from numpy import arctanh
import numpy as np
import pandas as pd

# refer from http://www.trail-note.net/tech/coordinate/

a_k = 6378137
a = 6371000
e2 = 0.00669438002290


def hirvonen(x, y, z):
    eps = np.deg2rad(0.00005 / 60**2)
    r = np.sqrt(x * x + y * y)
    phi = np.arctan(z / (r * (1 - e2)))
    while (1):
        N = a / np.sqrt(1 - e2 * np.sin(phi) ** 2)
        h = r / np.cos(phi) - N
        new_phi = np.arctan(z / r / (1 - e2 * (N / (N + h))))
        if (abs(new_phi - phi) < eps):
            phi = new_phi
            break
        else:
            phi = new_phi

    lam = np.arctan(y / x)
    return np.degrees(phi), np.degrees(lam), h

if __name__ == "__main__":
    print(hirvonen(18413883.182788137, -8185394.67936962, 17201832.968270725))

    # lat = [40.53092247141685, 35.1300848947277, 29.425055383494524, 23.51148727639027, 17.458884814772478, 11.319359090520301, 5.133872546774054, -1.0632522502383572, -7.240862345013485, -13.367982743101813, -19.41082758955506, -25.32934849169561, -31.072797275278194, -36.57369422969858, -41.739614903462744, -46.44276346242845, -50.50944869406837, -53.717071130180535, -55.814830849135724, -56.58481149681498, -55.928826321659294, -53.91711268262511, -50.751128718302915, -46.67809305619648, -41.92455608332986, -36.67072840988449, -31.05109841621198, -25.16428492956994, -19.08349445583368, -12.864949176852173, -6.554137922261609, -0.1904417609376446, 6.1892408916875645, 12.547312086689024, 18.84222247230049, 25.02461358873043, 31.032222458905103, 36.782794201605604, 42.16429590278341, 47.022577967220954, 51.14988094646091, 54.285636179821445, 56.15189684124962, 56.5391327848667, 55.40524720724784, 52.90004863313968, 49.28856220295486, 44.849524663791286, 39.8171001881929, 34.36792500576997, 28.629532865033614, 22.69338922624784, 16.62617584098595, 10.478163467368809, 4.289173872288475, -1.907090699935514, -8.07967283998553, -14.197395713660244, -20.22583921122373, -26.123786616271722, -31.838607523001542, -37.29995942452855, -42.41125009300405, -47.03899371143404, -51.00268868047704, -54.07389647263475, -56.00174065025489, -56.579540632220066, -55.73094920109054, -53.548111069230245, -50.24390312867154, -46.065707344534964, -41.23446833644389, -35.92378084643231, -30.262596990551796, -24.345491062236476, -18.242910899143066, -12.009290716897167, -5.689043141453437, 0.6789871754134997, 7.057990065721923, 13.410028066386381, 19.692734973197233, 25.855329471893654, 31.833294814669575, 37.5409590207932, 42.86131471379154, 47.633476107628276, 51.64193924678985, 54.62060028112731, 56.29476220521944, 56.472605827055325, 55.13929899459947, 52.46646928828373, 48.72641553735111, 44.19400945644544, 39.095610778929235]
    lat_1 = [40.53092247141685, 35.1300848947277, 29.425055383494524, 23.51148727639027, 17.458884814772478, 11.319359090520301, 5.133872546774054, -1.0632522502383572, -7.240862345013485, -13.367982743101813, -19.41082758955506, -25.32934849169561, -31.072797275278194, -36.57369422969858, -41.739614903462744, -46.44276346242845, -50.50944869406837, -53.717071130180535, -55.814830849135724, -56.58481149681498, -55.928826321659294, -53.91711268262511, -50.751128718302915, -46.67809305619648, -41.92455608332986, -36.67072840988449, -31.05109841621198, -25.16428492956994, -19.08349445583368, -12.864949176852173, -6.554137922261609, -0.1904417609376446, 6.1892408916875645, 12.547312086689024, 18.84222247230049, 25.02461358873043, 31.032222458905103, 36.782794201605604, 42.16429590278341, 47.022577967220954, 51.14988094646091, 54.285636179821445, 56.15189684124962, 56.5391327848667, 55.40524720724784, 52.90004863313968, 49.28856220295486, 44.849524663791286, 39.8171001881929, 34.36792500576997, 28.629532865033614, 22.69338922624784, 16.62617584098595, 10.478163467368809, 4.289173872288475, -1.907090699935514, -8.07967283998553, -14.197395713660244, -20.22583921122373, -26.123786616271722, -31.838607523001542, -37.29995942452855, -42.41125009300405, -47.03899371143404, -51.00268868047704, -54.07389647263475, -56.00174065025489, -56.579540632220066, -55.73094920109054, -53.548111069230245, -50.24390312867154, -46.065707344534964, -41.23446833644389, -35.92378084643231, -30.262596990551796, -24.345491062236476, -18.242910899143066, -12.009290716897167, -5.689043141453437, 0.6789871754134997, 7.057990065721923, 13.410028066386381, 19.692734973197233, 25.855329471893654, 31.833294814669575, 37.5409590207932, 42.86131471379154, 47.633476107628276, 51.64193924678985, 54.62060028112731, 56.29476220521944, 56.472605827055325, 55.13929899459947, 52.46646928828373, 48.72641553735111, 44.19400945644544, 39.095610778929235]
    lon_1 = [23.966246443706332, 26.886236969540168, 28.936421792494002, 30.342572569509016, 31.285796841722416, 31.911871548333618, 32.341682343653005, 32.68059518547358, 33.02660343506248, 33.47774233439213, 34.139414644455954, 35.1322234325298, 36.60064111547257, 38.72202644253121, 41.7132716865112, 45.82701857486187, 51.31902303876518, 58.356611088118875, 66.85203490991087, 76.29724592366676, 85.80711395459346, -85.53121632921639, -78.28307854987585, -72.58238069119507, -68.28324588518296, -65.13376974106923, -62.87716367277442, -61.29002154534728, -60.188387624252215, -59.4216863005832, -58.86358044226804, -58.40291572483515, -57.93538636395788, -57.35561542483816, -56.549036065048114, -55.38293579740134, -53.69631157871452, -51.289235052298515, -47.91547408931179, -43.289619179802166, -37.134362888198574, -29.30708499200644, -20.01235375355439, -9.96051837155793, -0.2029587885835992, 8.346494350786577, 15.255997855881194, 20.53665082107201, 24.424896616048002, 27.21128580377945, 29.16146672165481, 30.49475842545448, 31.386834863755773, 31.979480530332747, 32.390944368034525, 32.725130606397414, 33.07961066622977, 33.55298709990975, 34.25225624554546, 35.30074574089383, 36.84688923788374, 39.073157399310745, 42.20193112530014, 46.489162506835406, 52.18564105421567, 59.43515262416642, 68.10026392588622, 77.61168736435785, 87.05490693659635, -84.45307598423261, -77.41627584146941, -71.91909819163594, -67.79230152596384, -64.77909027775054, -62.625982331852256, -61.11501063988202, -60.067253022213805, -59.335990322907804, -58.797472100970865, -58.34195345529196, -57.86544625386113, -57.26181130461601, -56.4145608468841, -55.18774930928276, -53.41568125725608, -50.89239301900314, -47.36534445107454, -42.546109939989, -36.16607820459297, -28.11625387065739, -18.665247725405237, -8.58917864338792, 1.048605837547921, 9.388202390863546, 16.06767104233046, 21.142084909563785, 24.863125740737548]

    lat_2 = [4.1585401805852165, 10.324985514163387, 16.39747823963566, 22.335983818267444, 28.093047949932835, 33.60892017144639, 38.80522424462384, 43.57712088509342, 47.785169329253804, 51.251233009736865, 53.768091585648044, 55.1353531921709, 55.22164039509618, 54.020503322048285, 51.65381123645308, 48.31935102401461, 44.22696023646249, 39.559269719421934, 34.4598659481832, 29.036549685896627, 23.369391522937878, 17.51873808456629, 11.531732854701753, 5.44733004831965, -0.699798389609463, -6.8759998265945885, -13.045577939002861, -19.16748316910765, -25.191252749969056, -31.051584704973887, -36.6608255712977, -41.89879910160122, -46.60054282404126, -50.54634560223758, -53.467006774968674, -55.08649190400836, -55.2116353258615, -53.82313468127843, -51.08551061973849, -47.26572286091859, -42.637949419939645, -37.431948783664396, -31.82260588670831, -25.938250396750803, -19.87288350235391, -13.696749488756769, -7.4642494138409665, -1.2196660981395626, 4.998574832082278, 11.154464587581838, 17.21126192458809, 23.128169658733327, 28.85638091981767, 34.334027101638235, 39.47963201783516, 44.18411778586091, 48.3028606430104, 51.65275838213144, 54.02471584045943, 55.22369435709858, 55.13273245227536, 53.76407259853137, 51.25374846439687, 47.80459379417161, 43.62435836785247, 38.89060018127891, 33.74167731992568, 28.281131169063215, 22.585917133346, 16.714246416328805, 10.711888007855663, 4.617005756354941, -1.5360487953554633, -7.713526174750473, -13.879209355827387, -19.991034017164395, -25.99688237016416, -31.828917701824945, -37.39573525671102, -42.57182720507063, -47.185238981516726, -51.008666380519294, -53.76838448810943, -55.19351404661719, -55.110136244561815, -53.52574903537019, -50.624788556532394, -46.68009166616552, -41.961713841014856, -36.69194909984582, -31.038694760444102, -25.124919597225876, -19.04084443658794, -12.854158192907326, -6.617594813043369, -0.37441779686178017, 5.837464886414679]
    lon_2 = [56.05715620607514, 56.65023146333554, 57.39155400222359, 58.39398505276933, 59.786807501473305, 61.72294536413175, 64.38431264305946, 67.9802909923842, 72.72820800079363, 78.79707520787444, 86.19872646782143, -85.3468114273926, -76.45712856649445, -67.91907115366568, -60.38203338950851, -54.16502673107823, -49.282804742545736, -45.57787011328681, -42.83496864427945, -40.842811732867176, -39.41671288009741, -38.401481969410646, -37.66657941403994, -37.099070810468916, -36.596393192513446, -36.05934437094081, -35.385051700941176, -34.45943973389854, -33.14872163980548, -31.289802853975903, -28.680743130932477, -25.075889009202385, -20.198326489833537, -13.796243301910486, -5.778088008344455, 3.584198145003962, 13.541832636435688, 23.08081932566077, 31.377963536433708, 38.07724181506893, 43.22060918846665, 47.04397469779885, 49.826089301087805, 51.82042904852845, 53.237305073985546, 54.246926530718206, 54.98865446772173, 55.58081313708819, 56.12951426931847, 56.73647750199834, 57.50629406068264, 58.5536167031057, 60.01052391921081, 62.03363648288915, 64.80893053796619, 68.5486003201287, 73.46779296739635, 79.72176898600297, 87.29031876558003, -84.15349513806063, -75.26520798991929, -66.83114949742927, -59.46218785529206, -53.43053272410843, -48.71935334472776, -45.15776691296693, -42.52853148977749, -40.623249360113334, -39.261323289474156, -38.291273441616944, -37.58537441301852, -37.03251660121278, -36.530999655363274, -35.98154148757121, -35.28020952699172, -34.31078076625485, -32.936077335349346, -30.988265129880556, -28.259560234888387, -24.498715211119723, -19.42751145134403, -12.805888991084005, -4.579181631231979, 4.917504816618249, 14.878442588149419, 24.28813163168948, 32.37880870046645, 38.85832528484683, 43.806842335969954, 47.472890280970574, 50.134280854589655, 52.03899015214782, 53.39147815851779, 54.35718575397613, 55.07206371459855, 55.65228934122789, 56.2029385373965]

    lat = [lat_1, lat_2]
    lon = [lon_1, lon_2]
    import plotly.graph_objects as go
    fig = go.Figure()
    for i in range(len(lat)):
        lat_iterated = lat[i]
        lon_iterated = lon[i]
        fig.add_trace(
            go.Scattergeo(
                lon=lon_iterated,
                lat=lat_iterated,
                mode='lines',
                name=f"{i+1}"
            )
        )
        fig.update_layout(
            geo=dict(
                projection=dict(
                    type='orthographic'
                ),
                lonaxis=dict(
                    showgrid=True,
                    gridcolor='rgb(102, 102, 102)',
                    gridwidth=0.5
                ),
                lataxis=dict(
                    showgrid=True,
                    gridcolor='rgb(102, 102, 102)',
                    gridwidth=0.5
                )
            )
        )
    fig.show()

