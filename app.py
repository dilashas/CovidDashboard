import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import requests
from datetime import date
import datetime as dt

# GET Nepal Cases Timeline (history)
url = 'https://data.nepalcorona.info/api/v1/covid/timeline'

resp = requests.get(url)

jsonData = resp.json()

timelineDf = pd.DataFrame(jsonData)

timelineDf['Active'] = timelineDf['totalCases'] - timelineDf['totalRecoveries'] - timelineDf['totalDeaths']

timelineDf['date'] = pd.to_datetime(timelineDf['date'])

timelineDf = timelineDf[timelineDf['date'] > pd.to_datetime('2020430', format='%Y%m%d')]

fig11 = go.Figure([go.Scatter(x=timelineDf['date'], y=timelineDf['Active'])],
                  layout = go.Layout(
                      colorway=["#DC143C"],
                      template='plotly_white',
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin={'t': 100, 'b': 15, 'l':0, 'r':125},
                      hovermode='x',
                      autosize=True,
                      title={"yref": "paper",
                             "y": 1,
                             "yanchor": "bottom",
                             'text': 'ACTIVE CASES IN NEPAL',
                             'font':{'color': '#FFFFFF'}, 'x': 0.65, 'xanchor': 'right'},
                              xaxis={'title':'', 'linecolor':"#1C4E80", 'zeroline':False, 'showline':True},
                              yaxis={'title':'', 'linecolor':"#1C4E80", 'zeroline':False, 'showline':True},
                              height=400,
                              width=450,
                              xaxis_showgrid=False,
                              yaxis_showgrid=True,
                              font_color="#FFFFFF",

                  )
                 )


# ------------------------------------------------------------------------------

# GET Nepal Testing Summary
# Current data on infections in nepal, sourced from MOHP SIT reports

url = 'https://nepalcorona.info/api/v1/data/nepal'

resp = requests.get(url)

jsonData = resp.json()

summaryDf = pd.DataFrame(jsonData)

nepalDeaths = summaryDf['deaths'].iloc[0]

nepalDeaths = '{:,}'.format(nepalDeaths)

nepalActive = summaryDf['tested_positive'].iloc[0] - \
              summaryDf['recovered'].iloc[0] - \
              summaryDf['deaths'].iloc[0]

nepalActive = '{:,}'.format(nepalActive)

# ------------------------------------------------------------------------------

# GET Nepal Cases By Municipality
# List of infection in Nepal by municipality, district and province. It has geo location, age and gender of the patient

url = 'https://data.nepalcorona.info/api/v1/covid'

resp = requests.get(url)

jsonData = resp.json()

municipalityDf = pd.DataFrame(jsonData)

# ------------------------------------------------------------------------------

test = municipalityDf[municipalityDf['currentState'] == 'active']

check = test[['id', 'reportedOn']].groupby('reportedOn').count()

check = test.groupby('reportedOn').count()

sum(check['id'])

# ------------------------------------------------------------------------------

# GET Nepal Cases Summary (count)
# Count of nepali by different facts like agegroup, gender, currentState, province, municipality, district and more

url = 'https://data.nepalcorona.info/api/v1/covid/summary'

resp = requests.get(url)

jsonData = resp.json()

# caseCountDf = pd.DataFrame(jsonData)

# ------------------------------------------------------------------------------

# GET World Infection Timeline by Country
# Infection data per day for each countries

url = 'https://data.nepalcorona.info/api/v1/world/history'

resp = requests.get(url)

jsonData = resp.json()

timelineByCountryDf = pd.DataFrame(jsonData)

# ------------------------------------------------------------------------------

# GET District list
# fiter using name ?search={name of district}

url = 'https://data.nepalcorona.info/api/v1/districts'

resp = requests.get(url)

jsonData = resp.json()

districtsDf = pd.DataFrame(jsonData)

###############################################################################

###############################################################################

activeByDist = pd.DataFrame()

activeByDist = municipalityDf[:]

d1 = date.today()

d1 = d1 - dt.timedelta(days=1)

# ------------------------------------------------------------------------------

activeByDist['recoveredOn'] = activeByDist['recoveredOn'].fillna('2100-01-01')

activeByDist['startDate'] = pd.to_datetime(activeByDist['reportedOn'], format='%Y-%m-%d')

activeByDist['endDate'] = pd.to_datetime(activeByDist['recoveredOn'], format='%Y-%m-%d')

activeByDist['reportedDate'] = pd.to_datetime(activeByDist['startDate']).apply(lambda x: x.date())

activeByDist['recoveredDate'] = pd.to_datetime(activeByDist['endDate']).apply(lambda x: x.date())

reportedToday = activeByDist[activeByDist['reportedDate'] == d1]

nepalNewCases = '{:,}'.format(len(reportedToday))

recoveredToday = activeByDist[activeByDist['recoveredDate'] == d1]

nepalRecovered = '{:,}'.format(len(recoveredToday))

# ------------------------------------------------------------------------------

distrMap = dict(zip(districtsDf['id'], districtsDf['title_en']))

districtList = list(distrMap.keys())

# ------------------------------------------------------------------------------

