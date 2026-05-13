#include "FrameProcessor.hpp"

// Ініціалізація статичних змінних
int FrameProcessor::brightness = 50; 
cv::Point FrameProcessor::mousePos(-1, -1);
bool FrameProcessor::isDrawing = false;
cv::Rect FrameProcessor::drawingBox(0, 0, 0, 0);

void FrameProcessor::onMouse(int event, int x, int y, int flags, void* userdata) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        isDrawing = true;
        drawingBox = cv::Rect(x, y, 0, 0);
    } else if (event == cv::EVENT_MOUSEMOVE && isDrawing) {
        drawingBox.width = x - drawingBox.x;
        drawingBox.height = y - drawingBox.y;
    } else if (event == cv::EVENT_LBUTTONUP) {
        isDrawing = false;
        drawingBox.width = x - drawingBox.x;
        drawingBox.height = y - drawingBox.y;
    }
}

cv::Mat FrameProcessor::process(const cv::Mat& input, Mode mode) {
    cv::Mat output;
    
    // 1. Застосування режимів обробки [cite: 132]
    switch (mode) {
        case Mode::INVERT:
            cv::bitwise_not(input, output); // [cite: 134]
            break;
        case Mode::BLUR:
            cv::GaussianBlur(input, output, cv::Size(15, 15), 0); // [cite: 135]
            break;
        case Mode::CANNY:
            cv::cvtColor(input, output, cv::COLOR_BGR2GRAY);
            cv::Canny(output, output, 50, 150); // [cite: 136]
            cv::cvtColor(output, output, cv::COLOR_GRAY2BGR); // Повертаємо 3 канали для малювання кольорових фігур
            break;
        case Mode::NORMAL:
        default:
            output = input.clone();
            break;
    }

    // 2. Зміна яскравості через Trackbar [cite: 149]
    int beta = brightness - 50; // Діапазон від -50 до 50
    output.convertTo(output, -1, 1.0, beta);

    // 3. Малювання прямокутника мишкою [cite: 144]
    if (drawingBox.width != 0 && drawingBox.height != 0) {
        cv::rectangle(output, drawingBox, cv::Scalar(0, 255, 0), 2);
    }

    // 4. Текст на екрані (характеристики) [cite: 146]
    cv::putText(output, "Mode: " + std::to_string(static_cast<int>(mode)) + " (N/I/B/C)", 
                cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(0, 0, 255), 2);
    
    return output;
}