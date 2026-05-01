#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    // Параметри для інтерактиву
    static int brightness;
    static cv::Point mousePos;
    static bool isDrawing;
    static cv::Rect drawingBox;

    static void onMouse(int event, int x, int y, int flags, void* userdata);
    
    cv::Mat process(const cv::Mat& input, Mode mode);
};