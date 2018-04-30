import numpy as np
import cv2 as cv

#Try addadImageFinal1.jpg , addadImageFinal2.jpg , addadImageFinal3.jpg , addadImageFinal4.jpg



def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))

def find_squares(img):
    img = cv.GaussianBlur(img, (7,7), 0)
    squares = []
    for gray in cv.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv.Canny(gray, 0, 20, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000  and  cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                           squares.append(cnt)
    return squares

def calculate(filename):
    W = 1000.
    oriimg = cv.imread(filename)
    height, width, depth = oriimg.shape
    imgScale = W/width
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    newimg = cv.resize(oriimg,(int(newX),int(newY)))
    #cv.imshow("Show by CV2",newimg)
    #cv.waitKey(0)
    cv.imwrite("resizeimg.jpg",newimg)
    from glob import glob
    for fn in glob('resizeimg.jpg'):
        img = cv.imread(fn)
        squares = find_squares(img)
    crop_img = img[min(squares[0][0][1],squares[0][1][1]):min(squares[0][2][1],squares[0][3][1]),min(squares[0][1][0],squares[0][2][0]):min(squares[0][0][0],squares[0][3][0])] 
    return crop_img

def preprocess(img_path) :

    imageToBeFilteredUsingOCR = calculate(img_path)
    # cv.imwrite('cropped.jpg',imageToBeFilteredUsingOCR)
    img = imageToBeFilteredUsingOCR[7:,170:400]
    img = cv.resize(img,(811,431))
    w,h = img.shape[:2]
    cv.imwrite('test.bmp',img)
