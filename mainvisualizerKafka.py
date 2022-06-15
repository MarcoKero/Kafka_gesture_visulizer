import json
from kafka import KafkaConsumer
import threading
import datetime
import dash
from dash import dcc, html

from dash.dependencies import Input, Output

global stampa

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

def gest_thread(thread_name,config_info):
    global stampa
    consumer = KafkaConsumer(thread_name,
                            bootstrap_servers=config_info["bootstrapservers"],
                            security_protocol=config_info["security_protocol"],
                            sasl_mechanism=config_info["sasl_mechanism"],
                            sasl_plain_username=config_info["sasl_plain_username"],
                            sasl_plain_password=config_info["sasl_plain_password"],
                            value_deserializer=lambda x: json.loads(x.decode('utf-8')))#forse ultimo no

    print(stampa)
    for msg in consumer:
        print("befine")
        msg_value=msg.value
        tempointero=int(msg_value["wear_time"])*1e-6
        timestamp = datetime.datetime.fromtimestamp(tempointero)
        print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        stringfinale="Gesture detected: "+str(msg_value["gesture_name"])+". Esecuted by Body id "+str(msg_value['body_id'])+". Was shaked wearable "+ str(msg_value['wear_id']) + ", time: "+str(timestamp)+"|||||||||||||||||||||||||||||||||"
        tempo=str(msg_value)
        print(tempo)

        stampa = stampa + stringfinale + "\n"+"                                                    "


"""def pose_thread(thread_name,config_info):
    global datafine
    global stampa
    #msg=read_filejson("GestureRecKafkaDocker/data/befine_no_collision_1_zed/1.json")
    #datasample = decode_json(msg)
    #datafine=[datasample,datasample,datasample]
    #print(datafine)
    #print(config_info)
    consumer = KafkaConsumer(thread_name,
                            bootstrap_servers=config_info["bootstrapservers"],
                            security_protocol=config_info["security_protocol"],
                            sasl_mechanism=config_info["sasl_mechanism"],
                            sasl_plain_username=config_info["sasl_plain_username"],
                            sasl_plain_password=config_info["sasl_plain_password"],
                            value_deserializer=lambda x: json.loads(x.decode('utf-8')))#forse ultimo no

    print(stampa)
    for msg in consumer:
        print("befine")
        #print(msg)#{"timestamp": 1654607356927.583, "body": [{"body_id": 0, "event": [], "keypoints": {"nose": {"x": NaN, "y": NaN, "z": NaN}, "left_ear": {"x": NaN, "y": NaN, "z": NaN}, "right_ear": {"x": NaN, "y": NaN, "z": NaN}, "left_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "right_shoulder": {"x": NaN, "y": NaN, "z": NaN}, "left_elbow": {"x": NaN, "y": NaN, "z": NaN}, "right_elbow": {"x": NaN, "y": NaN, "z": NaN}, "left_wrist": {"x": NaN, "y": NaN, "z": NaN}, "right_wrist": {"x": NaN, "y": NaN, "z": NaN}, "left_hip": {"x": 10.851959228515625, "y": -4.4818196296691895, "z": -0.900795578956604}, "right_hip": {"x": 10.782848358154297, "y": -4.492856979370117, "z": -0.9190366268157959}, "left_knee": {"x": NaN, "y": NaN, "z": NaN}, "right_knee": {"x": 10.482959747314453, "y": -4.294037342071533, "z": -0.881792426109314}, "left_ankle": {"x": NaN, "y": NaN, "z": NaN}, "right_ankle": {"x": NaN, "y": NaN, "z": NaN}, "neck": {"x": NaN, "y": NaN, "z": NaN}, "chest": {"x": NaN, "y": NaN, "z": NaN}, "mid_hip": {"x": 10.817403793334961, "y": -4.487338066101074, "z": -0.9099161028862}}}]}
        #time = decode_json(msg)
        tempo=str(msg.value["timestamp"])
        print(tempo)
        #tempo = str(time["timestamp"])
        stampa = stampa + tempo + "\n"+"  "
"""

def visualizerapp():
    global stampa
    stampa="Elenco gesture riconosciute:\n"
    path = "data_config_gestures.json"
    config_info = read_filejson(path)
    """pose_aggregatorThread = threading.Thread(target=pose_thread,
                                             args=(config_info["consumer_pose_aggreagator_name"], config_info))"""
    gestThread = threading.Thread(target=gest_thread,
                                             args=(config_info["consumer_gesture_recognition_name"], config_info))

    """consumer = KafkaConsumer(config_info["consumer_pose_aggreagator_name"],
                             bootstrap_servers=config_info["bootstrapservers"],
                             security_protocol=config_info["security_protocol"],
                             sasl_mechanism=config_info["sasl_mechanism"],
                             sasl_plain_username=config_info["sasl_plain_username"],
                             sasl_plain_password=config_info["sasl_plain_password"])"""
    app = dash.Dash(__name__)
    app.layout = html.Div(
        html.Div([
            html.H4('Gesture Recognition'),
            html.Div(id='live-update-text'),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ])
    )

    @app.callback(Output('live-update-text', 'children'),
                  Input('interval-component', 'n_intervals'))
    def update_metrics(n):
        #
        '''if consumer is not None:
            #print(msg)
            for msg in consumer:
                #msg=consumer[0]
                #print(msg)

                time = decode_json(msg)
                print(time["timestamp"])
                tempo=str(time["timestamp"])
                stampa=stampa+ tempo+"\n"'''
        time = datetime.datetime.now() - datetime.timedelta()
        return stampa

    gestThread.start()
    app.run_server(debug=True)

'''def new_app():

    from dash.dependencies import Input, Output  # Load Data

    df = px.data.tips()  # Build App

    from dash.dependencies import Input, Output

    #external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = JupyterDash(__name__)
    import datetime
    """app.layout = html.Div([
        html.H6("Change the value in the text box to see callbacks in action!"),
        html.Div(["Input: ",
                  dcc.Input(id='my-input', value='initial value', type='text')]),
        html.Br(),
        html.Div(id='my-output'),
        

    ])"""

    def serve_layout():
        return html.H1('The time is: ' + str(datetime.datetime.now()))

    app.layout = serve_layout

    path = "data_config_gestures.json"
    config_info = read_filejson(path)
    """consumer = KafkaConsumer(config_info["consumer_pose_aggreagator_name"],
                             bootstrap_servers=config_info["bootstrapservers"],
                             security_protocol=config_info["security_protocol"],
                             sasl_mechanism=config_info["sasl_mechanism"],
                             sasl_plain_username=config_info["sasl_plain_username"],
                             sasl_plain_password=config_info["sasl_plain_password"])"""

    @app.callback(
        Output(component_id='my-output', component_property='children'),
        Input(component_id='my-input', component_property='value')
    )
    def update_output_div(input_value):
        tempo="nulla"
        for msg in consumer:
            #print(msg)
            time = decode_json(msg)
            print(time["timestamp"])
            tempo=str(time["timestamp"])
        #return 'Output: {}'.format(input_value)

        return 'Output:{}'.format(tempo)

    app.run_server(mode='inline',dev_tools_hot_reload=True)'''

"""def send_to_visulizer(msg):
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
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )
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

    app.run_server(debug=True)"""

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
    visualizerapp()

if __name__ == '__main__':
    main()