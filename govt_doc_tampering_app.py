# -*- coding: utf-8 -*-
"""GOVT_DOC_TAMPERING_APP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1McpNW-hoDuJ7AEmWGGlAaU_Pv4_oJ1Bh
"""

# To find structural similarities between actual and other image

from skimage.metrics import structural_similarity

# to get contour / irregular figure / outlines of an image

import imutils

# for computer vision and image processing

import cv2

# to download image & visualise it

from PIL import Image

# to fetch data from url

import requests

!mkdir doc_tampering

!mkdir doc_tampering/images

# getting images from third party site using requests

original = Image.open(requests.get("https://www.thestatesman.com/wp-content/uploads/2019/07/pan-card.jpg", stream = True).raw)
tampered = Image.open(requests.get("https://assets1.cleartax-cdn.com/s/img/20170526124335/Pan4.png", stream = True).raw)

# original & tampered image format

print ("Original Image format : ", original.format)
print ("Tampered Image format : ", tampered.format)

# original & tampered image size

print ("Original Image size : ", original.size)
print ("Tampered Image size : ", tampered.size)

""" Resizing both images to same size & format"""

# Resizing original image

original = original.resize((250,160))
print(original.size)

# saving resized image

original.save('doc_tampering/images/original.png')

# Resizing tampered image

tampered = tampered.resize((250,160))
print(tampered.size)

# saving resized image

tampered.save('doc_tampering/images/tampered.png')

original

tampered

"""Loading these images using cv2 to apply some of its functions"""

# loading images

original = cv2.imread('/content/doc_tampering/images/original.png')
tampered = cv2.imread('/content/doc_tampering/images/tampered.png')

Image.fromarray(tampered)

# converting images to grascale

original_gry = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
tampered_gry = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)

original_gry

tampered_gry

"""Finding structural similarities between images"""

# finding similarity as well as difference score

(score, diff) = structural_similarity(original_gry, tampered_gry, full = True)

# multiplying difference with 255 to normalize it

diff = (diff*255).astype('uint8')

print("Structural Similarity : {}".format(score))

"""Calculating threshold & contours"""

# in threshhold, we are passing the difference, image size is between 0 to 255 and converting them into binary & OTSU

thresh = cv2.threshold (diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) [1]

cnts = cv2.findContours (thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)

# creating a bounding rectangle using contours to get width and height of both the images

for c in cnts :

  # applying contours on image

  (x,y,w,h) = cv2.boundingRect(c)
  cv2.rectangle(original, (x,y), (x+w, y+h), (0,0,255), 2)
  cv2.rectangle(tampered, (x,y), (x+w, y+h), (0,0,255), 2)

"""Visualizing images"""

# Display original image with contour

print ('Original format Image')
Image.fromarray(original)

# Display original image with contour

print ('Tampered format Image')
Image.fromarray(tampered)

# Display difference image with black

print ('Original format Image')
Image.fromarray(diff)

# Display threshold image with white

print ('Threshold Image')
Image.fromarray(thresh)

if score < 0.75:
  print ('Document is fake')
else:
  print ("Document is Real")

"""As we can see that Similarity score is ~31%, also from images, it can be stated that the provided document is fake"""