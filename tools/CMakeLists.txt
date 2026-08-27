# ---------------------------------------------------------------------------------------------------------------------
#
# Copyright (C) Microsoft Corporation.  
# Copyright (C) 2025 IAMAI CONSULTING CORP
#
# MIT License. All rights reserved.
#
# Module Name:
#
#   CMakeLists.txt
#
# Abstract:
#
#   CMake build file.
#
# ---------------------------------------------------------------------------------------------------------------------

# lvmon is a Windows/Linux debug monitor; skip it on macOS.
if(APPLE)
    add_library(lvmon INTERFACE)
    target_include_directories(lvmon INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/lvmon/Lib/include)
else()
    add_subdirectory(lvmon)
endif()
