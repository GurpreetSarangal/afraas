# -*- coding: utf-8 -*-
# @Time : 20-6-9 下午3:06
# @Author : zhuying
# @Company : Minivision
# @File : test.py
# @Software : PyCharm

import os
import cv2
import numpy as np
import argparse
import warnings
import time

# from src.anti_spoof_predict import AntiSpoofPredict
from reports.src.anti_spoof_predict import AntiSpoofPredict
from reports.src.generate_patches import CropImage
from reports.src.utility import parse_model_name
warnings.filterwarnings('ignore')


SAMPLE_IMAGE_PATH = "./images/sample/"


# 因为安卓端APK获取的视频流宽高比为3:4,为了与之一致，所以将宽高比限制为3:4
def check_image(image):
    height, width, channel = image.shape
    # cv2.imshow("test", image);
    # print(str(width)+"  "+str(height)+"  "+str(width/height)+"  "+str(4/3))
    if width/height != 1:
        print("Image is not appropriate!!!\nHeight/Width should be 1:1.")
        return False
    else:
        return True


def test(image, model_dir, device_id):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()
    
    result = check_image(image)
    if result is False:
        return
    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))
    test_speed = 0
    # sum the prediction from single model's result
    for model_name in os.listdir(model_dir):
        # print(model_name)
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": image,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
        test_speed += time.time()-start

    # draw result of prediction
    label = np.argmax(prediction)
    value = prediction[0][label]/2
    # if label == 1:
    #     print("Image {} is Real Face. Score: {:.2f}.".format(label,  value))
    #     result_text = "RealFace Score: {:.2f}".format(label, value)
    #     color = (255, 0, 0)
    # else:
    #     print("Image {} is Fake Face. Score: {:.2f}.".format(label,  value))
    #     result_text = "FakeFace Score: {:.2f}".format(label, value)
    #     color = (0, 0, 255)
    print("Prediction cost {:.2f} s".format(test_speed))
    

    # format_ = os.path.splitext(image)[-1]
    # result_image = image.replace(format_, "_result" + format_)
    # cv2.imwrite(SAMPLE_IMAGE_PATH + result_image, image)

    return label


if __name__ == "__main__":
    desc = "test"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--device_id",
        type=int,
        default=0,
        help="which gpu id, [0/1/2/3]")
    parser.add_argument(
        "--model_dir",
        type=str,
        default="./resources/anti_spoof_models",
        help="model_lib used to test")
    parser.add_argument(
        "--image",
        type=str,
        default="image_F1.jpg",
        help="image used to test")
    args = parser.parse_args()
    test(args.image, args.model_dir, args.device_id)
