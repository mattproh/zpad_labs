#pragma once

enum class Mode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY
};

class KeyProcessor {
public:
    Mode processKey(int key, Mode currentMode);
};