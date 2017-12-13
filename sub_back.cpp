#include "opencv2/imgcodecs.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>
//C
#include <stdio.h>
//C++
#include <iostream>
#include <sstream>
#include <string>
using namespace cv;
using namespace std;
// Global variables
Mat frame; //current frame
Mat fgMaskMOG; //fg mask fg mask generated by MOG2 method
Mat bkMask;
Mat fgFrame;
Mat bgFrame;
Mat finalMat;
Ptr<BackgroundSubtractor> pMOG; //MOG2 Background subtractor
int keyboard; //input from keyboard
void help();
void processVideo();

std::string type2string(cv::Mat mat)
{
	std::string r;
	switch (mat.depth()) {
	case CV_8U:
		r = "8U"; 
		break;
	case CV_8S:  
		r = "8S"; 
		break;
	case CV_16U: 
		r = "16U"; 
		break;
	case CV_16S: 
		r = "16S"; 
		break;
	case CV_32S: 
		r = "32S"; 
		break;
	case CV_32F: 
		r = "32F"; 
		break;
	case CV_64F: 
		r = "64F"; 
		break;
	default:
		r = "User"; 
		break;
  }
	r = r + "C" + std::to_string(mat.channels());
	return r;
}

int main(int argc, char* argv[])
{
    //print help information
    namedWindow("Frame");
    // namedWindow("FG Mask MOG 2");
    //create Background Subtractor objects
    pMOG = createBackgroundSubtractorMOG2(); //MOG2 approach
    processVideo();
    destroyAllWindows();
    return EXIT_SUCCESS;
}
void processVideo() {
    //create the capture object
    VideoCapture capture("video.mp4");
    if(!capture.isOpened()){
        //error in opening the video input
        cerr << "Unable to open camera: " << endl;
        exit(EXIT_FAILURE);
    }
    //read input data. ESC or 'q' for quitting
    while(1){
        //read the current frame
        if(!capture.read(frame)) {
            cerr << "Unable to read next frame." << endl;
            cerr << "Exiting..." << endl;
            exit(EXIT_FAILURE);
        }
        //update the background model
        pMOG->apply(frame, fgMaskMOG, -1);
	pMOG->getBackgroundImage(bgFrame);
	Mat element = getStructuringElement(MORPH_RECT, Size(3, 3), Point(-1, -1));
	cv::dilate(fgMaskMOG, fgMaskMOG, element, Point(-1, -1), 1);
	for (int i = 0; i < bkMask.rows; i++)
		for (int j = 0; j < bkMask.cols; ++j)
			if (fgMaskMOG.at<uchar>(i, j) > 0)
				fgMaskMOG.at<uchar>(i, j) = 255;
	cv::Mat floodFill = fgMaskMOG.clone();
	cv::floodFill(floodFill, cv::Point(0,0), cv::Scalar(255));
	bitwise_not(floodFill, floodFill);
	floodFill = fgMaskMOG | floodFill;
	fgMaskMOG = floodFill;
	cv::bitwise_not(fgMaskMOG, bkMask);
	imshow("bkMask", bkMask);
	//cout << "bkMask " << type2string(bkMask) << endl;
	cv::cvtColor(bkMask, bkMask, CV_GRAY2BGR);
	
	cv::bitwise_and(bkMask, frame, fgFrame);
	cout << "bkMask " << type2string(bgFrame) << " fgFrame " << type2string(fgFrame) << endl;
	cv::cvtColor(fgMaskMOG, fgMaskMOG, CV_GRAY2BGR);
	cv::bitwise_and(bgFrame, fgMaskMOG, bgFrame);
	cv::bitwise_or(fgFrame, bgFrame, finalMat);

        //show the current frame and the fg masks
        //imshow("Frame", frame);
	//imshow("Mask", fgMaskMOG);
	imshow("frame", frame);
	imshow("Bg frame", bgFrame);
	imshow("fgframe", fgFrame);
	//imshow("fgFrame - bgFrame", bgFrame- fgFrame);
	imshow("final frame", finalMat);

        //imshow("FrameMask", fgMaskMOG);
        // imshow("FG Mask MOG 2", fgMaskMOG);
        //get the input from the keyboard
        if(waitKey(30) > 0)
            break;
    }
    //delete capture object
    capture.release();
}