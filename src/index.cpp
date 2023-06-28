#include <CL/sycl.hpp>
#include <dpctl_sycl_queue_manager.hpp>
#include <opencv2/opencv.hpp>
#include <cmath>
#include <iostream>

namespace sycl = cl::sycl;

// Helper function to load and preprocess images
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

    std::vector<int> labels = { 1, 0 }; // PNEUMONIA = 1, NORMAL = 0

    // SYCL device selector
    auto deviceSelector = sycl::default_selector{};
    auto queue = sycl::queue{ deviceSelector };

    // Create buffers for training data and labels
    sycl::buffer<sycl::float3, 1> trainingDataBuffer(trainingImageData.data(), sycl::range<1>(trainingImageData.size()));
    sycl::buffer<int, 1> labelsBuffer(labels.data(), sycl::range<1>(labels.size()));

    // Create a buffer for storing predictions
    sycl::buffer<float, 1> predictionsBuffer(sycl::range<1>(labels.size()));

    // Define the kernel for prediction
    std::string kernelSourceCode = R"(
        kernel void predict(global const float3* trainingData,
                           global const int* labels,
                           global float* predictions) {
            size_t gid = get_global_id(0);
            float3 pixel = trainingData[gid];
            float probability = 0.0f; // Probability of pneumonia

            // Perform your prediction logic here
            // Modify the probability based on the pixel data

            predictions[gid] = probability;
        }
    )";

    // Compile the kernel and create a SYCL program
    sycl::program program(queue, kernelSourceCode);
    program.build();

    // Create a kernel from the compiled program
    sycl::kernel kernel(program, "predict");

    // Execute the kernel
    queue.submit([&](sycl::handler& cgh) {
        auto trainingDataAccessor = trainingDataBuffer.get_access<sycl::access::mode::read>(cgh);
        auto labelsAccessor = labelsBuffer.get_access<sycl::access::mode::read>(cgh);
        auto predictionsAccessor = predictionsBuffer.get_access<sycl::access::mode::write>(cgh);

        cgh.parallel_for<class predict>(sycl::range<1>(labels.size()), [=](sycl::item<1> item) {
            size_t gid = item.get_id(0);
            float3 pixel = trainingDataAccessor[gid];
            int label = labelsAccessor[gid];

            float probability = 0.0f; // Probability of pneumonia

            // Perform your prediction logic here
            // Modify the probability based on the pixel data

            predictionsAccessor[gid] = probability;
            });
        });

    // Access the predictions from the host
    auto predictionsHost = predictionsBuffer.get_access<sycl::access::mode::read>();

    // Display the predictions
    for (size_t i = 0; i < labels.size(); ++i) {
        std::cout << "The probability of pneumonia is: " << predictionsHost[i] << std::endl;
    }

    return 0;
}
