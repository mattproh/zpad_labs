#include "FrameProcessor.hpp"

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

cv::Mat FrameProcessor::process(const cv::Mat& input, Mode mode, const std::vector<cv::Rect>& faces) {
    cv::Mat output;
    
    switch (mode) {
        case Mode::INVERT: cv::bitwise_not(input, output); break;
        case Mode::BLUR: cv::GaussianBlur(input, output, cv::Size(15, 15), 0); break;
        case Mode::CANNY:
            cv::cvtColor(input, output, cv::COLOR_BGR2GRAY);
            cv::Canny(output, output, 50, 150);
            cv::cvtColor(output, output, cv::COLOR_GRAY2BGR);
            break;
        case Mode::NORMAL:
        case Mode::FACE_DETECT:
        default: output = input.clone(); break;
    }

    int beta = brightness - 50;
    output.convertTo(output, -1, 1.0, beta);

    if (drawingBox.width != 0 && drawingBox.height != 0) {
        cv::rectangle(output, drawingBox, cv::Scalar(0, 255, 0), 2);
    }

    // Draw bounding boxes around detected faces
    if (mode == Mode::FACE_DETECT) {
        for (const auto& face : faces) {
            cv::rectangle(output, face, cv::Scalar(255, 0, 0), 3); // Draw a blue rectangle around the face
        }
    }

    // FPS calculation and rendering
    int64 currentTick = cv::getTickCount();
    double fps = cv::getTickFrequency() / (currentTick - lastTick);
    lastTick = currentTick;

    cv::putText(output, "Mode: " + std::to_string(static_cast<int>(mode)), cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(0, 0, 255), 2);
    cv::putText(output, "FPS: " + std::to_string((int)fps), cv::Point(10, 60), cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(0, 255, 0), 2);
    
    return output;
}