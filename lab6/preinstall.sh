#!/bin/bash
echo "Встановлюємо необхідні залежності..."
sudo apt update
sudo apt install libopencv-dev cmake gcc g++ -y
echo "Залежності успішно встановлено!"