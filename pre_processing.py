import cv2
import numpy as np
from PIL import ImageEnhance, ImageOps
import PIL.Image


class PreProcessing:
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

    def segmentationProcess(smooth, image_cv, threshold=35):
        # threshold and invert
        ret, thresh1 = cv2.threshold(smooth, threshold, 255, cv2.THRESH_BINARY)
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
        crop = image_cv[first_y : last_y + 1, first_x : last_x + 1]

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
        return result

    def pre_process(image_path):
        # read image
        img = cv2.imread(image_path)

        opencvImage = cv2.cvtColor(
            np.array(PreProcessing.contrastEnhance(img, 1.3)), cv2.COLOR_RGB2BGR
        )
        gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(gray)
        smooth = cv2.GaussianBlur(gray, (3, 3), 0)

        return smooth, opencvImage

    def featureExtration(image_pre):

        opencvImage = cv2.cvtColor(
            np.array(PreProcessing.brightnessEnhance(image_pre, 0.6)), cv2.COLOR_RGB2BGR
        )
        img_to_yuv = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2YUV)
        img_to_yuv[:, :, 0] = cv2.equalizeHist(img_to_yuv[:, :, 0])
        hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)

        # img = cv2.resize(hist_equalization_result, (800, 800))
        # cv2.normalize(img, img, 0, 255, cv.NORM_MINMAX)

        gray = cv2.cvtColor(hist_equalization_result, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(gray)
        smooth = cv2.GaussianBlur(gray, (3, 3), 0)

        # result = PreProcessing.segmentationProcess(
        #     smooth, hist_equalization_result, 235
        # )
        ret, thresh1 = cv2.threshold(smooth, 240, 255, cv2.THRESH_TOZERO)

        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(thresh1, kernel)

        cv2.imshow("limiar", thresh1)
        cv2.imshow("erosion", erosion)
        # gray = cv2.cvtColor(image_pre, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(gray)
        return erosion

    def edgeDetection(region_image, image_path):

        image = cv2.imread(image_path)
        tight = cv2.Canny(region_image, 240, 250)
        rgb = cv2.cvtColor(
            tight, cv2.COLOR_GRAY2RGB
        )  # RGB for matplotlib, BGR for imshow() !

        # step 2: now all edges are white (255,255,255). to make it red, multiply with another array:
        rgb *= np.array((0, 0, 1), np.uint8)  # set g and b to 0, leaves red :)

        # step 3: compose:
        out = np.bitwise_or(rgb, rgb)

        out = cv2.resize(
            out, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA
        )

        # add a alpha layer in the images
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        out = cv2.cvtColor(out, cv2.COLOR_RGB2RGBA)

        # blending the images
        added_image = cv2.addWeighted(image, 1, out, 1, 0)

        cv2.imshow("mesclado", added_image)
        added_image = cv2.cvtColor(added_image, cv2.COLOR_RGBA2BGR)

        # comp_a = cv2.cvtColor(comp_a, cv2.COLOR_RGBA2RGB)
        return added_image
