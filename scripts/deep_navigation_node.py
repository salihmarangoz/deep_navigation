#!/anaconda3/envs/tensorflow/bin/python
import sys
sys.path.append('/usr/local/lib/python3.6/dist-packages')

import tensorflow as tf
import numpy as np
print("tensorflow imported successfully")

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
print("rospy imported successfully")

import os

new_model = tf.keras.models.load_model( os.path.dirname(__file__) + "/../notebooks/saved_model/my_model")

def laser_callback(laser_data):
    #print(laser_data.ranges)
    lsr = np.float32(laser_data.ranges)
    lsr = lsr.reshape(1, lsr.shape[0], 1)
    lsr = np.where(lsr==np.inf, 10.0, lsr) 
    lsr = np.where(lsr==-np.inf, 10.0, lsr) 
    output = np.float32( new_model(lsr) )
    output = output[0]
    print(output)
    publish_command(output[0], output[5])
   

def publish_command(linear, angular):
    cmd = Twist()
    cmd.linear.x = linear
    cmd.angular.z = angular
    cmd_pub.publish(cmd)

# Connect to ROS
rospy.init_node('deep_navigation_node', anonymous=True)

# Subscribe to laser and command_velocity topic
rospy.Subscriber("/scan", LaserScan, laser_callback)
cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=2)

print("Ready!")

# Wait until program terminates
rospy.spin()
