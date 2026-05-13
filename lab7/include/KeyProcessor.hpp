#pragma once

enum class Mode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    FACE_DETECT // New mode for Lab 7
};

class KeyProcessor {
public:
    Mode processKey(int key, Mode currentMode);
};