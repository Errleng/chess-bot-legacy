# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.11

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = D:\Applications\CMake\bin\cmake.exe

# The command to remove a file.
RM = D:\Applications\CMake\bin\cmake.exe -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build

# Include any dependencies generated for this target.
include CMakeFiles/ChessBot.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/ChessBot.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ChessBot.dir/flags.make

CMakeFiles/ChessBot.dir/main.cpp.obj: CMakeFiles/ChessBot.dir/flags.make
CMakeFiles/ChessBot.dir/main.cpp.obj: CMakeFiles/ChessBot.dir/includes_CXX.rsp
CMakeFiles/ChessBot.dir/main.cpp.obj: D:/Documents/SourceTree/ChessBot/VersionCpp/ChessBot/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/ChessBot.dir/main.cpp.obj"
	D:\Applications\MinGW-64\mingw64\bin\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\ChessBot.dir\main.cpp.obj -c D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot\main.cpp

CMakeFiles/ChessBot.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ChessBot.dir/main.cpp.i"
	D:\Applications\MinGW-64\mingw64\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot\main.cpp > CMakeFiles\ChessBot.dir\main.cpp.i

CMakeFiles/ChessBot.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ChessBot.dir/main.cpp.s"
	D:\Applications\MinGW-64\mingw64\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot\main.cpp -o CMakeFiles\ChessBot.dir\main.cpp.s

CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.obj: CMakeFiles/ChessBot.dir/flags.make
CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.obj: CMakeFiles/ChessBot.dir/includes_CXX.rsp
CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.obj: ChessBot_autogen/mocs_compilation.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.obj"
	D:\Applications\MinGW-64\mingw64\bin\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\ChessBot.dir\ChessBot_autogen\mocs_compilation.cpp.obj -c D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\ChessBot_autogen\mocs_compilation.cpp

CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.i"
	D:\Applications\MinGW-64\mingw64\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\ChessBot_autogen\mocs_compilation.cpp > CMakeFiles\ChessBot.dir\ChessBot_autogen\mocs_compilation.cpp.i

CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.s"
	D:\Applications\MinGW-64\mingw64\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\ChessBot_autogen\mocs_compilation.cpp -o CMakeFiles\ChessBot.dir\ChessBot_autogen\mocs_compilation.cpp.s

# Object files for target ChessBot
ChessBot_OBJECTS = \
"CMakeFiles/ChessBot.dir/main.cpp.obj" \
"CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.obj"

# External object files for target ChessBot
ChessBot_EXTERNAL_OBJECTS =

ChessBot.exe: CMakeFiles/ChessBot.dir/main.cpp.obj
ChessBot.exe: CMakeFiles/ChessBot.dir/ChessBot_autogen/mocs_compilation.cpp.obj
ChessBot.exe: CMakeFiles/ChessBot.dir/build.make
ChessBot.exe: D:/Applications/QT/5.10.1/msvc2017_64/lib/Qt5Core.lib
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_dnn341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_ml341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_objdetect341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_shape341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_stitching341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_superres341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_videostab341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_calib3d341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_features2d341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_flann341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_highgui341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_photo341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_video341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_videoio341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_imgcodecs341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_imgproc341.dll.a
ChessBot.exe: D:/Documents/Code/Dependencies/opencv-3.4.1-build/lib/libopencv_core341.dll.a
ChessBot.exe: CMakeFiles/ChessBot.dir/linklibs.rsp
ChessBot.exe: CMakeFiles/ChessBot.dir/objects1.rsp
ChessBot.exe: CMakeFiles/ChessBot.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable ChessBot.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\ChessBot.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ChessBot.dir/build: ChessBot.exe

.PHONY : CMakeFiles/ChessBot.dir/build

CMakeFiles/ChessBot.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\ChessBot.dir\cmake_clean.cmake
.PHONY : CMakeFiles/ChessBot.dir/clean

CMakeFiles/ChessBot.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build D:\Documents\SourceTree\ChessBot\VersionCpp\ChessBot-build\CMakeFiles\ChessBot.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ChessBot.dir/depend
