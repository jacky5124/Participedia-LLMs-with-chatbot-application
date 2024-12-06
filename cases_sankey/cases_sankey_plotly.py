from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Supply chain of the energy production'),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"),
    Input('dummy_input', 'value'),)
def display_sankey(dummy_input):
    node = dict(
      label = ["A1", "A2", "B1", "B2", "C1", "C2"],
    )

    link = dict(
      source = [0, 1, 0, 2, 3, 3],
      target = [2, 3, 3, 4, 4, 5],
      value = [8, 4, 2, 8, 4, 2]
    )

    fig = go.Figure(go.Sankey(link=link, node=node))
    fig.update_layout(font_size=10)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
