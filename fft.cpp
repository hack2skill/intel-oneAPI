#include <stdio.h>
#include <iostream>
#include <math.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

extern fft2(double **img, int s, int r, int c);

int mainfft2() {


    //  double ** fft()
    /// Read image given by user
    Mat image = imread("Lenna.png");
    Mat new_image = Mat::zeros( image.size(), image.type() );

    /// Initialize values
    std::cout<<" Basic FFT  Transforms "<<std::endl;
    std::cout<<"-------------------------"<<std::endl;
   // std::cout<<"* Enter the alpha value [1.0-3.0]: ";std::cin>>alpha;
   //std::cout<<"* Enter the beta value [0-100]: "; std::cin>>beta;

    // only powers of 2 at this time

    int N = image.rows * image.cols;

    int numsteps = log2(N); 

    Vec3b coords[numsteps]; 

    cv::Mat dst;

    // Convert to double (much faster than a simple for loop)
    image.convertTo(dst, CV_64F, 1, 0);

    double *ptrDst[dst.rows];
    for(int i = 0;i<dst.rows;++i) {
       ptrDst[i] = dst.ptr<double>(i);

    //   for(int j = 0; j < dst.cols; ++j) {
    //       double value = ptrDst[i][j];
    //   }

    }

       fft2(ptrDst, N, dst.rows, dst.cols);

    /*
    for(int i = 0;i<dst.rows;++i) {

       for(int j = 0; j < dst.cols; ++j) {
           double value = ptrDst[i][j];
           std::cout << value;
       }
           std::cout << std::endl;
    }
     */

//       fft2(ptrDst, N, dst.rows, dst.cols);


   

    /*
    /// Do the operation new_image(i,j) = alpha*image(i,j) + beta
    for( int y = 0; y < image.rows; y++ )
    { 
        for( int x = 0; x < image.cols; x++ )
        { 

            if(x == y && x )
            



            for( int c = 0; c < 3; c++ )
            {
                new_image.at<Vec3b>(y,x)[c] =
                    saturate_cast<uchar>( alpha*( image.at<Vec3b>(y,x)[c] ) + beta );
            }
        }
    }
    */

}
