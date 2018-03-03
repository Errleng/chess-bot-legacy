cmake_minimum_required(VERSION 2.8.12)

project(ChessBot)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD 11)

find_package(Qt5Core)
find_package(OpenCV REQUIRED)

add_executable(${PROJECT_NAME} "main.cpp")

target_link_libraries(${PROJECT_NAME} Qt5::Core)
target_link_libraries(ChessBot ${OpenCV_LIBS})
