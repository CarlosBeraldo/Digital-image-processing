import cv2
import numpy as np
from PIL import ImageEnhance, ImageOps
import PIL.Image
from matplotlib import pyplot as plt
from numpy.core.numeric import outer


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

    def createMask(thresh):
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        big_contour = max(contours, key=cv2.contourArea)

        # make mask from contour
        mask = np.zeros_like(thresh, dtype=np.uint8)
        # teste = np.zeros_like(thresh, dtype=np.uint8)
        # print([big_contour])
        mask = cv2.drawContours(mask, [big_contour], 0, 255, -1)

        # result_img = cv2.cvtColor(teste, cv2.COLOR_GRAY2RGB)

        # teste = cv2.drawContours(result_img, [big_contour], 0, (255, 0, 0), -1)

        # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        # cv2.imshow("img", teste)
        # print(mask.shape)
        return mask

    def segmentationProcess(smooth, image_cv, threshold=0, typeT=0):
        # threshold and invert

        ret, thresh1 = cv2.threshold(
            smooth,
            threshold,
            255,
            (cv2.THRESH_OTSU if typeT == 0 else cv2.THRESH_BINARY),
        )
        # thresh1 = 255 - thresh1
        kernel = np.ones((21, 21), np.uint8)
        erosion = cv2.dilate(thresh1, kernel, iterations=2)
        mask = PreProcessing.createMask(erosion)
        # cv2.imshow("erosion", erosion)

        # make crop black everywhere except where largest contour is white in mask
        result = image_cv.copy()
        result[mask == 0] = (0, 0, 0)

        return result

    def pre_process(image_path):
        # read image
        img = cv2.imread(image_path)

        img = cv2.resize(img, (700, 700))

        opencvImage = cv2.cvtColor(
            np.array(PreProcessing.contrastEnhance(img, 1.5)), cv2.COLOR_RGB2BGR
        )
        # cv2.imshow("Contraste", opencvImage)
        gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(gray)
        smooth = cv2.GaussianBlur(gray, (7, 7), 0)

        # cv2.imshow("Filtro Gaussiano", smooth)

        # plt.hist(smooth.ravel(), 256, [0, 256])
        # plt.show()

        return smooth, opencvImage

    def featureExtration(image_pre):

        img_to_yuv = cv2.cvtColor(image_pre, cv2.COLOR_BGR2YUV)
        img_to_yuv[:, :, 0] = cv2.equalizeHist(img_to_yuv[:, :, 0])
        hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)
        # cv2.imshow("hist_equalization_result", hist_equalization_result)

        # img = cv2.resize(hist_equalization_result, (800, 800))
        # cv2.normalize(img, img, 0, 255, cv.NORM_MINMAX)

        gray = cv2.cvtColor(hist_equalization_result, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(gray)
        # smooth = cv2.GaussianBlur(gray, (3, 3), 0)

        ret, thresh1 = cv2.threshold(gray, 215, 255, cv2.THRESH_BINARY)

        # result = PreProcessing.segmentationProcess(
        #     smooth, hist_equalization_result, 240, 1
        # )
        # cv2.imshow("result", thresh1)

        # gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # # eq = cv2.equalizeHist(gray)
        # smooth = cv2.GaussianBlur(gray, (3, 3), 0)

        kernel = np.ones((9, 9), np.uint8)
        erosion = cv2.erode(thresh1, kernel, iterations=1)

        # cv2.imshow("limiar", thresh1)
        # cv2.imshow("erosion", erosion)
        # gray = cv2.cvtColor(image_pre, cv2.COLOR_BGR2GRAY)
        # eq = cv2.equalizeHist(erosion)
        return erosion

    def edgeDetection(region_image, image_path):

        image = cv2.imread(image_path)
        image = cv2.resize(image, (700, 700))

        tight = cv2.Canny(region_image, 240, 255)
        rgb = cv2.cvtColor(
            tight, cv2.COLOR_GRAY2BGR
        )  # RGB for matplotlib, BGR for imshow() !

        # step 2: now all edges are white (255,255,255). to make it red, multiply with another array:
        rgb *= np.array((0, 1, 0), np.uint8)  # set g and b to 0, leaves red :)

        # step 3: compose:
        cv2.imshow("rgb", rgb)

        teste = np.bitwise_or(image, rgb)
        # cv2.imshow("teste", teste)
        # print(out.shape)
        # out = cv2.resize(
        #     out, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA
        # )

        # add a alpha layer in the images
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        # out = cv2.cvtColor(rgb, cv2.COLOR_RGB2RGBA)

        # # blending the images
        # added_image = cv2.addWeighted(image, 1, out, 1, 0)

        # cv2.imshow("mesclado", teste)
        added_image = cv2.cvtColor(teste, cv2.COLOR_RGBA2BGR)

        # comp_a = cv2.cvtColor(comp_a, cv2.COLOR_RGBA2RGB)
        return added_image
