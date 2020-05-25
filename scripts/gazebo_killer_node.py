#!/usr/bin/env python
import rospy
import os

rospy.init_node("gazebo_killer")

# wait for shutdown signal
rospy.logwarn("Gazebo killer is ready!")
rospy.spin()

# shutdown gzserver and gzclient
rospy.logwarn("Killing gzserver and gzclient")
for i in range(5):
    os.system("killall -9 gzserver")
    os.system("killall -9 gzclient")
