import websocket, json
from shader_visualizer import update_visualizer

AUTH_TOKEN = "your_observer_node_token"

def on_message(ws, message):
    data = json.loads(message)
    update_visualizer(data)

def start_quantime_stream():
    ws = websocket.WebSocketApp(
        "wss://civilisation.one/quantum-dashboard/stream/quantime",
        header={"Authorization": f"Bearer {AUTH_TOKEN}"},
        on_message=on_message
    )
    ws.run_forever()
