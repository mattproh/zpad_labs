#include <iostream>
#include "CameraProvider.hpp"
#include "Display.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "FaceDetector.hpp"

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) return -1;

    Display display("Lab 7 - CV & Multithreading");
    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;
    FaceDetector faceDetector;
    
    Mode currentMode = Mode::NORMAL;

    cv::createTrackbar("Brightness", display.getWindowName(), &FrameProcessor::brightness, 100);
    cv::setMouseCallback(display.getWindowName(), FrameProcessor::onMouse);

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        std::vector<cv::Rect> faces;

        if (currentMode == Mode::FACE_DETECT) {
            faceDetector.updateFrame(frame);
            faces = faceDetector.getFaces();
        }

        cv::Mat processedFrame = frameProcessor.process(frame, currentMode, faces);
        display.show(processedFrame); // Display (imshow)

        int key = cv::waitKey(30) & 0xFF;
        if (key == 27 || key == 'q') break;

        currentMode = keyProcessor.processKey(key, currentMode);
    }

    return 0;
}