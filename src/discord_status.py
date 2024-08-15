# DISCLAIMER: Some of this code has been written by ChatGPT. Be warned.

import threading
import json
import time
import os

import platformdirs
import websocket


# This will be set later
heartbeat_interval = None
bot_token = None


def _start():
    def on_message(ws, message):
        # This happens when the websocket sends us a message.
        global heartbeat_interval

        data = json.loads(message)
        if data["op"] == 10:
            heartbeat_interval = data["d"]["heartbeat_interval"] / 1000.0
            print(f"Sending heartbeats every {heartbeat_interval} seconds")
            start_heartbeat(ws)
        elif data["op"] == 11:
            # The server accepted our heartbeat, i.e. Heartbeat ACK
            print("Heartbeat acknowledged")

    def on_error(_, error):
        print(f"Error: {error}")

    def on_close(_, __, ___):
        print("Connection closed")

    def on_open(ws):
        print("Connection opened")

        # Authenticate
        payload = {
            "op": 2,
            "d": {
                "token": bot_token,
                "properties": {},
                "presence": {
                    "status": "online",
                    "activities": [],
                },
            },
        }

        # Send our payload
        ws.send(json.dumps(payload))

    def start_heartbeat(ws):
        # Sends messages to keep the status up
        def send_heartbeat():
            while True:
                if heartbeat_interval:
                    ws.send(json.dumps({"op": 1, "d": None}))
                    time.sleep(heartbeat_interval)

        # Send heartbeats in the background
        threading.Thread(target=send_heartbeat, daemon=True).start()

    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=10&encoding=json",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()


def keep_online():
    # Get Discord token
    if os.path.isfile(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt"):
        with open(platformdirs.user_config_dir("Qtcord") + "/discordauth.txt") as f:
            bot_token = f.read()

    # Stop if bot token isn't defined
    if not bot_token:
        return

    threading.Thread(target=_start, daemon=True).start()
