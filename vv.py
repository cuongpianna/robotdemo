import websocket
import json
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

try:
    import thread
except ImportError:
    import _thread as thread
import time

def set_value_redis(res):
    if res['code'] == 'KRW-BTC':
        r.set('upbit:btc', json.dumps(res))
    elif res['code'] == 'KRW-ETH':
        r.set('upbit:eth', json.dumps(res))
    elif res['code'] == 'KRW-EOS':
        r.set('upbit:eos', json.dumps(res))
    elif res['code'] == 'KRW-ADA':
        r.set('upbit:ada', json.dumps(res))
    elif res['code'] == 'KRW-LTC':
        r.set('upbit:ltc', json.dumps(res))
    elif res['code'] == 'KRW-BCH':
        r.set('upbit:bch', json.dumps(res))
    elif res['code'] == 'KRW-BSV':
        r.set('upbit:bsv', json.dumps(res))
    elif res['code'] == 'KRW-XRP':
        r.set('upbit:xrp', json.dumps(res))
    elif res['code'] == 'KRW-ETC':
        r.set('upbit:etc', json.dumps(res))
    elif res['code'] == 'KRW-TRX':
        r.set('upbit:trx', json.dumps(res))

def on_message(ws, message):
    get_message = json.loads(message.decode('utf-8'))
    print(get_message['code'])
    set_value_redis(get_message)


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("close")

def on_open(ws):
    def run(*args):
        sendData = '[{"ticket":"test"},{"type":"ticker","codes":["KRW-BTC", "KRW-ETH", "KRW-EOS", "KRW-ADA", "KRW-LTC", "KRW-BCH", "KRW-BSV", "KRW-XRP", "KRW-ETC", "KRW-TRX"]}]'
        ws.send(sendData)
        time.sleep(1)

        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())




if __name__ == "__main__":
    while True:
        time.sleep(.2)
        ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()