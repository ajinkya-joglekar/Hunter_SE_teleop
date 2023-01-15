#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import math
#import can
#import cantools

pi = math.pi
#db = cantools.db.load_file('/home/opencav-clone/Downloads/test_database.DBF')
#steering_msg = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

def callback(data):
	angle=data.axes[0]
	steering_angle= angle
	if data.axes[2] > 0:
		speed = data.axes[2]
	elif data.axes[3] > 0:
		speed = -data.axes[3]
	else:
		speed = 0.0
		
	#accel = (data.axes[2] + 1)*0.5
	twist_msg = Twist()
	twist_msg.linear.x = speed*1.5
	twist_msg.angular.z = steering_angle
	pub.publish(twist_msg)
	


def listener():
	rospy.init_node('listener',anonymous=True)
	
	rospy.Subscriber('/joy_orig',Joy,callback)
	
	


if __name__ == "__main__":
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
	listener()
	r = rospy.Rate(1000)
	r.sleep()
	rospy.spin()
	
	
	## Pub to hunter
	
	# Publisher to hunter --> /twist_vel --> CAN Take /joy_orig --> remap to /twist -->> Publisher } Logitech --> joy --> twist --> hunter --> Feedback (camera)
	
