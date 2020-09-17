#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
##################################### Header ############################################
""" obstruction.py: Description of the node """
#__author__ = ""
#__credits__ = [""]
#__version__ = "0.0.0"
#__maintainer__ = ""
#__email__ = ""
#########################################################################################
# import any libraries necessary to run script
import roslib
import rospy
import math
import time 
import sys
import random
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan



class navigation():

	def __init__(self):
		
		self.robot_stopped=True
		self.obstacle_distance=0.1
		#self.array_distancias
	
		self.velocity_message = Twist()

		velocity_publisher = rospy.Publisher("cmd_vel", Twist ,queue_size=10)

		Laser_subscriber = rospy.Subscriber("base_scan", LaserScan, self.laserCallback)

		self.rate = rospy.Rate(10)

		rand=random.randint(50,200)


		i=0
		vel_ang=1.0;

		while not rospy.is_shutdown():
			#print "entrou aqui"
			#print(self.obstacle_distance)
			#break
			if(self.obstacle_distance>0.5):
				self.velocity_message.linear.x=1.0
				self.velocity_message.angular.z=0.0

				if(self.robot_stopped):
					rospy.loginfo("Moving Forward")
					robot_stopped = False;

			else:

				if(i==rand):
					vel_ang=-(vel_ang)
					rand=random.randint(50,200)
					i=0
				

				self.velocity_message.linear.x=0.0
				self.velocity_message.angular.z=vel_ang

				if not (self.robot_stopped):
					rospy.loginfo("Stopping")
					self.robot_stopped=True

				i=i+1
				print i

			velocity_publisher.publish(self.velocity_message)

			self.rate.sleep()


	def laserCallback(self,msg_laser):
		
		if(self.robot_stopped):
			self.array_distancias=msg_laser.ranges
		#	rospy.loginfo("Received a LaserScan with %i samples" %(len(self.array_distancias)))
			self.obstacle_distance=min(self.array_distancias)
		#	self.obstacle_distance=self.array_distancias[120]
			rospy.loginfo("minimum distance to obstacle: %f" %(self.obstacle_distance))


	#def degrees_to_radians(self,degree):
		#self.velocity_message.angular.z=

		

def main():
	rospy.init_node('reactive_navigation', anonymous=True)
	obst = navigation()

	rospy.spin()



if __name__ == '__main__':
	try: 
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)