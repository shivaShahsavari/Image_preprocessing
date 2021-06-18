from PIL import Image, ImageEnhance, ImageFilter
import os
import cv2 as cv
import numpy as np

########################### Preprocessing functions ####################################
############ Scaling to 300 dpi
def scaling(im):
    size=4061,4816
    im_resize=im.resize(size,Image.ANTIALIAS)
    im_resize.save(".\\preprocessing\\"+im.filename.split('.')[0]+'_300dpi.'+im.filename.split('.')[1],dpi=(600,600))

############ Removing borders
'''
cv.fillPoly(mask, cnts, [255,255,255])
mask = 255 - mask
result = cv.bitwise_or(im, mask)
'''
def border_rmv(im):
    mask = np.zeros(im.shape, dtype=np.uint8)
    #gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(im, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    cnts = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area < 10000:
            cv.drawContours(mask, [c], -1, (255,255,255), -1)

    #mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    result = cv.bitwise_and(im,im,mask=mask)
    result[mask==0] = 255
    return result 


############ binarize
def binarize(im):
    ret,im_bi=cv.threshold(im,150,255,cv.THRESH_BINARY)
    return im_bi


############ dilate/erosion    
def dilate(im):
    kernel = np.ones((2,2), np.uint8)
    img_dilation=cv.dilate(im,kernel,iterations=1)
    return img_dilation


############ Removing Noise by sharping and bilateral filtering
def noise_rm(im):
    im_converted = cv.cvtColor(im, cv.COLOR_BGR2RGB)# cv image to Pillow image
    pil_im = Image.fromarray(im_converted)
    im1=pil_im.filter(ImageFilter.UnsharpMask(radius=1,percent=150,threshold=2)) #Unsharp without using blur is better than with blur
    #im2=cv.GaussianBlur(im,(5,5),0) Median & Mode were better than GauissianBlur
    #im2=cv.medianBlur(img,5) # unsharp better than Median
    #im3=im.filter(ImageFilter.ModeFilter(3)) # unsharp better than Mode
    im_converted2=np.array(im1.convert('RGB')) # pillow image to cv image
    im4=cv.bilateralFilter(im_converted2,9,75,75)
    return im4

############ making contrast btwn colors
def contrast(im):
    im_converted = cv.cvtColor(im, cv.COLOR_BGR2RGB) # cv image to Pillow image
    pil_im = Image.fromarray(im_converted)
    enhancer=ImageEnhance.Contrast(pil_im)
    factor=5
    im_c=enhancer.enhance(factor)
    im_c2=np.array(im_c.convert('RGB')) # pillow image to cv image
    return im_c2


############ deskew
def getSkewAngle(cvImage,imageName):
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    #gray = cv.cvtColor(cvImage, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(newImage, (9, 9), 0)
    thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (30, 5))
    dilate = cv.dilate(thresh, kernel, iterations=11)
    # Find all contours
    contours, hierarchy = cv.findContours(dilate, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    image_copy = cvImage.copy()
    cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(36,255,12), thickness=3, lineType=cv.LINE_AA)
    cv.imwrite(".\\preprocessing\\"+imageName+'_contours.jpg', image_copy)
    contours = sorted(contours, key = cv.contourArea, reverse = True)
    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv.minAreaRect(largestContour)
    image_copy2 = cvImage.copy()
    box = cv.boxPoints(minAreaRect) # cv2.boxPoints(rect) for OpenCV 3.x
    box = np.int0(box)
    cv.drawContours(image_copy2,[box],0,(36,255,12),2)
    cv.imwrite(".\\preprocessing\\"+imageName+"_Large_contour.jpg", image_copy2)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    print('Angle : ',angle)
    if angle < -45:
        angle = -(90 + angle)
    elif angle > 45:
        angle = 90 - angle
    else: angle = - angle
    return  angle

def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv.warpAffine(newImage, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    return newImage

def deskew(cvImage,imageName):
    angle = getSkewAngle(cvImage,imageName)
    return rotateImage(cvImage, -1.0 * angle)


############ opening & closing
def opcl(im):
    kernel = np.ones((3,3), np.uint8)
    #useful in removing noise
    opn=cv.morphologyEx(im, cv.MORPH_OPEN, kernel,cv.BORDER_CONSTANT) 
    #useful in closing small holes inside the foreground objects, or small black points on the object.
    cl=cv.morphologyEx(im, cv.MORPH_CLOSE, kernel,cv.BORDER_CONSTANT) 
    return opn,cl



def main():
    im=Image.open('penguin-drawings.jpg')
    scaling(im)
    image_name=im.filename.split('.')[0]
    im_scaled=cv.imread(".\\preprocessing\\"+im.filename.split('.')[0]+'_300dpi.'+im.filename.split('.')[1],0)
    im_dsk=deskew(im_scaled,image_name)
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_deskew.'+im.filename.split('.')[1],im_dsk)
    im_brdr=border_rmv(im_dsk)
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_rmvBorder.'+im.filename.split('.')[1],im_brdr)
    im_bi=binarize(im_brdr) #Binarization without contrast better then with contrast
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_bnrz.'+im.filename.split('.')[1],im_bi)
    im_ers=dilate(im_bi)
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_dilation.'+im.filename.split('.')[1],im_ers)
    #im3=Image.open(".\\preprocessing\\"+im.filename.split('.')[0]+'_dilation.'+im.filename.split('.')[1])
    im_shrp=noise_rm(im_ers)
    ## check if you can convert 3D to 2D image
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_shrp.'+im.filename.split('.')[1],im_shrp) 
    im_opn,im_cl=opcl(im_shrp)
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_opening.'+im.filename.split('.')[1],im_opn)
    #cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'closing.'+im.filename.split('.')[1],im_cl)
    alpha_im = cv.cvtColor(im_opn, cv.COLOR_RGB2RGBA)
    cv.imwrite(".\\preprocessing\\"+im.filename.split('.')[0]+'_alpha.'+im.filename.split('.')[1],alpha_im)

    '''
    Note : all of below parameters need to be tuned:
    Scaling : Size
    Contrast : Factor
    Sharp : raduis, percent, threshold
    dilate : kernel matrix dimension
    '''


if __name__=="__main__":
    main()
