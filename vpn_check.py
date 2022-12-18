from dash import html, Dash
from dash.dcc import Interval
from dash.dependencies import Input, Output
from datetime import datetime
from loguru import logger

from telnet_func import telnet_connection


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.Title("Beskyd VPN Checking"),
    html.Br(),
    html.H1('Beskyd VPN Checking'),
    html.Hr(),
    html.Br(),
    html.H2('Connection to the VPN'),
    html.Br(),
    html.Div(id='output_div'),
    Interval(
        id='interval_component',
        max_intervals=-1,
        interval=1000*60*15,  # in milliseconds, 1000*60*15 = 15 mins.
        n_intervals=0,
    ),
    ],
    style={
        'margin-left': 30,
        'margin-right': 100,
    })


@app.callback(Output('output_div', 'children'),
              Input('interval_component', 'n_intervals'))
def response_output(value):
    result = telnet_connection()
    t = datetime.now()
    tt = t.strftime("%H:%M:%S")
    last_update = t.strftime("%d.%m.%Y %H:%M:%S")
    # logger.info(f"{tt} - {result}")
    match result:
        case "Success":
            return html.Div(
                style={'color': '#145A32'},
                children=[
                    html.H3("Success"),
                    html.Br(),
                    html.Img(src=r'assets/done.png', width=100, alt="Success"),
                    html.Br(),
                    html.Br(),
                    html.H4("Everything works fine!"),
                    html.Br(),
                    html.H4(f'Last update: {last_update}'),
                    html.Br(),
                ])
        case "TimeoutError":
            return html.Div(
                style={'color': 'red'},
                children=[
                    html.H3("Timeout Error"),
                    html.Br(),
                    html.Img(src=app.get_asset_url('error.png'), width=100, alt="Error"),
                    html.Br(),
                    html.Br(),
                    html.H4("The connection to the VPN is not working!"),
                    html.Br(),
                    html.H4(f'Last update: {last_update}'),
                    html.Br(),
                ])
        case _:
            return html.Div(
                style={'color': 'red'},
                children=[
                    html.H3("Something is wrong..."),
                    html.Br(),
                    html.H4("Ping function doesn't work!"),
                    html.Br(),
                    html.H4(f'Last update: {last_update}'),
                    html.Br(),
                ])


if __name__ == '__main__':
    app.run(debug=False)
