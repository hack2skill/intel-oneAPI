#include <CL/sycl.hpp>
#include <opencv2/opencv.hpp>
#include <cmath>
#include <iostream>
#include "dnnl.hpp"

using namespace cl::sycl;

std::vector<cv::Mat> loadImages(const std::vector<std::string>& imagePaths) {
    std::vector<cv::Mat> images;
    for (const auto& imagePath : imagePaths) {
        cv::Mat image = cv::imread(imagePath);
        cv::resize(image, image, cv::Size(120, 120));
        images.push_back(image);
    }
    return images;
}

int main() {
    std::vector<std::string> trainingImagePaths = {
        "/train/PNEUMONIA/person1000_bacteria_2931.jpeg",
        "/train/NORMAL/IM-0115-0001.jpeg"
    };

    std::vector<cv::Mat> trainingImages = loadImages(trainingImagePaths);

    std::vector<sycl::float3> trainingImageData;
    for (const auto& image : trainingImages) {
        for (int row = 0; row < image.rows; ++row) {
            for (int col = 0; col < image.cols; ++col) {
                cv::Vec3b pixel = image.at<cv::Vec3b>(row, col);
                sycl::float3 normalizedPixel(
                    static_cast<float>(pixel[0]) / 255.0f,
                    static_cast<float>(pixel[1]) / 255.0f,
                    static_cast<float>(pixel[2]) / 255.0f
                );
                trainingImageData.push_back(normalizedPixel);
            }
        }
    }

    std::vector<int> labels = { 1, 0 };

    auto deviceSelector = sycl::default_selector{};
    auto queue = sycl::queue{ deviceSelector };

    sycl::buffer<sycl::float3, 1> trainingDataBuffer(trainingImageData.data(), sycl::range(trainingImageData.size()));
    sycl::buffer<int, 1> labelsBuffer(labels.data(), sycl::range(labels.size()));
    sycl::buffer<float, 1> predictionsBuffer(sycl::range(labels.size()));

    dnnl::convolution_forward convolution;

    auto predictionsHost = predictionsBuffer.get_access<sycl::access::mode::read>();

    for (size_t i = 0; i < labels.size(); ++i) {
        std::cout << "The probability of pneumonia is: " << predictionsHost[i] << std::endl;
    }
}
