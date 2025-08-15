# AI-Powered Sudoku Solver with GUI

A comprehensive Python application that combines artificial intelligence with a modern GUI to solve Sudoku puzzles. Features include puzzle generation, animated solving visualization, OCR integration, and export capabilities.

## 🚀 Features

### Core Functionality
- **Sudoku Puzzle Generator**: Creates valid, solvable puzzles with three difficulty levels (Easy, Medium, Hard)
- **AI Solver**: Implements backtracking algorithm with efficient recursive logic
- **Animated Visualization**: Step-by-step solving animation with color-coded cell highlighting
- **Custom Puzzle Input**: Manual puzzle entry through the GUI interface

### Advanced Features
- **OCR Integration**: Extract Sudoku puzzles from images or webcam using OpenCV and Tesseract
- **Export Options**: Save puzzles and solutions as TXT or CSV files
- **Theme Support**: Toggle between light and dark modes
- **Real-time Validation**: Check solution correctness with error highlighting
- **Performance Statistics**: Display solving time and step count

### GUI Features
- Modern PyQt5 interface with responsive design
- Color-coded animations (green for correct entries, red for backtracked cells)
- Adjustable animation speed
- Comprehensive control panel with grouped functionality
- Status updates and progress indicators

## 📋 Requirements

- Python 3.7+
- PyQt5
- OpenCV
- Tesseract OCR
- NumPy
- Pillow

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   cd AI-Powered-Sudoku-Solver
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (for OCR functionality)
   - Windows: Download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. **Create app icon**
   ```bash
   python create_icon.py
   ```

## 🎮 Usage

### Running the Application
```bash
python main_gui.py
```

### Main Features

#### Puzzle Generation
1. Select difficulty level (Easy, Medium, Hard)
2. Click "Generate New Puzzle" to create a new challenge
3. Given numbers appear in blue with bold styling

#### Solving Puzzles
- **Animated Solving**: Watch the AI solve step-by-step with visual feedback
- **Instant Solving**: Get immediate solution without animation
- **Speed Control**: Adjust animation speed with the slider
- **Stop Function**: Halt solving process at any time

#### OCR Integration
- **Webcam Capture**: Use your camera to capture Sudoku puzzles from books or screens
- **Image Upload**: Load puzzle images from your computer
- **Automatic Detection**: AI detects grid boundaries and extracts numbers

#### Puzzle Management
- **Clear Puzzle**: Start with empty grid for custom input
- **Reset**: Return to original puzzle state
- **Validate**: Check if current solution is correct
- **Export**: Save puzzles as TXT or CSV files

### Keyboard Shortcuts
- Numbers 1-9: Enter digits in selected cells
- Delete/Backspace: Clear cell content
- Arrow keys: Navigate between cells
- Tab: Move to next cell

## 🏗️ Project Structure

```
AI-Powered-Sudoku-Solver/
├── main_gui.py           # Main application with PyQt5 GUI
├── sudoku_generator.py   # Puzzle generation logic
├── sudoku_solver.py      # Backtracking solver with animation
├── ocr_processor.py      # OpenCV + Tesseract OCR integration
├── create_icon.py        # App icon generation script
├── compile.bat           # Windows compilation script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── icon.png             # Application icon (generated)
└── icon.ico             # Windows icon file (generated)
```

## 🔧 Compilation to Executable

### Windows
Run the provided batch script:
```bash
compile.bat
```

### Manual Compilation
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --icon=icon.ico --name="AI-Sudoku-Solver" main_gui.py
```

The executable will be created in the `dist/` folder.

## 🎨 Customization

### Themes
- Toggle between light and dark modes using the theme button
- Modify color schemes in the `apply_theme()` method

### Animation Speed
- Adjust solving animation speed with the slider (1-10 scale)
- Modify delay calculations in `SolverThread` class

### OCR Settings
- Configure Tesseract path in `ocr_processor.py` if needed
- Adjust image preprocessing parameters for better recognition

## 🐛 Troubleshooting

### Common Issues

1. **Tesseract not found**
   - Ensure Tesseract is installed and in system PATH
   - Manually set path in `ocr_processor.py`: 
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

2. **Webcam not working**
   - Check camera permissions
   - Ensure no other applications are using the camera
   - Try different camera indices in `cv2.VideoCapture(0)`

3. **PyQt5 installation issues**
   - Try: `pip install PyQt5 --force-reinstall`
   - On Linux: `sudo apt-get install python3-pyqt5`

4. **Slow puzzle generation**
   - Normal for Hard difficulty due to unique solution validation
   - Consider reducing validation strictness for faster generation

## 🔬 Algorithm Details

### Backtracking Solver
- Implements recursive backtracking with constraint propagation
- Validates placements against Sudoku rules (row, column, 3x3 box)
- Tracks solving steps for animation and statistics

### Puzzle Generation
- Starts with complete valid solution
- Removes numbers while maintaining unique solution
- Difficulty based on number of removed cells:
  - Easy: 40-45 removed cells
  - Medium: 46-52 removed cells  
  - Hard: 53-58 removed cells

### OCR Processing
- Preprocesses images with Gaussian blur and adaptive thresholding
- Detects grid using contour analysis
- Applies perspective transformation for grid straightening
- Extracts individual cells and recognizes digits with Tesseract

## 📊 Performance

- **Generation Time**: 1-5 seconds depending on difficulty
- **Solving Time**: Usually under 1 second for most puzzles
- **OCR Accuracy**: ~85-95% depending on image quality
- **Memory Usage**: ~50-100MB during operation

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **PyQt5**: For the excellent GUI framework
- **OpenCV**: For computer vision capabilities
- **Tesseract**: For OCR functionality
- **NumPy**: For efficient array operations

## 📞 Support

If you encounter issues or have questions:
1. Check the troubleshooting section
2. Review the code comments for implementation details
3. Create an issue with detailed error information

---

**Enjoy solving Sudoku puzzles with AI! 🧩🤖**
