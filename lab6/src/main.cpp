#include <iostream>
#include "CameraProvider.hpp"
#include "Display.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"

int main() {
    CameraProvider camera(0); // [cite: 129]
    if (!camera.isOpened()) return -1;

    Display display("Lab 6 - OpenCV"); // 
    KeyProcessor keyProcessor; // [cite: 131]
    FrameProcessor frameProcessor; // [cite: 132]
    Mode currentMode = Mode::NORMAL;

    // Налаштування інтерактивних елементів
    cv::createTrackbar("Brightness", display.getWindowName(), &FrameProcessor::brightness, 100); // [cite: 149]
    cv::setMouseCallback(display.getWindowName(), FrameProcessor::onMouse); // [cite: 144]

    // Головний цикл [cite: 106]
    while (true) {
        cv::Mat frame = camera.getFrame(); // [cite: 107, 129]
        if (frame.empty()) break;

        cv::Mat processedFrame = frameProcessor.process(frame, currentMode); // [cite: 132]
        display.show(processedFrame); // [cite: 108, 150]

        int key = cv::waitKey(30) & 0xFF; // [cite: 131]
        if (key == 27 || key == 'q') { // Вихід по ESC або 'q'
            break;
        }

        currentMode = keyProcessor.processKey(key, currentMode); // [cite: 110, 131]
    }

    return 0;
}