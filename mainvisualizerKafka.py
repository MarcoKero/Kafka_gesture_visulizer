import json
import numpy as np
from kafka import KafkaConsumer, KafkaProducer
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.express import data, scatter

def read_filejson(path):
    f = open(path)
    data = json.load(f)
    for i in data:
        print(i)
    f.close()
    return data

def decode_json(msg):
    msg = msg.value.decode('utf-8')
    data = json.loads(msg)
    """    for i in data:
        print(i)"""

    return data

def send_to_visulizer(msg):
    print(msg)

    path = "data_config_gestures.json"
    config_info = read_filejson(path)
    consumer = KafkaConsumer(config_info["consumer_pose_aggreagator_name"],
                             bootstrap_servers=config_info["bootstrapservers"],
                             security_protocol=config_info["security_protocol"],
                             sasl_mechanism=config_info["sasl_mechanism"],
                             sasl_plain_username=config_info["sasl_plain_username"],
                             sasl_plain_password=config_info["sasl_plain_password"])
    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Gesture recognition'),
        html.P("Select color:"),
        dcc.Dropdown(
            id="dropdown",
            options=['Gold', 'MediumTurquoise', 'LightGreen'],
            value='Gold',
            clearable=False,
        ),
        dcc.Graph(id="graph"),
    ])

    @app.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"))
    def display_color():
        for msg in consumer:
            #print(msg)
            print("cambio")
            time = decode_json(msg)

            app.layout = html.Div([
                html.H4('Gesture recognition'),
                html.P(time["timestamp"]),
                dcc.Dropdown(
                    id="dropdown",
                    options=['Gold', 'MediumTurquoise', 'LightGreen'],
                    value='Gold',
                    clearable=False,
                ),
                dcc.Graph(id="graph"),
            ])

    app.run_server(debug=True)

"""
def kafka_gesture_reader():
    path = "data_config_gestures.json"
    config_info = read_filejson(path)
    consumer = KafkaConsumer(config_info["consumer_pose_aggreagator_name"],
                             bootstrap_servers=config_info["bootstrapservers"],
                             security_protocol=config_info["security_protocol"],
                             sasl_mechanism=config_info["sasl_mechanism"],
                             sasl_plain_username=config_info["sasl_plain_username"],
                             sasl_plain_password=config_info["sasl_plain_password"])

    i=0
    for msg in consumer:
        print(msg)
        time=decode_json(msg)
        fig = scatter(title=time["timestamp"])
        fig.show(host='0.0.0.0', port='56442',auto_open=False)
        if i>=17:
            break
        i=i+1
        
def print_ploty (msg):
    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Gesture recognition'),
        html.P(msg),
        dcc.Dropdown(
            id="dropdown",
            options=['Gold', 'MediumTurquoise', 'LightGreen'],
            value='Gold',
            clearable=False,
        ),
        dcc.Graph(id="graph"),
    ])"""
def main():
    send_to_visulizer("ciao")
    print("main")

    #send_to_visulizer('ciao')
    #send_to_visulizer('ciao')

    #change_skeleton('ciao')

if __name__ == '__main__':
    main()