#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
    // Load images and check for failure
    Mat img1 = imread("1.jpg");
    Mat img2 = imread("2.jpg");
    if (img1.empty() || img2.empty()) {
        cerr << "Error loading images!" << endl;
        return -1;
    }

    // Create ORB detector
    Ptr<Feature2D> orb = ORB::create();

    // Detect and compute feature points and descriptors for both images
    vector<KeyPoint> keypoints1, keypoints2;
    Mat descriptors1, descriptors2;
    orb->detectAndCompute(img1, Mat(), keypoints1, descriptors1);
    orb->detectAndCompute(img2, Mat(), keypoints2, descriptors2);

    // Match descriptors using BFMatcher with Hamming distance
    BFMatcher matcher(NORM_HAMMING);
    vector<DMatch> matches;
    matcher.match(descriptors1, descriptors2, matches);

    // Extract point coordinates from good matches
    vector<Point2f> points1(matches.size()), points2(matches.size());
    for (size_t i = 0; i < matches.size(); ++i) {
        points1[i] = keypoints1[matches[i].queryIdx].pt;
        points2[i] = keypoints2[matches[i].trainIdx].pt;
    }

    // Use RANSAC to find the homography and filter matches
    vector<uchar> inliers_mask;
    Mat homography = findHomography(points1, points2, RANSAC, 3.0, inliers_mask);

    // Filter inliers
    vector<DMatch> inliers;
    inliers.reserve(matches.size());
    for (size_t i = 0; i < inliers_mask.size(); ++i) {
        if (inliers_mask[i]) {
            inliers.push_back(matches[i]);
        }
    }

    // Draw matches between the two images
    Mat result;
    drawMatches(img1, keypoints1, img2, keypoints2, inliers, result);

    // Display result
    imshow("Result", result);
    waitKey(0);

    return 0;
}
