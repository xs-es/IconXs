from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Generate an icon for the application"""
    try:
        # Create an icon in multiple sizes
        icon_sizes = [16, 24, 32, 48, 64, 128, 256]
        icons = []
        
        # Base icon is a 256x256 image
        base_size = 256
        icon = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        
        # Background - dark circle
        circle_radius = base_size // 2 - 4
        circle_center = (base_size // 2, base_size // 2)
        
        # Draw the background circle (dark blue gradient)
        for r in range(circle_radius, 0, -1):
            # Calculate color for this circle - gradient from dark to accent blue
            ratio = r / circle_radius
            red = int(0x12 * (1-ratio) + 0x00 * ratio)
            green = int(0x12 * (1-ratio) + 0x7B * ratio)
            blue = int(0x12 * (1-ratio) + 0xFF * ratio)
            
            draw.ellipse(
                [
                    circle_center[0] - r,
                    circle_center[1] - r,
                    circle_center[0] + r,
                    circle_center[1] + r
                ],
                fill=(red, green, blue, 255)
            )
        
        # Draw a gear icon in the center - create polygon points for a gear
        gear_radius_outer = base_size // 3
        gear_radius_inner = gear_radius_outer * 0.7
        gear_radius_hub = gear_radius_inner * 0.4
        num_teeth = 8
        
        # Create gear shape using polygons
        points = []
        for i in range(num_teeth * 2):
            angle = i * 3.14159 * 2 / (num_teeth * 2)
            radius = gear_radius_outer if i % 2 == 0 else gear_radius_inner
            x = circle_center[0] + int(radius * 1.0 * (angle))
            y = circle_center[1] + int(radius * 1.0 * (angle))
            points.append((x, y))
            
        # Draw the gear as a white shape
        draw.polygon(points, fill=(255, 255, 255, 220))
        
        # Draw the hub circle
        draw.ellipse(
            [
                circle_center[0] - gear_radius_hub,
                circle_center[1] - gear_radius_hub,
                circle_center[0] + gear_radius_hub,
                circle_center[1] + gear_radius_hub
            ],
            fill=(255, 255, 255, 255),
            outline=(200, 200, 200, 255)
        )
        
        # Resize for all required icon sizes
        for size in icon_sizes:
            resized_icon = icon.resize((size, size), Image.LANCZOS)
            icons.append(resized_icon)
            
        # Save as .ico file
        icon.save("icon.ico", format="ICO", sizes=[(s, s) for s in icon_sizes])
        print("Icon created successfully: icon.ico")
        return True
    
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

if __name__ == "__main__":
    create_app_icon() 