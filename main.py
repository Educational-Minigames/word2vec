from dash import Dash

app = Dash(__name__, use_pages=True)
app.run(debug=True, host="0.0.0.0", port=8000)
