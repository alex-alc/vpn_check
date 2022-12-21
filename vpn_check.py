from dash import html, Dash
from dash.dcc import Interval
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
from loguru import logger

from ping_func import check_connection


dbc_css = r'assets/bootstrap.min.css'
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
server = app.server

app.layout = (html.Div(
	className="data-gr-ext-installed style class", children=[
		html.Div(className="col-lg-6 offset-lg-3 col-md-8 offset-md-2 col-10 offset-1", style={"textAlign": "center"}, children=[
			html.Br(),
			html.H1("Beskyd VPN Checking"),
			html.Hr(),
			html.Br(),
			html.Div(id='output_div'),
		]),
		Interval(
			id='interval_component',
			max_intervals=-1,
			interval=1000 * 60 * 15,  # in milliseconds: 1000 * 60 * 15 = 15 mins.
			n_intervals=0
		)
	])
)


@app.callback(Output('output_div', 'children'),
              Input('interval_component', 'n_intervals'))
def response_output(value):
	result = None
	try:
		result = check_connection()
	except Exception as ex:
		logger.critical(ex)
		pass
	time_ = datetime.now()
	t = time_ + timedelta(minutes=120)
	last_update = t.strftime("%d.%m.%Y %H:%M:%S")

	if isinstance(result, float):

		return html.Div(id='output_div', children=[
				html.Div(className="card-header", children=["Connection to the VPN"]),
				html.Div(className="card-body", children=[
					html.H4(className="card-title", children=["Everything works fine!"]),
					html.P(className="card-text", children=[f"Last update: {last_update}"]),
					html.P(className="card-text", children=[f"Response time: {result:.0f} ms."]),
					html.Img(src=r'assets/done.png', width=100, alt="Success"),
					html.Br()
				])
		], className="card text-white bg-success mb-3", style={"max-width": "20rem;"})
	elif result is False:
		return html.Div(id='output_div', children=[
				html.Div(className="card-header", children=["Connection to the VPN"]),
				html.Div(className="card-body", children=[
					html.P(className="card-text", children=[f"Last update: {last_update}"]),
					html.H4(className="card-title", children=["The connection to the VPN is lost!"]),
					html.Img(src=r'assets/error.png', width=100, alt="Error"),
					html.Br()
				])
			], className="card text-white bg-danger mb-3", style={"max-width": "20rem;"})


if __name__ == '__main__':
	app.run(debug=False)
