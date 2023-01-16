import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input,Output
dataset_path = "data.csv"

# Load dataset
data_frame = pd.read_csv(dataset_path ,sep=';')

# Display first 5 lines
print(data_frame.head())

image_path = 'assets/popa2.png'


mapbox_token = "pk.eyJ1IjoieWFtaWRvdmljaDc2IiwiYSI6ImNsMGVndGE3dTBpdGUzZG9udjJxcWw4a2kifQ.-RwMEc-nz4Ak_0YstiJ-Bg"

names = ['vicko','A','B','C']


optoins = []
for k in names:
    optoins.append({'label': k, 'value': k})


votos_selector = dcc.Dropdown(
    id='votos',
    options=optoins,
    value=['vicko','A','B','C'],
    multi=True

)
# Selecting the day to display
day = "04.03.2022"
tmp = data_frame

#print(tmp.head())

#tmp['size'] = df['vicko'].apply(lambda x: (np.sqrt(x/100) + 1) if x > 500 else (np.log(x) / 2 + 1))
#tmp['color'] = (df['vicko']/df['A'])*10

#tmp

#GLOBAL DESIGN SETTINGS

CHARTS_TEMPLATE = go.layout.Template(
    layout=dict(
        legend=dict(
            orientation="h",
            title_text="")
    )
)

# Create the figure and feed it all the prepared columns




# Specify layout information
fig = px.scatter_mapbox(lat=tmp['lat'], lon=-tmp['lon'])
fig.update_layout(
    mapbox=dict(
        accesstoken=mapbox_token, #
        center=go.layout.mapbox.Center(lat=0.965446, lon=-79.65),
        zoom=10
    )
)
fig2 = px.bar(data_frame, x=tmp['zona'], y=tmp['vicko'], color_continuous_scale=px.colors.cyclical.IceFire, width=1000, height=700)
fig2.update_layout(template=CHARTS_TEMPLATE)


app = dash.Dash(__name__,
                      external_stylesheets=[dbc.themes.MATERIA])


"""LAYOUT"""

app.layout = html.Div([
html.Img(src=image_path),
#dbc.Row(html.H1('Предвыборная компания другa моего папы'),
#style={'margin-bottom': '40px'}),
dbc.Row([
    dbc.Col([
     html.Div("статистика предвыборной компании"), 
     html.Div("kandidat"),
     html.Div(votos_selector,
     style={'width': '400px',
     "margin-bottom": '40px'}

     ),
        dcc.Graph(id="mapbox-markers",
        figure=fig
        )
], width={"size": 5}),
    dbc.Col([
        html.Div("колонны какие-то"),
        dcc.Graph(id="chart-bar",
        figure=fig2)
    ], width={"size": 3, "offset": 2}),
],style={'margin-bottom': 40}) 
],

style={'margin-left': '0px',
'margin-right': '80px'})


@app.callback (
    Output(component_id='mapbox-markers', component_property='figure'),
    Input(component_id='votos', component_property='value')
)
def update_mapbox_markers(votos): 
    print(votos)
    
    fig = px.scatter_mapbox(data_frame, lat=tmp['lat'], lon=-tmp['lon'], size=tmp['size'], color=tmp[f"colvicko"], hover_name=tmp["zona"], hover_data=votos,
                   zoom=10, text= tmp['zona'], size_max=50, width=1000, height=700)
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_token, #
            center=go.layout.mapbox.Center(lat=0.965446, lon=-79.65),
            zoom=10
        )
    )

    

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)