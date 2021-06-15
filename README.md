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

## Contrast/ Sharpen  
Low contrast can result in poor OCR and Increasing the contrast between the text/image and its background brings out more clarity in the output.  

## Binarization  
This step converts a multicolored image (RGB) to a black and white image. Most OCR engines are internally working with monochrome images. So, better to conver and color image to monochrome image. Another advantage of binarizing your images before sending them to your OCR engine is the reduced size of your images.  

## Noise removal  
Noise can drastically reduce the overall quality of the OCR process. It can be present in the background or foreground and can result from poor scanning or the poor original quality of the data.  

## Deskew  
This may also be referred to as rotation. The text should appear horizontal and not tilted in any angle. So, if the image is skewed to any side, deskew it by rotating it clockwise or anti clockwise direction.  

## Dilation and Erosion  




## Layout/Zone Analysis  
In order to detect words correctly, it is important to first recognize the zones or the layout (which are also the areas of interest). This step detects the paragraphs, tables, columns, captions of the images etc. If the software misses out on any zone or layout, words might be cut in half or not detected at all.

**References:  
[Improve OCR accuracy by image preprocessing](https://docparser.com/blog/improve-ocr-accuracy/)

 
