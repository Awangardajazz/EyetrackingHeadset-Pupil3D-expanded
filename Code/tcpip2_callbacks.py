# me - this DAT
#
# dat - the DAT that received the data
# rowIndex - the row number the data was placed into
# message - an ascii representation of the data
#			Unprintable characters and unicode characters will
#			not be preserved. Use the 'bytes' parameter to get
#			the raw bytes that were sent.
# bytes - a byte array of the data received
# peer - a Peer object describing the originating data
#   peer.close() 	#close the connection
#	peer.owner	#the operator to whom the peer belongs
#	peer.address	#network address associated with the peer
#	peer.port		#network port associated with the peer

"""
For TouchDesigner environment the code should used with DAT Text component
"""

import zmq
import msgpack

context = zmq.Context()
# open a req port to talk to pupil
addr = "127.0.0.1"  # remote ip or localhost
req_port = "50021"  # same as in the pupil remote gui
req = context.socket(zmq.REQ)
req.connect("tcp://{}:{}".format(addr, req_port))
# ask for the sub port
req.send_string("SUB_PORT")
sub_port = req.recv_string()
# open a sub port to listen to pupil
sub = context.socket(zmq.SUB)
sub.connect("tcp://{}:{}".format(addr, sub_port))
# set subscriptions to topics
sub.setsockopt_string(zmq.SUBSCRIBE, "pupil.")

def setMinMax(coords, d, nodeName = 'extremes'):
		x = coords[0]
		y=  coords[1]
		d = d
		if op('isReset')['reset'] == 0:
			pass
		else:
			op(nodeName).par.value0 = coords[0]
			op(nodeName).par.value1 = coords[0]
			op(nodeName).par.value2 = coords[1]
			op(nodeName).par.value3 = coords[1]

			op(nodeName).par.value4 = d
			op(nodeName).par.value5 = d
			print("Resetting all parameters!")
		# y = msg['ellipse']['center'][1]
		if (op(nodeName).par.value0) > x: op(nodeName).par.value0 = x
		elif (op(nodeName).par.value1) < x: op(nodeName).par.value1 = x
		elif (op(nodeName).par.value2) > y: op(nodeName).par.value2 = y
		elif (op(nodeName).par.value3) < y: op(nodeName).par.value3 = y
		elif (op(nodeName).par.value4) > d: op(nodeName).par.value4 = d
		elif (op(nodeName).par.value5) < d: op(nodeName).par.value5 = d

def receive(dat, rowIndex, message, bytes, peer):
	topic = sub.recv_string()
	msg = sub.recv()
	msg = msgpack.loads(msg, raw=False)
	mode_name = msg['topic']
	required_model_name =  "pupil.0.2d"
	model_confidence = msg['confidence']
	required_confidence = .5
	#print(msg)
	if mode_name == required_model_name and model_confidence >= required_confidence:
		# coords = msg['sphere']['center']
		d = msg['diameter']
		coords = msg['norm_pos']
		setMinMax(coords, d, nodeName = 'extremes')
		op('val').par.value0 = coords[0]
		op('val').par.value1 = coords[1]
		op('val').par.value2 = d
		print(coords)
	elif mode_name == required_model_name and model_confidence < required_confidence:
		print("Current model confidence is: {}. Required value of {} not acheived!".format(model_confidence, required_confidence))
	return