columnList = ['Date'] + districtList

inputDataDf = pd.DataFrame(columns=columnList)

# ------------------------------------------------------------------------------

d0 = date(2020, 5, 1)

delta = d1 - d0

dateRange = pd.date_range('2020-05-01', periods=delta.days+1, freq='1D')

inputDataDf['Date'] = dateRange

# ------------------------------------------------------------------------------

# Iterate over rows of active cases table and fill in with number of active cases per district

for i, row in inputDataDf.iterrows():

    filtered = activeByDist[(activeByDist['startDate'] < row['Date']) & \
                            (activeByDist['endDate'] > row['Date'])]

    for distr in districtList:
        distrCount = filtered[filtered['district'] == int(distr)]

        countVal = len(distrCount)

        inputDataDf.at[i, distr] = countVal

# ------------------------------------------------------------------------------

inputDataDf = inputDataDf.rename(columns=distrMap)

# ------------------------------------------------------------------------------

inputDataDf.index = pd.to_datetime(inputDataDf['Date'])

df = inputDataDf.copy()

del df['Date']

###############################################################################

###############################################################################

# Load data
# demo_data = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
# df.index = pd.to_datetime(demo_data['Date'])


# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server = app.server


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

    for i in list_socks:
        dict_list.append({'label': i, 'value': i})

    for



app.layout = html.Div(
    children=[
        html.Div([
            html.H1("NEPAL COVID-19 INSIGHTS", style={'font-weight': 'bold', 'font-size': '30px'}),
        ],
            style={'padding': '8px',
                   'backgroundColor': '#DC143C',
                   'color': '#FFFFFF',
                   'padding-top': '30px',
                   # 'padding-left': '445px',
                   'text-align': 'center',
                   }),
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.H2('SEARCH BY DISTRICT',
                                          style={'color': '	#FFFFFF'}),
                                  html.P('Pick one or more districts from the dropdown below.',
                                         style={'color': '#FFFFFF'}),
                                  html.Div(
                                      className='custom-dropdown',
                                      children=[
                                          dcc.Dropdown(id='stockselector', options=get_options(list(df.columns)),
                                                       multi=True, value=['Kathmandu'],
                                                       ),
                                      ],
                                  ),

                                  dcc.Graph(id='nepalSummary', figure=fig11, config={'displayModeBar': False},
                                            animate=True,
                                            style={"height": "25%", "width": "100%"}),

                              ],
                              ),
                     html.Div(className='eight columns div-for-charts bg-white',
                              children=[
                                  # District Graph here
                                  dcc.Graph(id='districtGraph',
                                            config={'displayModeBar': False},
                                            animate=True, ),
                                    # Boxes with stats start here
                                  html.Div(
                                      [
                                          html.Div(
                                              [html.H4("Active Cases",
                                                       style={'color': 'white', \
                                                              'font-weight': 'bold'}), html.H2(nepalActive,
                                                                                               style={'color': 'red', \
                                                                                                      'font-weight': 'bold',
                                                                                                      'text-align': 'center'})],
                                              id="wells",
                                              className="mini_container",
                                          ),
                                          html.Div(
                                              [html.H4("New Cases",
                                                       style={'color': 'white', \
                                                              'font-weight': 'bold'}), html.H2(nepalNewCases,
                                                                                               style={'color': 'red', \
                                                                                                      'font-weight': 'bold',
                                                                                                      'text-align': 'center'})],
                                              id="gas",
                                              className="mini_container",
                                          ),
                                          html.Div(
                                              [html.H4("New Recovered",
                                                       style={'color': 'white', \
                                                              'font-weight': 'bold'}), html.H2(nepalRecovered,
                                                                                               style={'color': 'red', \
                                                                                                      'font-weight': 'bold',
                                                                                                      'text-align': 'center'})],
                                              id="oil",
                                              className="mini_container",
                                          ),
                                          html.Div(
                                              [html.H4("Total Deaths",
                                                       style={'color': 'white', \
                                                              'font-weight': 'bold'}), html.H2(nepalDeaths,
                                                                                               style={'color': 'red', \
                                                                                                      'font-weight': 'bold',
                                                                                                      'text-align': 'center'})],
                                              id="water",
                                              className="mini_container",
                                          ),
                                      ],
                                      id="info-container",
                                      className="row container-display",
                                  ),
                              ])
                    ]
                 )
        ]
    )


# Callback for districtGraph price
@app.callback(Output('districtGraph', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub.index,
                                 y=df_sub[stock],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))





    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#DC143C", '#0091D5', '#FF3403', '#B3C100', '#C724B1', '#488A99'],
                  template='plotly_white',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'ACTIVE CASES BY DISTRICT',
                         'font': {'color': '#1C4E80'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()],
                         'title': 'Date',
                         'linecolor': "#1C4E80",
                         'zeroline': False},
                  yaxis={'title': 'Confirmed Cases',
                         'linecolor': "#1C4E80",
                         'zeroline': False},

                  xaxis_showgrid=True,
                  yaxis_showgrid=True,
                  font_color="#1C4E80"
              ),

              }

    return figure


if __name__ == '__main__':
    app.run_server()



