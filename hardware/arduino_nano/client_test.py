import zmq
import time

port = 7000
address = 'tcp://127.0.0.1:%i' % port

context = zmq.Context()
socket = context.socket(zmq.REQ)

while True:

    socket.connect(address)

    json = {'method': 'humidity'}
    socket.send_json(json)

    response = socket.recv_json()
    print('response: ' + str(response))

    socket.disconnect(address)

    time.sleep(0.1)