# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.9

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

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /cygdrive/c/Users/aisae/.CLion2017.3/system/cygwin_cmake/bin/cmake.exe

# The command to remove a file.
RM = /cygdrive/c/Users/aisae/.CLion2017.3/system/cygwin_cmake/bin/cmake.exe -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/Windows10.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/Windows10.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Windows10.dir/flags.make

CMakeFiles/Windows10.dir/main.cpp.o: CMakeFiles/Windows10.dir/flags.make
CMakeFiles/Windows10.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/Windows10.dir/main.cpp.o"
	/usr/bin/c++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/Windows10.dir/main.cpp.o -c /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/main.cpp

CMakeFiles/Windows10.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Windows10.dir/main.cpp.i"
	/usr/bin/c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/main.cpp > CMakeFiles/Windows10.dir/main.cpp.i

CMakeFiles/Windows10.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Windows10.dir/main.cpp.s"
	/usr/bin/c++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/main.cpp -o CMakeFiles/Windows10.dir/main.cpp.s

CMakeFiles/Windows10.dir/main.cpp.o.requires:

.PHONY : CMakeFiles/Windows10.dir/main.cpp.o.requires

CMakeFiles/Windows10.dir/main.cpp.o.provides: CMakeFiles/Windows10.dir/main.cpp.o.requires
	$(MAKE) -f CMakeFiles/Windows10.dir/build.make CMakeFiles/Windows10.dir/main.cpp.o.provides.build
.PHONY : CMakeFiles/Windows10.dir/main.cpp.o.provides

CMakeFiles/Windows10.dir/main.cpp.o.provides.build: CMakeFiles/Windows10.dir/main.cpp.o


# Object files for target Windows10
Windows10_OBJECTS = \
"CMakeFiles/Windows10.dir/main.cpp.o"

# External object files for target Windows10
Windows10_EXTERNAL_OBJECTS =

Windows10.exe: CMakeFiles/Windows10.dir/main.cpp.o
Windows10.exe: CMakeFiles/Windows10.dir/build.make
Windows10.exe: CMakeFiles/Windows10.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable Windows10.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Windows10.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/Windows10.dir/build: Windows10.exe

.PHONY : CMakeFiles/Windows10.dir/build

CMakeFiles/Windows10.dir/requires: CMakeFiles/Windows10.dir/main.cpp.o.requires

.PHONY : CMakeFiles/Windows10.dir/requires

CMakeFiles/Windows10.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/Windows10.dir/cmake_clean.cmake
.PHONY : CMakeFiles/Windows10.dir/clean

CMakeFiles/Windows10.dir/depend:
	cd /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10 /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10 /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug /cygdrive/c/Users/aisae/Documents/Sourcetree/ChessBot/VersionC++/Windows10/cmake-build-debug/CMakeFiles/Windows10.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/Windows10.dir/depend

