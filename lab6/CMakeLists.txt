cmake_minimum_required(VERSION 3.10)
project(Lab6_OpenCV)

set(CMAKE_CXX_STANDARD 17)

# Шукаємо OpenCV
find_package(OpenCV REQUIRED)

# Додаємо папку include для заголовних файлів
include_directories(include ${OpenCV_INCLUDE_DIRS})

# Збираємо всі .cpp файли з папки src
file(GLOB SOURCES "src/*.cpp")

# Створюємо виконуваний файл
add_executable(${PROJECT_NAME} ${SOURCES})

# Лінкуємо бібліотеки OpenCV
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})