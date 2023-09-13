import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from pyvis.network import Network
import pandas as pd

# Your network generation code as a function
def generate_graph():
    got_net = Network(height="750px", width="100%", bgcolor="white", font_color="#222222")

    # set the physics layout of the network
    got_net.barnes_hut(spring_length=30, spring_strength=0.5, central_gravity=0.1, damping=0.40)

    got_data = pd.read_csv("\\Users\dambe\Downloads\stormofswords.csv")

    got_data = got_data.iloc[:30]
    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']

    edge_data = zip(sources, targets, weights)
    website_url = "https://www.google.com"

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        # Define node color attributes
        node_color = {
            "background": "#4F81BD",  
            "border": "#2C3E50",  
            "highlight": {  
                "background": "blue", 
                "border": "dark blue"
            },
            "hover": {  
                "background": "lightyellow", 
                "border": "orange"
            }
        }

        # Adding nodes with large labels inside bigger ellipses and custom colors.
        got_net.add_node(src, label=src, title=f'<a href="{website_url}" target="_blank">{src}</a>', font={"size": 200, "face": "arial"}, shape="ellipse", size=300, color=node_color)
        got_net.add_node(dst, label=dst, title=f'<a href="{website_url}" target="_blank">{src}</a>', font={"size": 200, "face": "arial"}, shape="ellipse", size=300, color=node_color)
        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    got_net.save_graph("gameofthrones.html")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Game of Thrones Network Graph"),

    # Button to trigger the re-rendering
    html.Button("Regenerate Graph", id="regenerate-button"),

    # Iframe to display the graph
    html.Iframe(id="graph-iframe", width="100%", height="800px")
])

# Callback to re-render the graph
@app.callback(
    Output("graph-iframe", "srcDoc"),
    Input("regenerate-button", "n_clicks")
)
def update_graph(n_clicks):
    if n_clicks:
        generate_graph()
        return open("gameofthrones.html", "r").read()
    return dash.no_update

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
