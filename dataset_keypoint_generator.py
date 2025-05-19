import cv2
import mediapipe as mp
import csv
import copy
import itertools
import string
import os

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Landmark processing functions
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []

    for landmark in landmarks.landmark:
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    base_x, base_y = temp_landmark_list[0]
    
    for point in temp_landmark_list:
        point[0] -= base_x
        point[1] -= base_y

    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
    max_value = max(map(abs, temp_landmark_list)) or 1
    return [val / max_value for val in temp_landmark_list]

def logging_csv(letter, landmark_list, csv_path='keypoint.csv'):
    with open(csv_path, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([letter] + landmark_list)

# Settings
alphabet = list(string.ascii_uppercase) + [str(i) for i in range(1, 10)]
samples_per_class = 1199  # Updated to collect exactly 1199 images
image_base_path = '/Users/saimonesh/Dev/Finalyear/Indian-DataSet'

# Start Mediapipe
with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
    for letter in alphabet:
        folder = os.path.join(image_base_path, letter)
        if not os.path.exists(folder):
            print(f"[WARNING] Folder missing: {folder}")
            continue

        collected = 0
        for i in range(samples_per_class):
            img_path = os.path.join(folder, f"{i}.jpg")
            if not os.path.exists(img_path):
                print(f"[WARNING] Missing image: {img_path}")
                continue

            image = cv2.flip(cv2.imread(img_path), 1)
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmark_list = calc_landmark_list(image, hand_landmarks)
                    processed_list = pre_process_landmark(landmark_list)
                    logging_csv(letter, processed_list)
                    collected += 1

            if collected >= samples_per_class:
                break

        print(f"[INFO] Collected {collected} samples for '{letter}'")

print("[DONE] Dataset generation complete.")
