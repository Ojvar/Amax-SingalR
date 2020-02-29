from signalr_aio import Connection
from base64 import b64decode
from zlib import decompress, MAX_WBITS
from requests import Session
import json
import asyncio

hub = None;
appHub = None;
connection = None;

def process_message(message):
    print(message);
#    deflated_msg = decompress(b64decode(message), -MAX_WBITS)
#    return json.loads(deflated_msg.decode())

# Create debug message handler.
async def on_debug(**msg):
    # In case of 'queryExchangeState'
    print(msg)
    if 'R' in msg and type(msg['R']) is not bool:
        # decoded_msg = process_message(msg['R'])
        # print(decoded_msg);

        # session.headers.update({'Authorization': 'Bearer {token}'.format(token=token)})
        token = msg['R'];

        print('Token is: ', token);

        print('-------------------------');
        # session = Session();
        server_url = server_url + "?token=${token}".format(token=token);
        conn = Connection(server_url, session);
        # conn.session.headers.update({'Authorization': 'Bearer {token}'.format(token=token)})

        appHub = conn.register_hub('omsclienthub');
        conn.received += on_recieved;
        conn.error += on_error
        companies = appHub.server.invoke('GetInstrumentList');

        connection.close();

        conn.start()

async def on_recieved(**msg):
    companies = msg['R'];


# Create error handler
async def on_error(msg):
    print(msg)

# Create hub message handler
async def on_message(msg):
    decoded_msg = process_message(msg[0])
    print(decoded_msg)


if __name__ == "__main__":
    server_url = 'http://firouzex.exphoenixtrade.com/realtime';

    # Create a connection
    session = Session();
    connection = Connection(server_url, session)
    hub = connection.register_hub('omsclienttokenhub')
    appHub = connection.register_hub('omsclienthub');
    connection.received += on_debug
    connection.error += on_error
    hub.server.invoke('GetAPIToken', 'fTTTTTT', 'XXXXX');

    connection.start()
