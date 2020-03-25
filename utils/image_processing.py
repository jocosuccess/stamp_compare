import os
import numpy as np
import cv2

from settings import CUR_DIR


def preprocess_image(frame_path, file_id):

    file_path = os.path.join(CUR_DIR, 'utils', "temp_{}.jpg".format(file_id))
    frame = cv2.imread(frame_path)

    # height, width = frame.shape[:2]
    bg_color = np.zeros((1, 3))
    for i in range(10):
        bg_color += frame[1][i]
    bg_color /= 10
    # origin_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if bg_color[0][0] >= 127 and bg_color[0][1] >= 127 and bg_color[0][2] >= 127:
        thresh_frame = cv2.threshold(frame_gray, 230, 255, cv2.THRESH_BINARY_INV)[1]
    else:
        thresh_frame = cv2.threshold(frame_gray, 100, 255, cv2.THRESH_BINARY)[1]

    # cv2.imshow("thresh frame", thresh_frame)
    # cv2.waitKey()

    contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contour = sorted(contours, key=cv2.contourArea, reverse=True)
    object_contour = sorted_contour[0]

    # cv2.drawContours(frame, [object_contour], 0, (0, 0, 255), 3)
    # cv2.imshow("frame", frame)
    # cv2.waitKey()
    # top_left_pt = get_closest_point_from_corner(corner=[0, 0], points=object_contour)
    # top_right_pt = get_closest_point_from_corner(corner=[width, 0], points=object_contour)
    # bottom_left_pt = get_closest_point_from_corner(corner=[0, height], points=object_contour)
    # bottom_right_pt = get_closest_point_from_corner(corner=[width, height], points=object_contour)
    # bottom_y = min(bottom_right_pt[1], bottom_left_pt[1])
    # top_y = max(top_right_pt[1], top_left_pt[1])
    # left_x = max(top_left_pt[0], bottom_left_pt[0])
    # right_x = min(top_right_pt[0], bottom_right_pt[0])
    # cv2.circle(frame, (top_left_pt[0], top_left_pt[1]), 3, (0, 0, 255), 2)
    # cv2.circle(frame, (top_right_pt[0], top_right_pt[1]), 3, (0, 0, 255), 2)
    # cv2.circle(frame, (bottom_left_pt[0], bottom_left_pt[1]), 3, (0, 0, 255), 2)
    # cv2.circle(frame, (bottom_right_pt[0], bottom_right_pt[1]), 3, (0, 0, 255), 2)
    # cv2.imshow("point frame", frame)
    # cv2.waitKey()
    # corner_points = np.float32([top_left_pt, top_right_pt, bottom_left_pt, bottom_right_pt])
    #
    # perspex_ratio = cv2.getPerspectiveTransform(corner_points, origin_points)
    # geo_frame = cv2.warpPerspective(frame_gray, perspex_ratio, (width, height))

    x, y, w, h = cv2.boundingRect(object_contour)
    obj_frame = frame_gray[y:y+h, x:x+w]
    # obj_frame = frame[top_y:bottom_y, left_x:right_x]
    # cv2.imshow("obj frame", obj_frame)
    # cv2.waitKey()

    cv2.imwrite(file_path, obj_frame)

    return file_path


def get_closest_point_from_corner(points, corner):

    points_dists = []
    for pt in points:
        dist = (pt[0][0] - corner[0]) ** 2 + (pt[0][1] - corner[1]) ** 2
        points_dists.append(dist)

    min_idx = points_dists.index(min(points_dists))

    return points[min_idx][0]


if __name__ == '__main__':

    preprocess_image(frame_path="", file_id=0)
