# 🔄 Unit Converter

A comprehensive web-based unit conversion application built with Python Flask. Convert between different units of length, weight, and temperature with an intuitive and beautiful user interface.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **📏 Length Converter**: Convert between 8 different length units
- **⚖️ Weight Converter**: Convert between 5 different weight units
- **🌡️ Temperature Converter**: Convert between Celsius, Fahrenheit, and Kelvin
- **🎨 Modern UI**: Beautiful gradient design with smooth animations
- **📱 Responsive**: Works seamlessly on desktop and mobile devices
- **✅ Input Validation**: Comprehensive error handling and user feedback
- **🔄 Form Persistence**: Values are preserved after conversion

## 🚀 Demo

### Supported Units

#### Length
- Millimeter (mm)
- Centimeter (cm)
- Meter (m)
- Kilometer (km)
- Inch (in)
- Foot (ft)
- Yard (yd)
- Mile (mi)

#### Weight
- Milligram (mg)
- Gram (g)
- Kilogram (kg)
- Ounce (oz)
- Pound (lb)

#### Temperature
- Celsius (°C)
- Fahrenheit (°F)
- Kelvin (K)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/unit-converter.git
cd unit-converter
```

### 2. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

Open your web browser and navigate to the URL to use the converter.

## 📁 Project Structure

```
unit-converter/
│
├── app.py                      # Main Flask application
├── templates/                  # HTML templates
│   ├── index.html             # Home page
│   ├── length.html            # Length converter page
│   ├── weight.html            # Weight converter page
│   └── temperature.html       # Temperature converter page
├── test_app.py                # Pytest test suite
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 🧪 Testing

This project includes a comprehensive test suite with 81+ tests covering all functionality.

### Install Testing Dependencies

```bash
pip install pytest pytest-cov
```

### Run Tests

**Run all tests:**
```bash
pytest test_app.py -v
```

**Run with coverage report:**
```bash
pytest test_app.py -v --cov=app --cov-report=html
```

**Run specific test class:**
```bash
pytest test_app.py::TestLengthConversion -v
```

### Test Coverage

- ✅ Conversion logic (length, weight, temperature)
- ✅ Flask routes and HTTP methods
- ✅ Form validation and error handling
- ✅ Edge cases and boundary conditions
- ✅ Invalid inputs and error messages
- ✅ Floating-point precision
- ✅ Conversion reversibility

## 💡 Usage Examples

### Length Conversion
```
Input: 10 meters
Convert to: feet
Result: 32.8084 feet
```

### Weight Conversion
```
Input: 1 kilogram
Convert to: pounds
Result: 2.20462 pounds
```

### Temperature Conversion
```
Input: 100 Celsius
Convert to: Fahrenheit
Result: 212 Fahrenheit
```

## 🔧 Configuration

### Debug Mode

The application runs in debug mode by default for development. To disable debug mode for production:

```python
# In app.py
if __name__ == '__main__':
    app.run(debug=False)
```

### Port Configuration

To change the default port (5000):

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

### Host Configuration

To make the app accessible from other devices on your network:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

## 🎨 Customization

### Changing Colors

Edit the CSS gradient colors in the HTML template files:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adding New Units

1. **For Length**: Update `LENGTH_TO_METERS` dictionary in `app.py`
2. **For Weight**: Update `WEIGHT_TO_GRAMS` dictionary in `app.py`
3. **For Temperature**: Update the `convert_temperature()` function

Example - Adding nautical miles:
```python
LENGTH_TO_METERS = {
    # ... existing units
    'nautical_mile': 1852,
}
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```
OSError: [Errno 48] Address already in use
```
Solution: Change the port or kill the process using port 5000

**Templates not found:**
```
jinja2.exceptions.TemplateNotFound
```
Solution: Ensure `templates/` folder exists in the same directory as `app.py`

**Module not found:**
```
ModuleNotFoundError: No module named 'flask'
```
Solution: Install Flask using `pip install flask`

## 🚀 Deployment

### Deploy to Production

For production deployment, use a production-grade WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn app:app
```

### Deploy to Cloud Platforms

#### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Create `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### PythonAnywhere
1. Upload your files
2. Configure web app with Flask
3. Set source code directory
4. Reload the web app

## 📝 API Documentation

### Conversion Functions

#### `convert_length(value, from_unit, to_unit)`
Converts length between different units.

**Parameters:**
- `value` (float): The numeric value to convert
- `from_unit` (str): Source unit (e.g., 'meter', 'foot')
- `to_unit` (str): Target unit (e.g., 'kilometer', 'mile')

**Returns:**
- `float`: Converted value rounded to 6 decimal places
- `None`: If invalid units provided

#### `convert_weight(value, from_unit, to_unit)`
Converts weight between different units.

**Parameters:**
- `value` (float): The numeric value to convert
- `from_unit` (str): Source unit (e.g., 'kilogram', 'pound')
- `to_unit` (str): Target unit (e.g., 'gram', 'ounce')

**Returns:**
- `float`: Converted value rounded to 6 decimal places
- `None`: If invalid units provided

#### `convert_temperature(value, from_unit, to_unit)`
Converts temperature between Celsius, Fahrenheit, and Kelvin.

**Parameters:**
- `value` (float): The temperature value to convert
- `from_unit` (str): Source unit ('Celsius', 'Fahrenheit', 'Kelvin')
- `to_unit` (str): Target unit ('Celsius', 'Fahrenheit', 'Kelvin')

**Returns:**
- `float`: Converted temperature rounded to 2 decimal places
- `None`: If invalid units provided

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass (`pytest test_app.py`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Add comments for complex logic
- Update documentation for new features
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Flask framework for the backend
- Font Awesome for icons (if used)
- The Python community for excellent documentation

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Unit Conversion Formulas](https://en.wikipedia.org/wiki/Conversion_of_units)

## 🔮 Future Enhancements

- [ ] Add more unit categories (area, volume, speed)
- [ ] Implement unit conversion history
- [ ] Add dark mode toggle
- [ ] Create REST API endpoints
- [ ] Add unit search/filter functionality
- [ ] Implement batch conversions
- [ ] Add conversion formulas display
- [ ] Create mobile app version
- [ ] Add localization support
- [ ] Implement user preferences storage

## 📊 Version History

### v1.0.0 (2025-10-21)
- Initial release
- Length, weight, and temperature converters
- Comprehensive test suite
- Responsive web interface

---

**Made with ❤️ using Python and Flask**

If you find this project helpful, please give it a ⭐!