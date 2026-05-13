#include "FaceDetector.hpp"
#include <iostream>

FaceDetector::FaceDetector() : hasNewFrame(false), isRunning(true) {
    try {
        net = cv::dnn::readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
    } catch (const cv::Exception& e) {
        std::cerr << "Network loading error: " << e.what() << std::endl;
    }
    workerThread = std::thread(&FaceDetector::backgroundProcessing, this);
}

FaceDetector::~FaceDetector() {
    isRunning = false;
    if (workerThread.joinable()) {
        workerThread.join();
    }
}

void FaceDetector::updateFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(dataMutex);
    currentFrame = frame.clone();
    hasNewFrame = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(dataMutex);
    return detectedFaces;
}

void FaceDetector::backgroundProcessing() {
    while (isRunning) {
        cv::Mat frameToProcess;
        
        {
            std::lock_guard<std::mutex> lock(dataMutex);
            if (!hasNewFrame || currentFrame.empty()) {
                continue;
            }
            frameToProcess = currentFrame.clone();
            hasNewFrame = false;
        }

        cv::Mat blob = cv::dnn::blobFromImage(frameToProcess, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
        
        net.setInput(blob);
        cv::Mat detection = net.forward();

        // Artificial load to demonstrate smooth video with parallel computing
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        std::vector<cv::Rect> newFaces;
        cv::Mat detectionMat(detection.size[2], detection.size[3], CV_32F, detection.ptr<float>());
        
        for (int i = 0; i < detectionMat.rows; i++) {
            float confidence = detectionMat.at<float>(i, 2);
            if (confidence > 0.5) { // Filter faces with confidence > 50%
                int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameToProcess.cols);
                int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameToProcess.rows);
                int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameToProcess.cols);
                int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameToProcess.rows);
                
                newFaces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
            }
        }

        {
            std::lock_guard<std::mutex> lock(dataMutex);
            detectedFaces = newFaces;
        }
    }
}