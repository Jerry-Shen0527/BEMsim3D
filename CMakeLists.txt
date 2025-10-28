cmake_minimum_required(VERSION 3.18)
project(BEMsim3D LANGUAGES CXX CUDA)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set CUDA architecture (adjust as needed)
set(CMAKE_CUDA_ARCHITECTURES 86)

# Find required packages
find_package(CUDAToolkit REQUIRED)

# Try to find FFTW using our custom config first
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/dependencies" ${CMAKE_MODULE_PATH})
include(FFTWConfig OPTIONAL)

# Add compile definitions for Thrust/CUB C++ dialect
add_compile_definitions(
    THRUST_IGNORE_DEPRECATED_CPP_DIALECT
    CUB_IGNORE_DEPRECATED_CPP_DIALECT
)

# Fallback to pkg-config if custom config not found
if(NOT FFTW_FOUND)
    find_package(PkgConfig QUIET)
    if(PkgConfig_FOUND)
        pkg_check_modules(FFTW fftw3f)
    endif()
endif()

# Include directories
include_directories(include)
include_directories(include/eigen)

# CUDA libraries are handled by CUDAToolkit

# Set optimization flags
if(WIN32)
    # For MSVC: remove conflicting flags
    string(REGEX REPLACE "/RTC1" "" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /W4")
else()
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()
set(CMAKE_CUDA_FLAGS "-O3 --expt-relaxed-constexpr")

# Source files for bem3d executable
set(BEM3D_CPP_SOURCES
    Estimate.cpp
    Grid.cpp
    Incidence.cpp
    MVProd.cpp
    MVProd0.cpp
    Scattering.cpp
    Singular.cpp
    Singular0.cpp
    Solver.cpp
)

set(BEM3D_CUDA_SOURCES
    Kernels.cu
    MVProd1.cu
    MVProd2.cu
    MVProd3.cu
    MVProd4.cu
    Singular12.cu
    Singular34.cu
)

# Create bem3d executable
add_executable(bem3d
    bem3d.cpp
    ${BEM3D_CPP_SOURCES}
    ${BEM3D_CUDA_SOURCES}
)


add_subdirectory(dependencies/cxxopts)

# Link libraries for bem3d
target_link_libraries(bem3d
    CUDA::cudart
    CUDA::cufft
    CUDA::cusparse
    cxxopts::cxxopts
)

# Link FFTW libraries if found
if(FFTW_FOUND AND FFTW_LIBRARIES)
    target_link_libraries(bem3d ${FFTW_LIBRARIES})
    message(STATUS "Linking FFTW libraries: ${FFTW_LIBRARIES}")
else()
    message(FATAL_ERROR "FFTW not found! Please run 'python dependencies.py' first to set up FFTW.")
endif()

# Set CUDA properties for bem3d
set_property(TARGET bem3d PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS ON)

# Create steerBasicDirs executable
add_executable(steerBasicDirs steerBasicDirs.cpp)
target_link_libraries(steerBasicDirs cxxopts::cxxopts)
if(WIN32)
    target_compile_options(steerBasicDirs PRIVATE /O2)
else()
    target_compile_options(steerBasicDirs PRIVATE -O3)
endif()

# Create steerBRDFs executable
add_executable(steerBRDFs steerBRDFs.cpp)
target_link_libraries(steerBRDFs cxxopts::cxxopts)
if(UNIX)
    target_link_libraries(steerBRDFs pthread)
endif()
if(WIN32)
    target_compile_options(steerBRDFs PRIVATE /O2)
else()
    target_compile_options(steerBRDFs PRIVATE -O3)
endif()

# Add custom target for all executables (equivalent to 'all' in Makefile)
add_custom_target(all_targets ALL DEPENDS bem3d steerBasicDirs steerBRDFs)