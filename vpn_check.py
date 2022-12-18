from dash import html, Dash
from dash.dcc import Interval
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import pytz
# from loguru import logger

# from messenger import notification
from telnet_func import telnet_connection


app = Dash(__name__)
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
    result: str = ""
    try:
        result = telnet_connection()
    except Exception as ex:
        # logger.critical(ex)
        pass
    time_ = datetime.now(pytz.timezone('Europe/Kyiv'))
    t = time_ + timedelta(minutes=120)
    tt = t.strftime("%H:%M:%S")
    last_update = t.strftime("%d.%m.%Y %H:%M:%S")
    sending_h = int(t.strftime("%H"))
    sending_mins = t + timedelta(minutes=1)
    sending_m = int(sending_mins.strftime("%M"))

    if result == "Success":
        # msg = f"{last_update} - VPN works fine!"
        # try:
        #     notification(msg, sending_h, sending_m)
        # except Exception as ex:
        #     logger.warning(ex)
        #     pass
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
    elif result == "TimeoutError":
        # msg = f"{last_update} - TimeoutError - The connection to the VPN is not working!"
        # try:
        #     notification(msg, sending_h, sending_m)
        # except Exception as ex:
        #     logger.warning(ex)
        #     pass
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
    else:
        # msg = f"{last_update} - OtherException - Something is wrong!"
        # try:
        #     notification(msg, sending_h, sending_m)
        # except Exception as ex:
        #     logger.warning(ex)
        #     pass
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
