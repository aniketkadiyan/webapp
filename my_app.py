import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


# df = pd.read_csv('testdata.csv')
machinedata = pd.read_csv("machinetestdata.csv")
reasondata = pd.read_csv("reasontestdata.csv")
breakdowndata = pd.read_csv("testdata.csv")
df1 = pd.merge(breakdowndata, machinedata, how="inner", on=["MachineID"])
df = pd.merge(df1, reasondata, how="inner", on=["ReasonId"])


df_groups = df.groupby(['MachineID'])['MachineID'].count()
# print(df_groups)
dff = df[df.MachineID == 18]
# print(dff)
dfg = dff.groupby(['ReasonId'])['ReasonId'].count().reset_index(name='count')
# print(dfg)
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
app = Dash(__name__)
server = app.server
print(server)
app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    dcc.Dropdown(df.MachineName.unique(), '1', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.MachineName == value]
    dfg = dff.groupby(['ReasonName'])[
        'ReasonName'].count().reset_index(name='count')
    # print(dfg)
    return px.bar(dfg, x='ReasonName', y='count')


if __name__ == '__main__':
    app.run()
