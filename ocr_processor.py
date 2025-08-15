import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

class OCRProcessor:
    def __init__(self):
        # Configure Tesseract path (may need adjustment based on installation)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Invert if background is dark
        if np.mean(thresh) < 127:
            thresh = cv2.bitwise_not(thresh)
        
        return thresh
    
    def detect_grid(self, image):
        """Detect Sudoku grid in the image"""
        processed = self.preprocess_image(image)
        
        # Find contours
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest rectangular contour (likely the Sudoku grid)
        largest_contour = None
        max_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4 corners)
                if len(approx) == 4 and area > 1000:
                    largest_contour = approx
                    max_area = area
        
        return largest_contour
    
    def extract_grid_region(self, image, contour):
        """Extract and straighten the grid region"""
        if contour is None:
            return None
        
        # Get the four corners
        points = contour.reshape(4, 2)
        
        # Order points: top-left, top-right, bottom-right, bottom-left
        rect = np.zeros((4, 2), dtype=np.float32)
        
        s = points.sum(axis=1)
        rect[0] = points[np.argmin(s)]  # top-left
        rect[2] = points[np.argmax(s)]  # bottom-right
        
        diff = np.diff(points, axis=1)
        rect[1] = points[np.argmin(diff)]  # top-right
        rect[3] = points[np.argmax(diff)]  # bottom-left
        
        # Define destination points for perspective transform
        width = height = 450  # Square grid
        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype=np.float32)
        
        # Apply perspective transform
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, matrix, (width, height))
        
        return warped
    
    def extract_cells(self, grid_image):
        """Extract individual cells from the grid"""
        if grid_image is None:
            return None
        
        height, width = grid_image.shape[:2]
        cell_height = height // 9
        cell_width = width // 9
        
        cells = []
        for i in range(9):
            row = []
            for j in range(9):
                y1 = i * cell_height
                y2 = (i + 1) * cell_height
                x1 = j * cell_width
                x2 = (j + 1) * cell_width
                
                cell = grid_image[y1:y2, x1:x2]
                row.append(cell)
            cells.append(row)
        
        return cells
    
    def recognize_digit(self, cell_image):
        """Recognize digit in a cell using OCR"""
        # Preprocess cell
        gray = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY) if len(cell_image.shape) == 3 else cell_image
        
        # Resize cell for better OCR
        resized = cv2.resize(gray, (50, 50))
        
        # Apply threshold
        _, thresh = cv2.threshold(resized, 127, 255, cv2.THRESH_BINARY)
        
        # Add padding
        padded = cv2.copyMakeBorder(thresh, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)
        
        try:
            # Configure Tesseract for single digit recognition
            config = '--psm 10 -c tessedit_char_whitelist=123456789'
            text = pytesseract.image_to_string(padded, config=config).strip()
            
            # Extract digit
            digits = re.findall(r'[1-9]', text)
            if digits:
                return int(digits[0])
            else:
                return 0
        except:
            return 0
    
    def process_image(self, image_path):
        """Process image and extract Sudoku puzzle"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return None, "Could not load image"
            
            # Detect grid
            contour = self.detect_grid(image)
            if contour is None:
                return None, "Could not detect Sudoku grid"
            
            # Extract grid region
            grid = self.extract_grid_region(image, contour)
            if grid is None:
                return None, "Could not extract grid region"
            
            # Extract cells
            cells = self.extract_cells(grid)
            if cells is None:
                return None, "Could not extract cells"
            
            # Recognize digits
            puzzle = []
            for i in range(9):
                row = []
                for j in range(9):
                    digit = self.recognize_digit(cells[i][j])
                    row.append(digit)
                puzzle.append(row)
            
            return puzzle, "Success"
            
        except Exception as e:
            return None, f"Error processing image: {str(e)}"
    
    def process_webcam_frame(self, frame):
        """Process a single webcam frame"""
        try:
            # Detect grid
            contour = self.detect_grid(frame)
            if contour is None:
                return None, frame
            
            # Draw detected contour on frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            
            # Extract and process grid
            grid = self.extract_grid_region(frame, contour)
            if grid is None:
                return None, frame
            
            # Extract cells and recognize digits
            cells = self.extract_cells(grid)
            puzzle = []
            for i in range(9):
                row = []
                for j in range(9):
                    digit = self.recognize_digit(cells[i][j])
                    row.append(digit)
                puzzle.append(row)
            
            return puzzle, frame
            
        except Exception as e:
            print(f"Webcam processing error: {e}")
            return None, frame
    
    def process_image_array(self, image_array):
        """Process image array (for webcam capture)"""
        try:
            # Detect grid
            contour = self.detect_grid(image_array)
            if contour is None:
                return None, "Could not detect Sudoku grid"
            
            # Extract grid region
            grid = self.extract_grid_region(image_array, contour)
            if grid is None:
                return None, "Could not extract grid region"
            
            # Extract cells
            cells = self.extract_cells(grid)
            if cells is None:
                return None, "Could not extract cells"
            
            # Recognize digits
            puzzle = []
            for i in range(9):
                row = []
                for j in range(9):
                    digit = self.recognize_digit(cells[i][j])
                    row.append(digit)
                puzzle.append(row)
            
            return puzzle, "Success"
            
        except Exception as e:
            return None, f"Error processing image: {str(e)}"
