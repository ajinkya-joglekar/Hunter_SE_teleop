#!/usr/bin/env python
import rospy
from sensor_msg.msg import Joy
import math
import can
import cantools

pi = math.pi
db = cantools.db.load_file('/home/opencav-clone/Downloads/test_database.DBF')
steering_msg = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

def callback(data):
	angle=data.axes[0]
	steering_angle= -(450*angle)
	accel = (data.axes[2] + 1)*100
	global bus
	global steering_msg
	steer_data = steering_msg.encode({"steering_value:":steering_angle})
	msg = can.Message(arbitration_id=0x18feaf00,data=steer_data,extended_id=True)
	try:
		bus.send(msg)
	except can.CanError:
		print("Message not sent")

def listener():
	rospy.init_node('listener',anonymous=True)
	rospy.Subscriber('/joy_orig',Joy,callback)


if __name__ == "__main__":
	listener()
	r = rospy.Rate(1000)
	r.sleep()
	rospy.spin()
	
	
	## Pub to hunter
	
	# Publisher to hunter --> /twist_vel --> CAN Take /joy_orig --> remap to /twist -->> Publisher } Logitech --> joy --> twist --> hunter --> Feedback (camera)
	
