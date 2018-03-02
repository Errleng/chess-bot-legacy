cmake_minimum_required(VERSION 3.9)
project(VersionCPP)

set(CMAKE_CXX_STANDARD 11)
find_package(OpenCV REQUIRED)
add_executable(VersionCPP main.cpp)
target_link_libraries(VersionCPP ${OpenCV_LIBS})