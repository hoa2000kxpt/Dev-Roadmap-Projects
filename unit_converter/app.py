from flask import Flask, render_template, request

app = Flask(__name__)

# Conversion factors to base units
LENGTH_TO_METERS = {
    'millimeter': 0.001,
    'centimeter': 0.01,
    'meter': 1,
    'kilometer': 1000,
    'inch': 0.0254,
    'foot': 0.3048,
    'yard': 0.9144,
    'mile': 1609.34
}

WEIGHT_TO_GRAMS = {
    'milligram': 0.001,
    'gram': 1,
    'kilogram': 1000,
    'ounce': 28.3495,
    'pound': 453.592
}

def convert_length(value, from_unit, to_unit):
    """Convert length between units"""
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        return None
    meters = value * LENGTH_TO_METERS[from_unit]
    result = meters / LENGTH_TO_METERS[to_unit]
    return round(result, 6)

def convert_weight(value, from_unit, to_unit):
    """Convert weight between units"""
    if from_unit not in WEIGHT_TO_GRAMS or to_unit not in WEIGHT_TO_GRAMS:
        return None
    grams = value * WEIGHT_TO_GRAMS[from_unit]
    result = grams / WEIGHT_TO_GRAMS[to_unit]
    return round(result, 6)

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between units"""
    # Convert to Celsius first
    if from_unit == 'Celsius':
        celsius = value
    elif from_unit == 'Fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'Kelvin':
        celsius = value - 273.15
    else:
        return None
    
    # Convert from Celsius to target unit
    if to_unit == 'Celsius':
        result = celsius
    elif to_unit == 'Fahrenheit':
        result = (celsius * 9/5) + 32
    elif to_unit == 'Kelvin':
        result = celsius + 273.15
    else:
        return None
    
    return round(result, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/length', methods=['GET', 'POST'])
def length():
    result = None
    error = None
    value = ''
    from_unit = 'meter'
    to_unit = 'foot'
    
    if request.method == 'POST':
        try:
            value = float(request.form.get('value', 0))
            from_unit = request.form.get('from_unit', 'meter')
            to_unit = request.form.get('to_unit', 'foot')
            
            if value < 0:
                error = "Please enter a positive value"
            else:
                result = convert_length(value, from_unit, to_unit)
                if result is None:
                    error = "Invalid unit selection"
        except ValueError:
            error = "Please enter a valid number"
    
    units = sorted(LENGTH_TO_METERS.keys())
    return render_template('length.html', units=units, result=result, error=error, 
                         value=value, from_unit=from_unit, to_unit=to_unit)

@app.route('/weight', methods=['GET', 'POST'])
def weight():
    result = None
    error = None
    value = ''
    from_unit = 'kilogram'
    to_unit = 'pound'
    
    if request.method == 'POST':
        try:
            value = float(request.form.get('value', 0))
            from_unit = request.form.get('from_unit', 'kilogram')
            to_unit = request.form.get('to_unit', 'pound')
            
            if value < 0:
                error = "Please enter a positive value"
            else:
                result = convert_weight(value, from_unit, to_unit)
                if result is None:
                    error = "Invalid unit selection"
        except ValueError:
            error = "Please enter a valid number"
    
    units = sorted(WEIGHT_TO_GRAMS.keys())
    return render_template('weight.html', units=units, result=result, error=error,
                         value=value, from_unit=from_unit, to_unit=to_unit)

@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    result = None
    error = None
    value = ''
    from_unit = 'Celsius'
    to_unit = 'Fahrenheit'
    
    if request.method == 'POST':
        try:
            value = float(request.form.get('value', 0))
            from_unit = request.form.get('from_unit', 'Celsius')
            to_unit = request.form.get('to_unit', 'Fahrenheit')
            
            result = convert_temperature(value, from_unit, to_unit)
            if result is None:
                error = "Invalid unit selection"
        except ValueError:
            error = "Please enter a valid number"
    
    units = ['Celsius', 'Fahrenheit', 'Kelvin']
    return render_template('temperature.html', units=units, result=result, error=error,
                         value=value, from_unit=from_unit, to_unit=to_unit)

if __name__ == '__main__':
    app.run(debug=True)