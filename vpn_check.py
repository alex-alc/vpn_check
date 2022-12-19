from dash import html, Dash
from dash.dcc import Interval
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
# from loguru import logger

# from messenger import notification
from telnet_func import telnet_connection

dbc_css = r'assets/bootstrap.min.css'
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
server = app.server

header = html.H4("Beskyd VPN Checking", className="card text-white bg-success mb-3", style="max-width: 20rem;")

app.layout = html.Div(className="data-gr-ext-installed style class", children=[
	html.Div(className="col-lg-8 offset-lg-2 col-md-6 offset-md-3 col-sm-6 offset-md-3", style={"textAlign": "center"}, children=[
		html.Br(),
		html.H1("Beskyd VPN Checking"),
		html.Hr(),
		html.Br(),
	]),

	html.Div(id='output_div'),

	Interval(
		id='interval_component',
		max_intervals=-1,
		interval=1000 * 60 * 15,  # in milliseconds, 1000*60*15 = 15 mins.
		n_intervals=0,
	),
])


@app.callback(Output('output_div', 'children'),
              Input('interval_component', 'n_intervals'))
def response_output(value):
	try:
		result = telnet_connection()
	except Exception as ex:
		# logger.critical(ex)
		pass
	time_ = datetime.now()
	t = time_ + timedelta(minutes=120)
	tt = t.strftime("%H:%M:%S")
	last_update = t.strftime("%d.%m.%Y %H:%M:%S")

	if result == "Success":
		return html.Div(
			id='output_div', className="card text-white bg-success mb-3", style="max-width: 20rem;", children=[
				html.Div(className="card-header", children=["Connection to the VPN"]),
				html.Div(className="card-body", children=[
					html.H4(className="card-title", children=["Everything works fine!"]),
					html.P(className="card-text", children=[
						f"Last update: {last_update}",
						html.Img(src=r'assets/done.png', width=100, alt="Success"),  # Success Img
					]),
				]),
			]),
	elif result == "TimeoutError":
		return html.Div(
			id='output_div', className="card text-white bg-danger mb-3", style="max-width: 20rem;", children=[
				html.Div(className="card-header", children=["Connection to the VPN"]),  # Card Header
				html.Div(className="card-body", children=[  # Card Body
					html.H4(className="card-title", children=["The connection to the VPN is lost!"]),
					html.P(className="card-text", children=[
						f"Last update: {last_update}",
						html.Img(src=r'assets/error.png', width=100, alt="Error"),  # Error Img
					]),
				]),
			]),
	else:
		return html.Div(
			id='output_div', className="card text-white bg-danger mb-3", style="max-width: 20rem;", children=[
				html.Div(className="card-header", children=["Connection to the VPN"]),  # Card Header
				html.Div(className="card-body", children=[  # Card Body
					html.H4(className="card-title", children=["Something is wrong..."]),
					# DANGER card title
					html.P(className="card-text", children=[
						f"Last update: {last_update}",
						html.Img(src=r'assets/error.png', width=100, alt="Error"),  # Error Img
					]),
				]),
			]),


if __name__ == '__main__':
	app.run(debug=False)
