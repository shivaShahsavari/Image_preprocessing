# Image_preprocessing

## the better the quality of the original source image, the higher the accuracy of OCR will be.  
“image quality” in this case means: “making it as easy as possible” for the OCR engine to distinguish a character from the background. Which means that we want to have:  
* sharp character borders
* high contrasts
* well aligned characters and
* as less pixel noise as possible

To have a better image quality, for sure image preprocessing have a key role. So, let's dive into different image preprocessing methods:  
## Scaling  
Ensure that the images are scaled to the right size which usually is of at least 300 DPI (Dots Per Inch). Keeping DPI lower than 200 will give unclear and incomprehensible results while keeping the DPI above 600 will unnecessarily increase the size of the output file without improving the quality of the file. Thus, a DPI of 300 works best for this purpose.  
* For regular text (font size > 8), it is recommended to go with 300 DPI itself  
* For smaller text (font size < 8), it is recommended to have 400–600 DPI  

## Contrast/ Sharpen  
Low contrast can result in poor OCR and Increasing the contrast between the text/image and its background brings out more clarity in the output.  

## Binarization  
This step converts a multicolored image (RGB) to a black and white image. Most OCR engines are internally working with monochrome images. So, better to conver and color image to monochrome image. Another advantage of binarizing your images before sending them to your OCR engine is the reduced size of your images.  
(we can binarize an image with cv2. threshold() . If type is set to cv2. THRESH_BINARY , any value greater than the threshold thresh is replaced with maxval and the other values are replaced with 0 )

## Noise removal  
Noise can drastically reduce the overall quality of the OCR process. It can be present in the background or foreground and can result from poor scanning or the poor original quality of the data. based on the nature of the source image, different types of noises may be present which needs to be handled in a specific way. Let us explore them now.
Blurring or Smoothing of an image removes “outlier” pixels that may be noise in the image. There are various filters that can be used to blur images and each has its own advantages and disadvantages.
 * **Gaussian Blur**: Uses Gaussian kernel for convolution and good at removing Gaussian noise from the image. It is much faster compared to other Blurring techniques but fails to preserve edges which may affect OCR output.
 * **Median Blur**: Replaces the central element in the kernel area with the median value of the pixels under the kernel area. It is good at removing salt and pepper noises from the scanned document.
 * **Bilateral Filtering**: It is highly effective in noise removal while keeping the edges sharp. Along with the Gaussian filter in space, it also takes another Gaussian filter which is a function of pixel difference. The Gaussian function of space makes sure that only nearby pixels are considered for blurring, while the Gaussian function of intensity difference makes sure that only those pixels with similar intensities to the central pixel are considered for blurring. So it preserves the edges since pixels at edges will have large intensity variation.

## Image Despeckling  
is a common technique used in the OCR noise removal step which is actually an adaptive bilateral filtering technique. It removes noises from the scanned image while preserving edges and other complex areas from blurring. It is very useful in removing granular marks from scanned images. When applied incorrectly it may remove commas and apostrophe from the image by considering them as noise.  

## Deskew  
This may also be referred to as rotation. The text should appear horizontal and not tilted in any angle. So, if the image is skewed to any side, deskew it by rotating it clockwise or anti clockwise direction.  

## Dilation and Erosion  
Bold characters or Thin characters (especially those with Serifs) may impact the recognition of details and reduce recognition accuracy. Many image processing programs allow Dilation and Erosion of edges of characters against a common background to dilate or grow in size (Dilation) or shrink (Erosion).
Heavy ink bleeding from historical documents can be compensated for by using an Erosion technique. Erosion can be used to shrink characters back to their normal glyph structure. 

## Keystone Effect/ Trapezoidal Distortion  
When the scanned document is not parallel to the scanner(camera), the source image captured will have a keystone effect (i.e) the shape of the source document will look like a trapezoid instead of a rectangle. This issue typically occurs while capturing / scanning images from mobile devices or digital cameras. For Keystone Correction, the system should first detect the trapezoid representing the scanned document, and do an affine transformation to convert the trapezoidal document into a rectangle, and then remove edges that do not contain any useful data.

## Border removal  
Scanned pages often have dark borders around them. These can be erroneously picked up as extra characters, especially if they vary in shape and gradation.  

## Correction of 3D perspective distortions  
This issue is more specific to images captured from Mobile devices or Digital cameras. Due to 3D perspective distortion, the Font Size of the document will vary from Top to Bottom, and also text at top of the page will not be clear. Once the image transformation is applied and corrected font size will look almost similar and gives better OCR results.
## Transparency / Alpha channel  
Some image formats (e.g. png) can have an alpha-channel for providing a transparency feature. Some libraries remove the alpha component by blending it with a white background. In some case (e.g. OCR of movie subtitles) this can lead to problems, so users would need to remove the alpha channel (or pre-process the image by inverting image colors) by themself.  
**Note** : The alpha channel is a color component that represents the degree of transparency (or opacity) of a color (i.e., the red, green and blue channels). It is used to determine how a pixel is rendered when blended with another.

## Lines Straightening  
When the lines are curvy as in the case of the above image, it may result in OCR issues and can cause issues with line segmentation and text re-arrangement. Hence, detecting the curved lines and straightening them will improve our OCR results.  

## ISO Noise Correction  
ISO level is the sensitivity level of the image sensor in the camera to the light. ISO gain which is an amplifier that improves the quality of the image in low light conditions will eventually amplify the noise as well which may affect the binarization step and therefore reduces OCR quality. By smoothening the image background, we will be able to reduce ISO noise and get better OCR results.  


## Layout/Zone Analysis  
In order to detect words correctly, it is important to first recognize the zones or the layout (which are also the areas of interest). This step detects the paragraphs, tables, columns, captions of the images etc. If the software misses out on any zone or layout, words might be cut in half or not detected at all.

## Image Denoising using Auto Encoders  
With the evolution of Deep Learning in Computer Vision, there has been a lot of research into image enhancement with Deep Neural Networks like removing noises from images, Image Super-Resolution, etc. Autoencoders are composed of an encoder and a decoder architecture. Where the encoder compresses the input data into a lower-dimensional representation and the decoder reconstructs the representation to obtain an output that mimics the input as closely as possible. In doing so, the autoencoder learns the most salient features of the input data.

### References:  
[Improve OCR accuracy by image preprocessing](https://docparser.com/blog/improve-ocr-accuracy/)  
[Tessaract image preprocessing](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html)  
[How to automatically deskew a text image using OpenCV](https://towardsdatascience.com/image-processing-with-python-blurring-and-sharpening-for-beginners-3bcebec0583a)  
[Survey on Image preprocessing techniques](https://medium.com/technovators/survey-on-image-preprocessing-techniques-to-improve-ocr-accuracy-616ddb931b76)


 
