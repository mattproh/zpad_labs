#include "KeyProcessor.hpp"

Mode KeyProcessor::processKey(int key, Mode currentMode) {
    switch (key) {
        case 'n': case 'N': return Mode::NORMAL;
        case 'i': case 'I': return Mode::INVERT;
        case 'b': case 'B': return Mode::BLUR;
        case 'c': case 'C': return Mode::CANNY;
        case 'f': case 'F': return Mode::FACE_DETECT; // Enable face detection
        default: return currentMode;
    }
}