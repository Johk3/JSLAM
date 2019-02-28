#include <opencv2/highgui.hpp>
#include "opencv2/imgproc.hpp"
#include "opencv2/video/background_segm.hpp"
#include "opencv2/video/tracking.hpp"
#include <iostream>
 
int main( int argc, char** argv ) {
  // Use these compiler option to run the code
  // g++ main.cpp -o output `pkg-config --cflags --libs opencv`
  // This is the section for reading a image
//  cv::Mat image;
//  image = cv::imread("frame.png" , CV_LOAD_IMAGE_COLOR);
//  
//  if(! image.data ) {
//      std::cout <<  "Could not open or find the image" << std::endl ;
//      return -1;
//    }
//  
//  cv::namedWindow( "Jslam", cv::WINDOW_AUTOSIZE );
//  cv::imshow( "Jslam", image );
//  
//  cv::waitKey(0);

  cv::VideoCapture cap("media/fastcar.mp4");
  cv::namedWindow("frame", cv::WINDOW_AUTOSIZE);
  if(!cap.isOpened()){
      std::cout << "Error opening video stream or file" << "\n";
      return -1;
  }
  
  while(1){
      int W = cap.get(cv::CAP_PROP_FRAME_WIDTH)/2;
      int H = cap.get(cv::CAP_PROP_FRAME_HEIGHT)/2;
      
      cv::Mat frame;
	  cv::Mat outframe;
      // Capture frame-by-frame
      cap >> frame;
	  
      if(frame.empty())
          break;
	  
	  cv::resize(frame, outframe, cv::Size(), 0.50, 0.50);
      cv::imshow("frame", outframe);
      char c=(char)cv::waitKey(25);
      if(c==27)
          break;
  }
  // When everything is done, release the video capture
  cap.release();
  //Closes all the frames
  cv::destroyAllWindows();
  
  return 0;
}