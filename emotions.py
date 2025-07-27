import os
import random

def load_emotion_image_pairs(root_dir="images"):
    emotion_image_pairs = []

    for folder_name in sorted(os.listdir(root_dir)):
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path):
            images = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ]
            if images:
                selected_image = random.choice(images)
                emotion_image_pairs.append((folder_name, selected_image))

    random.shuffle(emotion_image_pairs)
    return emotion_image_pairs