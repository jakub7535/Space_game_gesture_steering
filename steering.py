import cv2
import numpy as np
import math
import mediapipe as mp
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
import time
from google.protobuf.json_format import MessageToDict


class HandDetector:
    def __init__(self, screen_height, screen_width, mode=False, max_hands=2, 
                 detection_confidence=0.5, tracking_confidence=0.5,
                 draw_hands=True):
        self.mode = mode
        self.max_hands = max_hands
        self.draw_hands = draw_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.hands_detection = mp_hands.Hands(self.mode, self.max_hands, 
                                              self.detection_confidence,
                                              self.tracking_confidence)

        self.tipIds = [4, 8, 12, 16, 20]
        self.img = None
        self.imgRGB = None
        self.screen_height, self.screen_width = screen_height, screen_width
        self.results = None
        self.left_hand = None
        self.right_hand = None


    def get_hands_params(self, img):
        self.img = img
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.left_hand = None
        self.right_hand = None

        self.results = self.hands_detection.process(self.imgRGB)
        if not self.results.multi_hand_landmarks:
            return
        for hand_id, hand_info in enumerate(self.results.multi_hand_landmarks):
            hand_info_dict = MessageToDict(self.results.multi_handedness[hand_id])
            index = hand_info_dict['classification'][0]['index']
            prediction_confidence = hand_info_dict['classification'][0]['score']
            left_or_right = hand_info_dict['classification'][0]['label']
            point_list = []
            for id, point in enumerate(hand_info.landmark):
                point_x = int(point.x * self.screen_width)
                point_y = int(point.y * self.screen_height)
                point_list.append([point_x, point_y])
            # calculate hand center
            hand_center = center_points(point_list[0], point_list[9])

            fingers_extended = []

            thumb_index_dist = distance_points(point_list[4], point_list[6])
            index_middle_dist = distance_points(point_list[6], point_list[10])
            if thumb_index_dist > 1.8 * index_middle_dist:
                fingers_extended.append(1)
            else:
                fingers_extended.append(0)

            for id in range(1, 5):
                tip_distance = distance_points(point_list[self.tipIds[id]],
                                               point_list[self.tipIds[id]-3])
                dip_distance = distance_points(point_list[self.tipIds[id]-2],
                                               point_list[self.tipIds[id]-3])
                if tip_distance > 1.2*dip_distance:
                    fingers_extended.append(1)
                else:
                    fingers_extended.append(0)

            if self.draw_hands:
                mp_draw.draw_landmarks(img, hand_info,
                                           mp_hands.HAND_CONNECTIONS)
                cv2.circle(self.img, hand_center, 10, (255, 0, 255), cv2.FILLED)

            hand = SingleHandParameters(index, prediction_confidence, left_or_right,
                                        point_list, hand_center, fingers_extended)
            if hand.left_or_right == 'Left':
                self.left_hand = hand
            else:
                self.right_hand = hand



class SingleHandParameters:
    def __init__(self, index, prediction_confidence, left_or_right, point_dict,
                 hand_center, fingers_extended):
        self.index = index
        self.prediction_confidence = prediction_confidence
        self.left_or_right = left_or_right
        self.point_dict = point_dict
        self.hand_center = hand_center
        self.fingers_extended = fingers_extended


