import cv2
import numpy as np
from PIL import ImageEnhance, ImageOps
import PIL.Image
from matplotlib import pyplot as plt
from numpy.core.numeric import outer


class DigitalImageProcessing:
    def contrastEnhance(image_cv, factor):
        transform_image = PIL.Image.fromarray(image_cv)
        transform_image = ImageOps.grayscale(transform_image)
        enhancer = ImageEnhance.Contrast(transform_image)
        factor = factor
        img_output = enhancer.enhance(factor)
        return img_output

    def brightnessEnhance(image_cv, factor):
        transform_image = PIL.Image.fromarray(image_cv)
        transform_image = ImageOps.grayscale(transform_image)
        enhancer = ImageEnhance.Brightness(transform_image)
        factor = factor
        img_output = enhancer.enhance(factor)
        return img_output

    def sharpnessEnhance(image_cv, factor):
        transform_image = PIL.Image.fromarray(image_cv)
        transform_image = ImageOps.grayscale(transform_image)
        enhancer = ImageEnhance.Sharpness(transform_image)
        factor = factor
        img_output = enhancer.enhance(factor)
        return img_output

    def createMask(thresh):
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        big_contour = max(contours, key=cv2.contourArea)

        mask = np.zeros_like(thresh, dtype=np.uint8)

        mask = cv2.drawContours(mask, [big_contour], 0, 255, -1)

        return mask

    def segmentationProcess(smooth, image_cv, threshold=0, typeT=0):
        # threshold and invert

        ret, thresh1 = cv2.threshold(
            smooth,
            threshold,
            255,
            (cv2.THRESH_OTSU if typeT == 0 else cv2.THRESH_BINARY),
        )

        kernel = np.ones((21, 21), np.uint8)
        erosion = cv2.dilate(thresh1, kernel, iterations=2)
        mask = DigitalImageProcessing.createMask(erosion)

        result = image_cv.copy()
        result[mask == 0] = (0, 0, 0)

        return result

    def pre_process(image_path):

        img = cv2.imread(image_path)

        img = cv2.resize(img, (700, 700))

        opencvImage = cv2.cvtColor(
            np.array(DigitalImageProcessing.contrastEnhance(img, 1.5)), cv2.COLOR_RGB2BGR
        )

        gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)

        smooth = cv2.GaussianBlur(gray, (7, 7), 0)

        return smooth, opencvImage

    def featureExtration(image_pre):

        img_to_yuv = cv2.cvtColor(image_pre, cv2.COLOR_BGR2YUV)
        img_to_yuv[:, :, 0] = cv2.equalizeHist(img_to_yuv[:, :, 0])
        hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)

        gray = cv2.cvtColor(hist_equalization_result, cv2.COLOR_BGR2GRAY)

        ret, thresh1 = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)

        kernel = np.ones((6, 6), np.uint8)
        erosion = cv2.erode(thresh1, kernel, iterations=1)

        return erosion

    def edgeDetection(region_image, image_path):

        image = cv2.imread(image_path)
        image = cv2.resize(image, (700, 700))

        tight = cv2.Canny(region_image, 240, 255)
        rgb = cv2.cvtColor(
            tight, cv2.COLOR_GRAY2BGR
        )
        rgb *= np.array((0, 1, 0), np.uint8)

        teste = np.bitwise_or(image, rgb)

        added_image = cv2.cvtColor(teste, cv2.COLOR_RGBA2BGR)

        return added_image
