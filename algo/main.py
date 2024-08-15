# import os
import logging

# from dotenv import load_dotenv
from collections import deque
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

# from pydantic import BaseModel


listener = FastAPI()
messages = []
logging.basicConfig(level=logging.INFO)
indicator_maxlen, price_maxlen = 200, 200
indicator_queue = deque(maxlen=indicator_maxlen)
price_queue = deque(maxlen=price_maxlen)


def make_html_response(messages):
    html_content = f"""
    <html>
        <head>
            <title>FastAPI Messages</title>
        </head>
        <body>
            <h1>Last 5 Messages</h1>
            <ul>
                {"".join(f"<li>{msg}</li>" for msg in messages)}
            </ul>
        </body>
    </html>
    """
    return html_content


@listener.post("/run")
async def update_strategy_and_indicator(request: Request):
    """
    Get values from a push Pubsub and execute the algo trading logic.
    Updates the indicator and price queues, runs the algo based on those queues asynchronously.

    Params:
    - request: A message from the pubsub topic for getting price data.

    Publishes the signal if one is created, publishes the latest indicator value to another topic.


    Potential issues - asynchronous run - will the strategy execute fast enough before another message comes in?
    """
    global messages
    message = await request.json()
    messages.append(message)
    logging.info(message)

    # todo: update price and indicator queues asynchronously, run strategy script

    if len(messages) > 5:
        messages.pop(0)

    return "ack"


@listener.get("/view")
async def view_messages():
    global messages
    html_content = make_html_response(messages)

    return HTMLResponse(content=html_content, status_code=200)
