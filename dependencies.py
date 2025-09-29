#!/usr/bin/env python3
"""
Dependencies setup script for BEMsim3D project
Downloads and configures FFTW for Windows
"""

import os
import sys
import urllib.request
import zipfile
import subprocess
from pathlib import Path

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename} successfully")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract ZIP file to specified directory"""
    print(f"Extracting {zip_path} to {extract_to}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted successfully")
        return True
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")
        return False

def create_lib_files(fftw_dir):
    """Create .lib files for Visual Studio linking"""
    print("Creating .lib files for Visual Studio...")
    
    lib_files = [
        "libfftw3-3.def",
        "libfftw3f-3.def", 
        "libfftw3l-3.def"
    ]
    
    # Try to create .lib files directly without checking if lib.exe exists
    success_count = 0
    for def_file in lib_files:
        def_path = fftw_dir / def_file
        if def_path.exists():
            try:
                cmd = ["lib", f"/def:{def_file}"]
                result = subprocess.run(cmd, cwd=fftw_dir, shell=True, 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Created .lib for {def_file}")
                    success_count += 1
                else:
                    print(f"Failed to create .lib for {def_file}: {result.stderr}")
            except Exception as e:
                print(f"Error creating .lib for {def_file}: {e}")
        else:
            print(f"Definition file not found: {def_file}")
    
    if success_count > 0:
        print(f"Successfully created {success_count} .lib files")
    else:
        print("No .lib files were created. This is normal if not using Visual Studio.")
        print("The DLL files can still be used directly by most compilers.")

def setup_fftw():
    """Main function to set up FFTW"""
    project_root = Path(__file__).parent
    deps_dir = project_root / "dependencies"
    fftw_dir = deps_dir / "fftw"
    
    # Create directories
    deps_dir.mkdir(exist_ok=True)
    fftw_dir.mkdir(exist_ok=True)
    
    # Download FFTW 64-bit DLLs
    fftw_url = "https://fftw.org/pub/fftw/fftw-3.3.5-dll64.zip"
    fftw_zip = deps_dir / "fftw-3.3.5-dll64.zip"
    
    if not fftw_zip.exists():
        if not download_file(fftw_url, str(fftw_zip)):
            return False
    else:
        print(f"FFTW zip already exists: {fftw_zip}")
    
    # Extract FFTW
    if not extract_zip(str(fftw_zip), str(fftw_dir)):
        return False
    
    # Create .lib files for Visual Studio
    create_lib_files(fftw_dir)
    
    # Create environment setup
    create_env_setup(fftw_dir, deps_dir)
    
    print(f"\nFFTW setup complete!")
    print(f"FFTW installed to: {fftw_dir}")
    print(f"Include path: {fftw_dir}")
    print(f"Library path: {fftw_dir}")
    
    return True

def create_env_setup(fftw_dir, deps_dir):
    """Create environment setup files"""
    
    # Create CMake config file
    cmake_config = deps_dir / "FFTWConfig.cmake"
    with open(cmake_config, 'w') as f:
        f.write(f"""# FFTW Configuration for BEMsim3D
set(FFTW_ROOT "{fftw_dir.as_posix()}")
set(FFTW_INCLUDE_DIRS "${{FFTW_ROOT}}")
set(FFTW_LIBRARY_DIRS "${{FFTW_ROOT}}")

# Find libraries - try multiple naming conventions
find_library(FFTW3F_LIBRARY 
    NAMES fftw3f-3 libfftw3f-3 fftw3f libfftw3f
    PATHS "${{FFTW_ROOT}}"
    NO_DEFAULT_PATH
)

find_library(FFTW3F_THREADS_LIBRARY
    NAMES fftw3f_threads-3 libfftw3f_threads-3 fftw3f_threads libfftw3f_threads
    PATHS "${{FFTW_ROOT}}"
    NO_DEFAULT_PATH
)

# Debug output
message(STATUS "FFTW_ROOT: ${{FFTW_ROOT}}")
message(STATUS "FFTW3F_LIBRARY: ${{FFTW3F_LIBRARY}}")
message(STATUS "FFTW3F_THREADS_LIBRARY: ${{FFTW3F_THREADS_LIBRARY}}")

# Set libraries list
if(FFTW3F_LIBRARY)
    set(FFTW_LIBRARIES "${{FFTW3F_LIBRARY}}")
    if(FFTW3F_THREADS_LIBRARY)
        list(APPEND FFTW_LIBRARIES "${{FFTW3F_THREADS_LIBRARY}}")
    endif()
endif()

# Check if we found the main library at least
if(FFTW3F_LIBRARY)
    set(FFTW_FOUND TRUE)
    message(STATUS "Found FFTW: ${{FFTW_ROOT}}")
    message(STATUS "FFTW Libraries: ${{FFTW_LIBRARIES}}")
else()
    set(FFTW_FOUND FALSE)
    message(WARNING "FFTW not found in ${{FFTW_ROOT}}")
    # List available files for debugging
    file(GLOB FFTW_FILES "${{FFTW_ROOT}}/*")
    message(STATUS "Available files in FFTW directory: ${{FFTW_FILES}}")
endif()
""")
    
    # Create batch file for Windows
    batch_file = deps_dir / "setup_env.bat"
    with open(batch_file, 'w') as f:
        f.write(f"""@echo off
REM Environment setup for BEMsim3D dependencies
set FFTW_ROOT={fftw_dir}
set PATH=%FFTW_ROOT%;%PATH%
echo FFTW environment configured
echo FFTW_ROOT=%FFTW_ROOT%
""")

if __name__ == "__main__":
    if setup_fftw():
        print("Dependencies setup completed successfully!")
        sys.exit(0)
    else:
        print("Dependencies setup failed!")
        sys.exit(1)