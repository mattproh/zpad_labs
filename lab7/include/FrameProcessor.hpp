#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"
#include <vector>

class FrameProcessor {
private:
    int64 lastTick = 0; // For FPS calculation
public:
    static int brightness;
    static cv::Point mousePos;
    static bool isDrawing;
    static cv::Rect drawingBox;

    static void onMouse(int event, int x, int y, int flags, void* userdata);
    
    // Now this receives a list of rectangles (faces)
    cv::Mat process(const cv::Mat& input, Mode mode, const std::vector<cv::Rect>& faces);
};