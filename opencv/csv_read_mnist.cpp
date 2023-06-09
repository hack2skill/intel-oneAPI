#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <string>
#include <cstdlib>

using namespace std;
using namespace cv;


int reverseInt(int i) {
unsigned char c1, c2, c3, c4;
c1 = i & 255;
c2 = (i >> 8) & 255;
c3 = (i >> 16) & 255;
c4 = (i >> 24) & 255;
return ((int)c1 << 24) + ((int)c2 << 16) + ((int)c3 << 8) + c4;
}

void create_image(CvSize size, int channels, unsigned char* data, int imagenumber) {
string imgname; ostringstream imgstrm;string fullpath;
imgstrm << imagenumber;
imgname=imgstrm.str();
fullpath="/Users/omprakashvisvanathan/Documents/workspace/scalar/mnist/images/"+imgname+".jpg";

// opencv MAT image
//A = Mat(2, 5, CV_32FC1, &data);

IplImage *imghead=cvCreateImageHeader(size, IPL_DEPTH_16S, channels);
imghead->imageData=(char *)data;
cvSaveImage(fullpath.c_str(),imghead);  
}

int main(int argc, char **argv){

    std::cout << " prog open " << std::endl;

typedef unsigned char uchar;

//ifstream file ("train-images-idx3-ubyte",ios::binary);
ifstream file ("train-images-idx3-ubyte");
if (file.is_open())
{
    std::cout << " file open " << std::endl;

    int magic_number=0; int number_of_images=0;int r; int c;
    int n_rows=0; int n_cols=0;CvSize size;unsigned char temp=0;

    file.read((char*)&magic_number,sizeof(magic_number)); 
    magic_number= reverseInt(magic_number);

    if(magic_number != 2051) throw runtime_error("Invalid MNIST image file");

    file.read((char*)&number_of_images,sizeof(number_of_images));
    number_of_images= reverseInt(number_of_images);

    std::cout << " num images " <<  number_of_images << std::endl;

    file.read((char*)&n_rows,sizeof(n_rows));
    n_rows= reverseInt(n_rows);
    file.read((char*)&n_cols,sizeof(n_cols));
    n_cols= reverseInt(n_cols);

    int image_size = n_rows * n_cols;
    uchar** _dataset = new uchar*[number_of_images];
    for(int i = 0; i < number_of_images; i++) {
        _dataset[i] = new uchar[image_size];
        file.read((char *)_dataset[i], image_size);
    
        size.height=n_rows;size.width=n_cols;
        create_image(size,1, _dataset[i], i);
    }

    /*
    for(int i=0;i<number_of_images;++i)
    {
        for(r=0;r<n_rows;++r)
        {
            for(c=0;c<n_cols;++c)
            {                 
                file.read((char*)&temp,sizeof(temp));
            }           
        }
        size.height=r;size.width=c;
        create_image(size,1, &temp, i);
    }
    */

}
return 0;
}
