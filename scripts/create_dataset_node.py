#!/anaconda3/envs/tensorflow/bin/python
import sys
sys.path.append('/usr/local/lib/python3.6/dist-packages')

import tensorflow
print("tensorflow imported successfully")

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
print("rospy imported successfully")

import csv
import os
csv_file = open(os.path.dirname(__file__) + "/../notebooks/dataset.csv", 'w', newline='')
csv_writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)



laser_msg = None
def laser_callback(laser_data):
    global laser_msg
    laser_msg = laser_data

def cmd_callback(cmd_data):
    if laser_msg != None:
        laser_msg_ = laser_msg
        cmd_arr = [cmd_data.linear.x, cmd_data.linear.y, cmd_data.linear.z, cmd_data.angular.x, cmd_data.angular.y, cmd_data.angular.z]
        csv_writer.writerow(cmd_arr + list(laser_msg_.ranges))
        

# Connect to ROS
rospy.init_node('create_dataset_node', anonymous=True)

# Subscribe to laser and command_velocity topic
rospy.Subscriber("/scan", LaserScan, laser_callback)
rospy.Subscriber("/cmd_vel", Twist, cmd_callback)

# Wait until program terminates
rospy.spin()

csv_file.close()
