#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy as np
from sensor_msgs.msg import Image


class Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
                                          Image, self.image_callback)

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsv, (5, 5), 0)
        edge = cv2.Canny(blur, 20, 190)
        lower_yellow = np.array([0, 0, 70])
        upper_yellow = np.array([131, 255, 220])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        #
        xx = 20
        while True:
            area = edge[430:450, xx:xx + 15]
            if cv2.countNonZero(area) > 200:
                image = cv2.rectangle(image, (xx, 430), (xx + 15, 450), (0, 255, 0), 3)
            else:
                image = cv2.rectangle(image, (xx, 430), (xx + 15, 450), (255, 0, 0), 3)
            xx = xx + 20
            if xx > 640:
                break

        # # BEGIN CROP
        # h, w, d = image.shape
        # search_top = 3 * h / 4
        # search_bot = search_top + 20
        # mask[0:search_top, 0:w] = 0
        # mask[search_bot:h, 0:w] = 0
        # # END CROP
        # # BEGIN FINDER
        # M = cv2.moments(mask)
        # if M['m00'] > 0:
        #     cx = int(M['m10'] / M['m00'])
        #     cy = int(M['m01'] / M['m00'])
        #     # END FINDER
        #     # BEGIN CIRCLE
        #     cv2.circle(image, (cx, cy), 10, (0, 0, 255), -1)
        # # END CIRCLE
        #
        cv2.imshow("window", image)
        # cv2.imshow("hsv", hsv)
        # cv2.imshow("blur", blur)
        # cv2.imshow("line", mask)
        cv2.imshow("countNonZero", image)
        cv2.imshow("edge", edge)
        cv2.waitKey(3)


rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
