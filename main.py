from dash import Dash

app = Dash(__name__, use_pages=True)
app.run(debug=True, port=8000)
