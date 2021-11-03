import cv2
import numpy as np
from PIL import ImageEnhance, ImageOps
import PIL.Image


class PreProcessing:
    def pre_process(image_path):
        # read image
        img = cv2.imread(image_path)

        # convert to gray

        transform_image = PIL.Image.fromarray(img)
        transform_image = ImageOps.grayscale(transform_image)

        enhancer = ImageEnhance.Contrast(transform_image)
        factor = 0.7
        img_output = enhancer.enhance(factor)
        opencvImage = cv2.cvtColor(np.array(img_output), cv2.COLOR_RGB2BGR)
        cv2.imshow("opencvImage", opencvImage)

        gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(gray)
        smooth = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow("smooth", smooth)

        # threshold and invert
        ret, thresh1 = cv2.threshold(smooth, 35, 255, cv2.THRESH_BINARY)

        cv2.imshow("thresh", thresh1)
        thresh1 = 255 - thresh1

        # remove borders
        # count number of white pixels in columns as new 1D array
        count_cols = np.count_nonzero(thresh1, axis=0)

        # get first and last x coordinate where black
        first_x = np.where(count_cols > 0)[0][0]
        last_x = np.where(count_cols > 0)[0][-1]

        # count number of white pixels in rows as new 1D array
        count_rows = np.count_nonzero(thresh1, axis=1)

        # get first and last y coordinate where black
        first_y = np.where(count_rows > 0)[0][0]
        last_y = np.where(count_rows > 0)[0][-1]

        # crop image
        crop = img[first_y : last_y + 1, first_x : last_x + 1]

        # crop thresh1 and invert
        thresh2 = thresh1[first_y : last_y + 1, first_x : last_x + 1]
        thresh2 = 255 - thresh2

        # get external contours and keep largest one
        contours = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        big_contour = max(contours, key=cv2.contourArea)

        # make mask from contour
        mask = np.zeros_like(thresh2, dtype=np.uint8)
        cv2.drawContours(mask, [big_contour], 0, 255, -1)

        # make crop black everywhere except where largest contour is white in mask
        result = crop.copy()
        result[mask == 0] = (0, 0, 0)

        transform_image = PIL.Image.fromarray(result)
        transform_image = ImageOps.grayscale(transform_image)

        enhancer = ImageEnhance.Sharpness(transform_image)
        factor = 2  # imagem escura com 50% de Contraste.
        img_output = enhancer.enhance(factor)

        opencvImage = cv2.cvtColor(np.array(img_output), cv2.COLOR_RGB2BGR)

        return opencvImage
