#include "KeyProcessor.hpp"

Mode KeyProcessor::processKey(int key, Mode currentMode) {
    switch (key) {
        case 'n': case 'N': return Mode::NORMAL;
        case 'i': case 'I': return Mode::INVERT; // Інверсія кольорів [cite: 134]
        case 'b': case 'B': return Mode::BLUR;   // Gaussian blur [cite: 135]
        case 'c': case 'C': return Mode::CANNY;  // Фільтр Canny [cite: 136]
        default: return currentMode;
    }
}