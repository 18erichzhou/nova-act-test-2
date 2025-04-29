"""
Dependencies:
    "fastapi>=0.115.6"

This script sets up a server that allows users to interact with the AgiAutonomyClient SDK.
It provides a web interface where users can send commands to the client and view the output.

Usage:
    1. Install dependencies:
        ```
        pip install "fastapi[standard]>=0.115.6"
        ```
    2. Run this script with the `fastapi` command:
        ```
        fastapi dev src/nova_act/samples/ui_viewer.py
        ```
    3. Open a web browser and navigate to `http://127.0.0.1:8000` to access the UI.
    4. Start the client by clicking the "Start" button in the UI.
    5. Use the input to send commands to the client and view the output.
    6. To stop the client, use the "Stop" button in the UI.
"""

import asyncio
import functools
import sys
from io import StringIO

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from nova_act import NovaAct

app = FastAPI()
client = NovaAct(starting_page="https://www.amazon.com")


class StreamToWebSocket:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.buffer = StringIO()

    def write(self, text):
        # Store in buffer and send if we have a complete line
        self.buffer.write(text)
        if "\n" in text:
            self.flush()

    async def async_write(self, text):
        await self.websocket.send_text(text)

    def flush(self):
        text = self.buffer.getvalue()
        if text:
            loop = asyncio.get_event_loop()
            try:
                # Create new event loop for async operation if needed
                loop.create_task(self.async_write(text))
                self.buffer = StringIO()
            except Exception:
                loop.close()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    loop = asyncio.get_running_loop()
    await websocket.accept()
    stdout_redirect = StreamToWebSocket(websocket)
    sys.stdout = stdout_redirect

    try:
        while True:
            data = await websocket.receive_text()
            if data == "exit":
                # The run_in_executor is needed to run synchronous nova_act client functions
                # within the asyncio loop
                loop.run_in_executor(None, client.stop)
            elif data == "initiate":
                loop.run_in_executor(None, client.start)
            else:
                loop.run_in_executor(None, functools.partial(client.act, data))

    except WebSocketDisconnect:
        print("Client disconnected")


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>AgiAutonomyClient SDK Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            #messages {
                border: 1px solid #ccc;
                padding: 20px;
                min-height: 200px;
                max-height: 500px;
                overflow-y: auto;
                margin: 20px 0;
                background-color: #f9f9f9;
            }
            .message {
                margin: 5px 0;
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            .controls {
                margin: 20px 0;
            }
            button {
                padding: 10px 20px;
                margin-right: 10px;
                cursor: pointer;
            }
            .input-container {
                margin: 20px 0;
                display: flex;
                gap: 10px;
            }
            #messageInput {
                flex-grow: 1;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            #sendButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            #sendButton:hover {
                background-color: #45a049;
            }
            #sendButton:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
        </style>
    </head>
    <body>
        <h1>AgiAutonomyClient SDK Demo</h1>
        <div class="controls">
            <button onclick="sendCommand('initiate')">Start</button>
            <button onclick="sendCommand('exit')">Stop</button>
        </div>
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Enter your message..."
                   onkeypress="handleKeyPress(event)">
            <button id="sendButton" onclick="sendMessage()">Send</button>
        </div>
        <div id="messages"></div>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            function sendCommand(cmd) {
                ws.send(cmd);
            }

            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (message) {
                    ws.send(message);
                    input.value = '';
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            function updateControlsState(enabled) {
                document.querySelectorAll('button').forEach(btn => btn.disabled = !enabled);
                document.getElementById('messageInput').disabled = !enabled;
            }

            ws.onopen = function(event) {
                addMessage('Connected to server');
                updateControlsState(true);
            };

            ws.onmessage = function(event) {
                addMessage(event.data);
            };

            ws.onclose = function(event) {
                addMessage('Connection closed');
                updateControlsState(false);
            };

            ws.onerror = function(event) {
                addMessage('Error: ' + event);
            };

            function addMessage(text) {
                var messages = document.getElementById('messages');
                var message = document.createElement('div');
                message.className = 'message';
                message.textContent = text;
                messages.appendChild(message);
                messages.scrollTop = messages.scrollHeight;
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)
