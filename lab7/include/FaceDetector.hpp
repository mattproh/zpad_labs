#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
private:
    cv::dnn::Net net;
    
    std::thread workerThread;
    std::mutex dataMutex;
    std::atomic<bool> isRunning;

    cv::Mat currentFrame;
    bool hasNewFrame;
    std::vector<cv::Rect> detectedFaces;

    void backgroundProcessing();

public:
    FaceDetector();
    ~FaceDetector();

    void updateFrame(const cv::Mat& frame);
    std::vector<cv::Rect> getFaces();
};