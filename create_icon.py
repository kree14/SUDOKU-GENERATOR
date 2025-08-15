from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple app icon for the Sudoku solver"""
    # Create a 256x256 image with white background
    size = 256
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw Sudoku grid
    grid_size = 200
    start_x = (size - grid_size) // 2
    start_y = (size - grid_size) // 2
    cell_size = grid_size // 9
    
    # Draw grid lines
    for i in range(10):
        x = start_x + i * cell_size
        y = start_y + i * cell_size
        
        # Thick lines for 3x3 boxes
        width = 3 if i % 3 == 0 else 1
        
        # Vertical lines
        draw.line([(x, start_y), (x, start_y + grid_size)], fill='black', width=width)
        # Horizontal lines
        draw.line([(start_x, y), (start_x + grid_size, y)], fill='black', width=width)
    
    # Add some sample numbers
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Sample numbers to make it look like a Sudoku
    numbers = [
        (1, 0, '5'), (2, 1, '3'), (0, 2, '7'),
        (4, 3, '6'), (6, 4, '1'), (8, 5, '4'),
        (3, 6, '8'), (7, 7, '2'), (5, 8, '9')
    ]
    
    for row, col, num in numbers:
        x = start_x + col * cell_size + cell_size // 2
        y = start_y + row * cell_size + cell_size // 2
        
        # Get text size for centering
        bbox = draw.textbbox((0, 0), num, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text((x - text_width // 2, y - text_height // 2), num, 
                 fill='blue', font=font)
    
    # Add AI indicator
    draw.ellipse([size-60, 10, size-10, 60], fill='red', outline='darkred', width=2)
    try:
        ai_font = ImageFont.truetype("arial.ttf", 14)
    except:
        ai_font = ImageFont.load_default()
    
    draw.text((size-45, 25), "AI", fill='white', font=ai_font)
    
    # Save as PNG
    img.save('icon.png')
    
    # Create ICO file for Windows
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print("App icon created successfully!")

if __name__ == "__main__":
    create_icon()
