import cv2
import numpy as np
import sys


# Detect the SIFT key feature points of A and B images and compute the feature descriptors
def detectAndDescribe(image):
    # Creating a SIFT generator
    sift = cv2.SIFT_create()
    # Detect SIFT feature points and compute descriptors
    (kps, features) = sift.detectAndCompute(image, None)
    # Converting results to NumPy arrays
    kps = np.float32([kp.pt for kp in kps])
    # Return the set of feature points, and the corresponding descriptive features
    return kps, features, sift


# Feature Matching, Return Perspective Transformation Matrix
def FeatureMatch(kpsA, featuresA, kpsB, featuresB):
    # Creating a Violent Matcher
    bf = cv2.BFMatcher()
    # Detecting SIFT feature matching pairs from A and B graphs using KNN, K=2
    matches = bf.knnMatch(featuresA, featuresB, 2)
    good = []
    for m in matches:
        # When the ratio of the closest distance to the next closest distance is less than the ratio value, the match is retained.
        if len(m) == 2 and m[0].distance < m[1].distance * 0.75:
            # Stores the indexes of the two points in featuresA, featuresB.
            good.append((m[0].trainIdx, m[0].queryIdx))

    # If the filtered matched pairs are greater than 4, calculate the perspective transformation matrix
    if len(good) > 4:
        # Get the coordinates of the points of the matched pair
        ptsA = np.float32([kpsA[i] for (_, i) in good])
        ptsB = np.float32([kpsB[i] for (i, _) in good])
        # Calculate the perspective transformation matrix
        H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4.0)
        return H, good

    # Return None if there are not enough matches
    return None, None


# Remove black borders after image stitching
def removeBlackBorders(image):
    # Convert to grayscale and threshold the image to find non-black areas
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours around the non-black areas
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(contours[0])

    # Crop the image to remove black borders
    cropped_image = image[y:y + h, x:x + w]
    return cropped_image


# My Picture Stitching
def MyImgStitching(imgRight, imgLeft):
    A = imgRight.copy()
    B = imgLeft.copy()
    imageA = cv2.resize(A, (0, 0), fx=0.2, fy=0.2)
    imageB = cv2.resize(B, (0, 0), fx=0.2, fy=0.2)

    # Detect the SIFT key feature points of A and B images and compute the feature descriptors
    kpsA, featuresA, siftA = detectAndDescribe(imageA)
    kpsB, featuresB, siftB = detectAndDescribe(imageB)

    # Match the features of A and B images
    H, goodMatches = FeatureMatch(kpsA, featuresA, kpsB, featuresB)
    if H is None:
        print("No matches, two images could not be stitched together")
        sys.exit()

    # Visualize key-points detection
    keypointsA = siftA.detect(imageA, None)
    keypointsB = siftB.detect(imageB, None)
    imageA_with_kps = cv2.drawKeypoints(imageA, keypointsA, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    imageB_with_kps = cv2.drawKeypoints(imageB, keypointsB, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show the key-points detected on both images
    cv2.imshow('Keypoints in Image A', imageA_with_kps)
    cv2.imshow('Keypoints in Image B', imageB_with_kps)

    # Convert good matches to DMatch format for visualization
    good_matches_dmatch = [cv2.DMatch(_[1], _[0], 0) for _ in goodMatches]

    # Draw matches
    match_img = cv2.drawMatches(imageA, keypointsA, imageB, keypointsB, good_matches_dmatch, None)

    # Show matching results
    cv2.imshow('Feature Matching', match_img)

    # Transform image A into a viewpoint, result is the transformed image.
    result = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

    # Pass image B into the leftmost part of the result image
    result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

    # Remove the black borders from the stitched image
    result = removeBlackBorders(result)

    # Returns the splicing result
    return result


if __name__ == "__main__":
    # Read input image
    imgRight = cv2.imread("5-2.jpg")  # Right side picture
    imgLeft = cv2.imread("5-1.jpg")  # Left side picture

    # Splice A and B pictures
    result = MyImgStitching(imgRight, imgLeft)

    # Showing pictures of the results after stitching
    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
