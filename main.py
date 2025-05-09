import os
import sys
from PIL import Image

def resize_image(input_path, output_folder, sizes, naming_pattern=None, start_number=1, 
                include_dimensions=True, output_format=None):
    """
    Resize an image to multiple dimensions and save each copy with custom naming and format.
    
    Args:
        input_path: Path to the input image
        output_folder: Folder to save resized images
        sizes: List of sizes (width/height in pixels)
        naming_pattern: Optional custom naming pattern
        start_number: Starting number for sequential numbering
        include_dimensions: Whether to include dimensions in filename
        output_format: Output format (e.g., 'PNG', 'JPEG', 'GIF', 'ICO', etc.)
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Get the filename without extension
        filename = os.path.splitext(os.path.basename(input_path))[0]
        
        # Get the file extension based on output format or use original
        if output_format:
            # Convert format to lowercase for extension
            ext = f".{output_format.lower()}"
            # Special case for JPG vs JPEG
            if ext == ".jpg":
                save_format = "JPEG"
            elif ext == ".jpeg":
                save_format = "JPEG"
                ext = ".jpg"  # Standardize to .jpg
            else:
                save_format = output_format.upper()
        else:
            # Use original extension and format
            ext = os.path.splitext(input_path)[1]
            save_format = None  # PIL will determine from extension
        
        # For ICO format, validate sizes (ICO has specific size requirements)
        valid_ico_sizes = [16, 24, 32, 48, 64, 128, 256]
        if save_format == "ICO":
            valid_sizes = []
            for size in sizes:
                if size in valid_ico_sizes:
                    valid_sizes.append(size)
                else:
                    print(f"Warning: Size {size}x{size} is not valid for ICO format. Skipping.")
            
            if not valid_sizes:
                print("Error: No valid sizes for ICO format. Please select from: 16, 24, 32, 48, 64, 128, 256")
                return False
                
            sizes = valid_sizes
        
        # Resize for each target dimension
        success_count = 0
        for i, size in enumerate(sizes):
            # Create a resized copy
            if save_format == "ICO" and img.mode != "RGBA" and img.mode != "RGB":
                # Convert to RGBA for ICO format if needed
                resized_img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
            else:
                resized_img = img.resize((size, size), Image.LANCZOS)
            
            # Generate output filename based on pattern
            if naming_pattern:
                # Replace placeholders
                current_number = start_number + i
                custom_name = naming_pattern.replace("{name}", filename)
                custom_name = custom_name.replace("{num}", str(current_number))
                
                if include_dimensions:
                    output_path = os.path.join(output_folder, f"{custom_name}_{size}x{size}{ext}")
                else:
                    output_path = os.path.join(output_folder, f"{custom_name}{ext}")
            else:
                # Use default naming scheme
                output_path = os.path.join(output_folder, f"{filename}_{size}x{size}{ext}")
            
            # Save the resized image with format settings
            if save_format == "JPEG":
                # JPEG doesn't support transparency, convert to RGB and use quality setting
                if resized_img.mode in ('RGBA', 'LA') or (resized_img.mode == 'P' and 'transparency' in resized_img.info):
                    resized_img = resized_img.convert('RGB')
                resized_img.save(output_path, format=save_format, quality=95)
            elif save_format == "PNG":
                resized_img.save(output_path, format=save_format, optimize=True)
            elif save_format == "ICO":
                resized_img.save(output_path, format=save_format, sizes=[(size, size)])
            else:
                # Use default settings for other formats
                resized_img.save(output_path, format=save_format)
                
            print(f"Created: {output_path}")
            success_count += 1
            
        print(f"Successfully created {success_count} resized images in {output_folder}")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

def main():
    # Define target sizes
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    # Check if image path is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path> [output_folder]")
        return
    
    # Get image path from command line
    input_path = sys.argv[1]
    
    # Get output folder or use default
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "resized_images"
    
    # Resize the image
    resize_image(input_path, output_folder, sizes)

if __name__ == "__main__":
    main()