class Steering:
    def __init__(self,  screen_height, screen_width,  wheel_img_original='wheel_2.png',
                 arrow_img='arrow_direction.png'):
        self.wheel_img_original = cv2.imread("assets/{}".format(wheel_img_original), -1)
        self.arrow_left_img = cv2.imread("assets/{}".format(arrow_img), -1)
        self.arrow_right_img = cv2.flip(self.arrow_left_img, 1)
        self.img = None
        self.screen_height = int(screen_height)
        self.screen_width = int(screen_width)
        self.wheel_radius = None
        self.wheel_center = None
        self.wheel_angle = None
        self.turn = None
        self.shot_pause_time = time.time()

    def calculate_wheel(self, img, left_hand, right_hand):
        self.img = img
        if left_hand is None or right_hand is None:
            self.wheel_radius = None
            self.wheel_center = None
            self.wheel_angle = None
            return

        wheel_radius_test = max(int(0.5 * distance_points(left_hand.hand_center,
                                                          right_hand.hand_center)), 10)
        if wheel_radius_test > 0.1*self.screen_width:
            wheel_radius = wheel_radius_test
        else:
            self.wheel_radius = None
            self.wheel_center = None
            self.wheel_angle = None
            return

        wheel_center = center_points(left_hand.hand_center, right_hand.hand_center)
        #cv2.circle(self.img, wheel_center, 10, (255, 0, 255), cv2.FILLED)
        wheel_angle = math.atan2((right_hand.hand_center[1]-left_hand.hand_center[1]),
                                 (right_hand.hand_center[0]-left_hand.hand_center[0]))
        wheel_angle = -math.degrees(wheel_angle)
        self.wheel_radius = wheel_radius
        self.wheel_center = wheel_center
        self.wheel_angle = wheel_angle
        #self.draw_wheel()

    def draw_wheel(self):
        wheel_img = self.wheel_img_original.copy()
        wheel_img = cv2.resize(wheel_img,
                               (2 * self.wheel_radius, 2 * self.wheel_radius))
        wheel_img = rotate_image(wheel_img, self.wheel_angle)

        img_chunk_x1 = int(max(0, self.wheel_center[0] - self.wheel_radius))
        img_chunk_x2 = int(min(self.screen_width,
                                self.wheel_center[0] + self.wheel_radius))
        img_chunk_y1 = int(max(0, self.wheel_center[1] - self.wheel_radius))
        img_chunk_y2 = int(min(self.screen_height,
                                self.wheel_center[1] + self.wheel_radius))

        wheel_img_chunk_x1, wheel_img_chunk_x2 = 0, 2 * self.wheel_radius
        wheel_img_chunk_y1, wheel_img_chunk_y2 = 0, 2 * self.wheel_radius

        if self.wheel_center[0] - self.wheel_radius < 0:
            wheel_img_chunk_x1 = self.wheel_radius - self.wheel_center[0]
        if self.wheel_center[0] + self.wheel_radius > self.screen_width:
            wheel_img_chunk_x2 = self.screen_width + self.wheel_radius\
                                 - self.wheel_center[0]
        if self.wheel_center[1] - self.wheel_radius < 0:
            wheel_img_chunk_y1 = self.wheel_radius - self.wheel_center[1]
        if self.wheel_center[1] + self.wheel_radius > self.screen_height:
            wheel_img_chunk_y2 = self.screen_height + self.wheel_radius\
                                 - self.wheel_center[1]
        wheel_img = wheel_img[int(wheel_img_chunk_y1):int(wheel_img_chunk_y2),
                    int(wheel_img_chunk_x1):int(wheel_img_chunk_x2)]

        alpha_s = wheel_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            self.img[img_chunk_y1:img_chunk_y2, img_chunk_x1:img_chunk_x2, c] = \
                (alpha_s * wheel_img[:, :, c] +
                 alpha_l * self.img[img_chunk_y1:img_chunk_y2,
                           img_chunk_x1:img_chunk_x2, c])


    def get_commands(self, detector):
        turn = None
        shot = False
        if self.wheel_angle > 0:
            turn = min(60, (max(5, self.wheel_angle)))
            #self.draw_turns(turn)
        elif self.wheel_angle <= 0:
            turn = max(-60, (min(-5, self.wheel_angle)))
            #self.draw_turns(turn)

        fire = (detector.right_hand.fingers_extended[0] == 1 and
                detector.left_hand.fingers_extended[0] == 1 and
                not any([detector.left_hand.fingers_extended[i] for i in range(1, 5)]) and
                not any([detector.left_hand.fingers_extended[i] for i in range(1, 5)]))

        if fire:
            cv2.putText(self.img, "FIRE!", (20, int(self.screen_height*0.4)),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 10)
            if time.time() - self.shot_pause_time > 0.2:
                shot = True
                self.shot_pause_time = time.time()
        self.turn = turn
        return turn, shot

    def draw_turns_png(self, x1, y1, arrow_img, turn):
        arrow_img = cv2.resize(arrow_img, (int(abs(turn) * 0.003 * self.screen_width),
                               int(abs(turn) * 0.003 * self.screen_height)))

        if turn > 0:
            x1, x2 = x1, int(x1 + arrow_img.shape[1])
            y1, y2 = y1, int(y1 + arrow_img.shape[0])
        else:
            x1, x2 = int(x1 - arrow_img.shape[1]), x1
            y1, y2 = y1, int(y1 + arrow_img.shape[0])

        alpha_s = arrow_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            self.img[y1:y2, x1:x2, c] = (alpha_s * arrow_img[:, :, c] +
                                      alpha_l * self.img[y1:y2, x1:x2, c])


    def draw_turns(self, turn):
        size = int(1.2 * abs(turn))
        off_side = int(10)
        line_thickness = int(size/3)
        point_a = [off_side, size + off_side]
        point_b = [3 * size + off_side, size + off_side]
        point_c = [size + off_side, off_side]
        point_d = [size + off_side, 2 * size + off_side]
        if turn>0:
            point_a[0] = self.screen_width - point_a[0]
            point_b[0] = self.screen_width - point_b[0]
            point_c[0] = self.screen_width - point_c[0]
            point_d[0] = self.screen_width - point_d[0]

        cv2.line(self.img, (point_a[0], point_a[1]), (point_b[0], point_b[1]),
                 (0, 0, 255), line_thickness)
        cv2.line(self.img, (point_a[0], point_a[1]), (point_c[0], point_c[1]),
                 (0, 0, 255), line_thickness)
        cv2.line(self.img, (point_a[0], point_a[1]), (point_d[0], point_d[1]),
                 (0, 0, 255), line_thickness)


        #cv2.line(self.img, (x1, y1), (x2, y2), (0, 255, 0),





def center_points(point_1, point_2):
    center_x = int(0.5*(point_1[0] + point_2[0]))
    center_y = int(0.5*(point_1[1] + point_2[1]))
    return (center_x, center_y)

def distance_points(point_1, point_2):
    x = abs(point_1[0] - point_2[0])
    y = abs(point_1[1] - point_2[1])
    distance = (x**2 + y**2)**0.5
    return distance

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  img_result = cv2.warpAffine(image, rot_mat, image.shape[1::-1],
                              flags=cv2.INTER_LINEAR)
  return img_result


def main():
    vid = cv2.VideoCapture(0)
    screen_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    screen_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    detector = HandDetector(screen_height, screen_width, draw_hands=False)
    wheel_img = cv2.imread("wheel.png", -1)
    arrow_left_img = cv2.imread("arrow_left.png", -1)
    arrow_right_img = cv2.imread("arrow_right.png", -1)
    screen_steering = ScreenSteering(screen_height, screen_width, wheel_img,
                                     arrow_left_img, arrow_right_img)

    while True:
        _, img = vid.read()
        img = cv2.flip(img, 1)
        detector.get_hands_params(img)

        if detector.right_hand is not None and detector.left_hand is not None:
            screen_steering.calculate_wheel(img, detector.left_hand,
                                            detector.right_hand)
            if screen_steering.wheel_radius is not None:
                turn, shot = screen_steering.get_commands(detector)


        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
            vid.release()
            cv2.destroyAllWindows()



if __name__ == "__main__":
    main()