from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from collections import Counter


dataset = pd.read_csv('./cases_filled.csv')

input_type_columns = [
    {'label': 'Purpose', 'value': 'purposes_1'},
    {'label': 'General Issue', 'value': 'general_issues_1'}
]

process_type_columns = [
    {'label': 'Participant Interaction', 'value': 'participants_interactions_1'},
    {'label': 'Decision Method', 'value': 'decision_methods_1'}
]

outcome_type_columns = [
    {'label': 'Change', 'value': 'change_types_1'},
    {'label': 'Implementer of Change', 'value': 'implementers_of_change_1'}
]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div([
        html.H4('Input-Process-Outcome Modeling: Participation Method Effectiveness'),
        dcc.Graph(id="graph"),
        html.H5('Input, Process, and Outcome Types'),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('Input Type', htmlFor='input-type'),
                    dcc.Dropdown(
                        id='input-type',
                        options=input_type_columns,
                        value=input_type_columns[0]['value'],
                    )
                ])),
            dbc.Col(
                html.Div([
                    html.Label('Process Type', htmlFor='process-type'),
                    dcc.Dropdown(
                        id='process-type',
                        options=process_type_columns,
                        value=process_type_columns[0]['value'],
                    )
                ])),
            dbc.Col(
                html.Div([
                    html.Label('Process', htmlFor='process'),
                    dcc.Dropdown(id='process')
                ])),
            dbc.Col(
                html.Div([
                    html.Label('Outcome Type', htmlFor='output-type'),
                    dcc.Dropdown(
                        id='output-type',
                        options=outcome_type_columns,
                        value=outcome_type_columns[0]['value'],
                    )
                ]))
        ])
    ])
], fluid=True)

@app.callback(
    Output('process', 'options'),
    Input('process-type', 'value')
)
def set_process_options(selected_process_type):
    options = []
    column = dataset[selected_process_type].unique()
    for value in column:
        if value == 'unknown':
            continue
        options.append({'label': value, 'value': f"{selected_process_type};{value}"})
    return options

@app.callback(
    Output('process', 'value'),
    Input('process', 'options')
)
def set_process_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output("graph", "figure"),
    Input('input-type', 'value'),
    Input("process", "value"),
    Input("output-type", "value")
)
def display_sankey(input_type, process, outcome_type):
    process_type, process_value = process.split(';')
    data = dataset.loc[dataset[process_type] == process_value, [input_type, process_type, outcome_type]]

    input_counts = Counter(data[input_type])
    inputs = list(input_counts.keys())
    input_indices = [i for i in range(len(inputs))]
    input_nodes = list(input_indices)

    process_node = len(input_nodes)

    outcome_counts = Counter(data[outcome_type])
    outcomes = list(outcome_counts.keys())
    outcome_indices = [i for i in range(len(outcomes))]
    outcome_nodes = list(map(lambda i: i + process_node + 1, outcome_indices))

    labels = inputs + [process_value] + outcomes
    nodes = dict(label=labels)

    sources = input_nodes + [process_node] * len(outcome_nodes)
    targets = [process_node] * len(input_nodes) + outcome_nodes
    values = [input_counts[i] for i in inputs] + [outcome_counts[o] for o in outcomes]
    links = dict(source=sources, target=targets, value=values)

    fig = go.Figure(go.Sankey(link=links, node=nodes))
    fig.update_layout(font_size=10)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
