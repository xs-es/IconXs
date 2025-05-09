import os
import sys
import shutil
import subprocess
from icon import create_app_icon

def build_app():
    """Build the Image Dimension Converter application"""
    print("=" * 60)
    print("Building Image Dimension Converter")
    print("=" * 60)
    
    # Step 1: Check dependencies
    print("\n[1/5] Checking dependencies...")
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
    try:
        from PIL import Image
        print("✓ Pillow is installed")
    except ImportError:
        print("Installing Pillow (PIL)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    
    # Step 2: Create application icon
    print("\n[2/5] Creating application icon...")
    if create_app_icon():
        print("✓ Application icon created successfully")
    else:
        print("⚠ Could not create icon, will use default")
    
    # Step 3: Create executable with PyInstaller
    print("\n[3/5] Building executable...")
    
    # Check if dist and build directories exist and remove them
    if os.path.exists("dist"):
        print("Removing existing dist directory...")
        shutil.rmtree("dist")
    if os.path.exists("build"):
        print("Removing existing build directory...")
        shutil.rmtree("build")
        
    # Build the executable
    build_cmd = [
        "pyinstaller", 
        "--name=Image Dimension Converter",
        "--windowed",  # No console window
        "--onedir",    # Create a directory with the executable
        "--clean",     # Clean build files
        "--noconfirm"  # No confirmation
    ]
    
    # Add icon if it exists
    if os.path.exists("icon.ico"):
        build_cmd.append("--icon=icon.ico")
        
    # Add main script
    build_cmd.append("gui.py")
    
    # Run the build
    try:
        subprocess.check_call(build_cmd)
        print("✓ Executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠ Error building executable: {e}")
        return False
    
    # Step 4: Create output directory and copy files
    print("\n[4/5] Creating distribution package...")
    
    # Create output directory
    output_dir = "dist/Image Dimension Converter"
    if not os.path.exists(output_dir):
        print(f"Output directory not found: {output_dir}")
        return False
        
    # Copy README if it exists
    if os.path.exists("README.md"):
        shutil.copy("README.md", output_dir)
        print("✓ Copied README.md")
        
    # Step 5: Test the executable
    print("\n[5/5] Verifying executable...")
    exe_path = os.path.join(output_dir, "Image Dimension Converter.exe")
    if os.path.exists(exe_path):
        print(f"✓ Executable created: {exe_path}")
    else:
        print(f"⚠ Executable not found: {exe_path}")
        return False
    
    # Final success message
    print("\n" + "=" * 60)
    print("✓ Build completed successfully!")
    print(f"Executable location: {os.path.abspath(exe_path)}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    build_app() 