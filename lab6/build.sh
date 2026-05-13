#!/bin/bash
echo "Починаємо білд проєкту..."
mkdir -p build
cd build
cmake ..
make
echo "Білд завершено!"