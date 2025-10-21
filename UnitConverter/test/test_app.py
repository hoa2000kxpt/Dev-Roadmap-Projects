
"""
Comprehensive test suite for Unit Converter application
Tests all conversion functions with edge cases, boundary conditions, and invalid inputs
"""

import pytest
import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import (
    app, 
    convert_length, 
    convert_weight, 
    convert_temperature,
    LENGTH_TO_METERS,
    WEIGHT_TO_GRAMS
)

# ============================================================================
# FIXTURES: Common test setup
# ============================================================================

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def length_units():
    """Return list of all valid length units"""
    return list(LENGTH_TO_METERS.keys())


@pytest.fixture
def weight_units():
    """Return list of all valid weight units"""
    return list(WEIGHT_TO_GRAMS.keys())


@pytest.fixture
def temperature_units():
    """Return list of all valid temperature units"""
    return ['Celsius', 'Fahrenheit', 'Kelvin']


# ============================================================================
# LENGTH CONVERSION TESTS
# ============================================================================

class TestLengthConversion:
    """Test suite for length conversion functionality"""
    
    # Basic conversion tests
    def test_meter_to_centimeter(self):
        """Test basic meter to centimeter conversion"""
        result = convert_length(1, 'meter', 'centimeter')
        assert result == 100
    
    def test_foot_to_inch(self):
        """Test basic foot to inch conversion"""
        result = convert_length(1, 'foot', 'inch')
        assert result == 12
    
    def test_kilometer_to_meter(self):
        """Test basic kilometer to meter conversion"""
        result = convert_length(1, 'kilometer', 'meter')
        assert result == 1000
    
    def test_mile_to_kilometer(self):
        """Test mile to kilometer conversion (common use case)"""
        result = convert_length(1, 'mile', 'kilometer')
        assert pytest.approx(result, rel=1e-5) == 1.60934
    
    # Same unit conversion
    def test_same_unit_conversion(self):
        """Test converting a unit to itself returns the same value"""
        result = convert_length(42, 'meter', 'meter')
        assert result == 42
    
    # Decimal and floating point tests
    def test_decimal_conversion(self):
        """Test conversion with decimal values"""
        result = convert_length(1.5, 'meter', 'centimeter')
        assert result == 150
    
    def test_small_decimal_conversion(self):
        """Test conversion with very small decimal values"""
        result = convert_length(0.001, 'kilometer', 'meter')
        assert result == 1
    
    # Zero and negative values
    def test_zero_value_conversion(self):
        """Test conversion with zero value"""
        result = convert_length(0, 'meter', 'kilometer')
        assert result == 0
    
    def test_negative_value_conversion(self):
        """Test conversion with negative value (mathematically valid)"""
        result = convert_length(-10, 'meter', 'centimeter')
        assert result == -1000
    
    # Large numbers
    def test_large_number_conversion(self):
        """Test conversion with very large numbers"""
        result = convert_length(1000000, 'meter', 'kilometer')
        assert result == 1000
    
    # Precision and rounding
    def test_conversion_precision(self):
        """Test that results are rounded to 6 decimal places"""
        result = convert_length(1, 'inch', 'meter')
        # Should be 0.0254, check it's rounded properly
        assert isinstance(result, float)
        assert len(str(result).split('.')[-1]) <= 6
    
    # Invalid unit tests
    def test_invalid_from_unit(self):
        """Test conversion with invalid 'from' unit"""
        result = convert_length(10, 'invalid_unit', 'meter')
        assert result is None
    
    def test_invalid_to_unit(self):
        """Test conversion with invalid 'to' unit"""
        result = convert_length(10, 'meter', 'invalid_unit')
        assert result is None
    
    def test_both_invalid_units(self):
        """Test conversion with both invalid units"""
        result = convert_length(10, 'invalid1', 'invalid2')
        assert result is None
    
    # Case sensitivity
    def test_case_sensitive_units(self):
        """Test that unit names are case sensitive"""
        result = convert_length(10, 'Meter', 'centimeter')
        assert result is None  # Should fail as 'Meter' is not valid
    
    # Complex conversion chains
    def test_millimeter_to_mile(self):
        """Test conversion between very different scales"""
        result = convert_length(1000000, 'millimeter', 'mile')
        assert pytest.approx(result, rel=1e-4) == 0.621371

# ============================================================================
# LENGTH CONVERSION TESTS
# ============================================================================

class TestLengthConversion:
    """Test suite for length conversion functionality"""
    
    # Basic conversion tests
    def test_meter_to_centimeter(self):
        """Test basic meter to centimeter conversion"""
        result = convert_length(1, 'meter', 'centimeter')
        assert result == 100
    
    def test_foot_to_inch(self):
        """Test basic foot to inch conversion"""
        result = convert_length(1, 'foot', 'inch')
        assert result == 12
    
    def test_kilometer_to_meter(self):
        """Test basic kilometer to meter conversion"""
        result = convert_length(1, 'kilometer', 'meter')
        assert result == 1000
    
    def test_mile_to_kilometer(self):
        """Test mile to kilometer conversion (common use case)"""
        result = convert_length(1, 'mile', 'kilometer')
        assert pytest.approx(result, rel=1e-5) == 1.60934
    
    # Same unit conversion
    def test_same_unit_conversion(self):
        """Test converting a unit to itself returns the same value"""
        result = convert_length(42, 'meter', 'meter')
        assert result == 42
    
    # Decimal and floating point tests
    def test_decimal_conversion(self):
        """Test conversion with decimal values"""
        result = convert_length(1.5, 'meter', 'centimeter')
        assert result == 150
    
    def test_small_decimal_conversion(self):
        """Test conversion with very small decimal values"""
        result = convert_length(0.001, 'kilometer', 'meter')
        assert result == 1
    
    # Zero and negative values
    def test_zero_value_conversion(self):
        """Test conversion with zero value"""
        result = convert_length(0, 'meter', 'kilometer')
        assert result == 0
    
    def test_negative_value_conversion(self):
        """Test conversion with negative value (mathematically valid)"""
        result = convert_length(-10, 'meter', 'centimeter')
        assert result == -1000
    
    # Large numbers
    def test_large_number_conversion(self):
        """Test conversion with very large numbers"""
        result = convert_length(1000000, 'meter', 'kilometer')
        assert result == 1000
    
    # Precision and rounding
    def test_conversion_precision(self):
        """Test that results are rounded to 6 decimal places"""
        result = convert_length(1, 'inch', 'meter')
        # Should be 0.0254, check it's rounded properly
        assert isinstance(result, float)
        assert len(str(result).split('.')[-1]) <= 6
    
    # Invalid unit tests
    def test_invalid_from_unit(self):
        """Test conversion with invalid 'from' unit"""
        result = convert_length(10, 'invalid_unit', 'meter')
        assert result is None
    
    def test_invalid_to_unit(self):
        """Test conversion with invalid 'to' unit"""
        result = convert_length(10, 'meter', 'invalid_unit')
        assert result is None
    
    def test_both_invalid_units(self):
        """Test conversion with both invalid units"""
        result = convert_length(10, 'invalid1', 'invalid2')
        assert result is None
    
    # Case sensitivity
    def test_case_sensitive_units(self):
        """Test that unit names are case sensitive"""
        result = convert_length(10, 'Meter', 'centimeter')
        assert result is None  # Should fail as 'Meter' is not valid
    
    # Complex conversion chains
    def test_millimeter_to_mile(self):
        """Test conversion between very different scales"""
        result = convert_length(1000000, 'millimeter', 'mile')
        assert pytest.approx(result, rel=1e-4) == 0.621371

# ============================================================================
# WEIGHT CONVERSION TESTS
# ============================================================================

class TestWeightConversion:
    """Test suite for weight conversion functionality"""
    
    # Basic conversion tests
    def test_kilogram_to_gram(self):
        """Test basic kilogram to gram conversion"""
        result = convert_weight(1, 'kilogram', 'gram')
        assert result == 1000
    
    def test_pound_to_ounce(self):
        """Test basic pound to ounce conversion"""
        result = convert_weight(1, 'pound', 'ounce')
        assert pytest.approx(result, rel=1e-5) == 16
    
    def test_gram_to_milligram(self):
        """Test basic gram to milligram conversion"""
        result = convert_weight(1, 'gram', 'milligram')
        assert result == 1000
    
    def test_kilogram_to_pound(self):
        """Test kilogram to pound conversion (common use case)"""
        result = convert_weight(1, 'kilogram', 'pound')
        assert pytest.approx(result, rel=1e-4) == 2.20462
    
    # Same unit conversion
    def test_same_unit_conversion(self):
        """Test converting a unit to itself returns the same value"""
        result = convert_weight(100, 'gram', 'gram')
        assert result == 100
    
    # Decimal and floating point tests
    def test_decimal_conversion(self):
        """Test conversion with decimal values"""
        result = convert_weight(0.5, 'kilogram', 'gram')
        assert result == 500
    
    def test_small_weight_conversion(self):
        """Test conversion with very small weights"""
        result = convert_weight(0.001, 'gram', 'milligram')
        assert result == 1
    
    # Zero and negative values
    def test_zero_value_conversion(self):
        """Test conversion with zero value"""
        result = convert_weight(0, 'kilogram', 'gram')
        assert result == 0
    
    def test_negative_value_conversion(self):
        """Test conversion with negative value"""
        result = convert_weight(-5, 'kilogram', 'gram')
        assert result == -5000
    
    # Large numbers
    def test_large_weight_conversion(self):
        """Test conversion with very large weights"""
        result = convert_weight(1000000, 'gram', 'kilogram')
        assert result == 1000
    
    # Precision and rounding
    def test_conversion_precision(self):
        """Test that results are rounded to 6 decimal places"""
        result = convert_weight(1, 'ounce', 'gram')
        assert isinstance(result, float)
        assert len(str(result).split('.')[-1]) <= 6
    
    # Invalid unit tests
    def test_invalid_from_unit(self):
        """Test conversion with invalid 'from' unit"""
        result = convert_weight(10, 'invalid_unit', 'gram')
        assert result is None
    
    def test_invalid_to_unit(self):
        """Test conversion with invalid 'to' unit"""
        result = convert_weight(10, 'gram', 'invalid_unit')
        assert result is None
    
    def test_both_invalid_units(self):
        """Test conversion with both invalid units"""
        result = convert_weight(10, 'invalid1', 'invalid2')
        assert result is None
    
    # Metric to Imperial conversions
    def test_metric_to_imperial_conversion(self):
        """Test conversion from metric to imperial system"""
        result = convert_weight(100, 'gram', 'ounce')
        assert pytest.approx(result, rel=1e-4) == 3.5274

# ============================================================================
# TEMPERATURE CONVERSION TESTS
# ============================================================================

class TestTemperatureConversion:
    """Test suite for temperature conversion functionality"""
    
    # Basic conversion tests
    def test_celsius_to_fahrenheit_freezing(self):
        """Test water freezing point: 0°C = 32°F"""
        result = convert_temperature(0, 'Celsius', 'Fahrenheit')
        assert result == 32
    
    def test_celsius_to_fahrenheit_boiling(self):
        """Test water boiling point: 100°C = 212°F"""
        result = convert_temperature(100, 'Celsius', 'Fahrenheit')
        assert result == 212
    
    def test_fahrenheit_to_celsius_freezing(self):
        """Test water freezing point: 32°F = 0°C"""
        result = convert_temperature(32, 'Fahrenheit', 'Celsius')
        assert result == 0
    
    def test_celsius_to_kelvin_absolute_zero(self):
        """Test absolute zero: -273.15°C = 0K"""
        result = convert_temperature(-273.15, 'Celsius', 'Kelvin')
        assert result == 0
    
    def test_kelvin_to_celsius_zero_kelvin(self):
        """Test absolute zero: 0K = -273.15°C"""
        result = convert_temperature(0, 'Kelvin', 'Celsius')
        assert result == -273.15
    
    def test_fahrenheit_to_kelvin(self):
        """Test Fahrenheit to Kelvin conversion"""
        result = convert_temperature(32, 'Fahrenheit', 'Kelvin')
        assert result == 273.15
    
    # Same unit conversion
    def test_same_unit_celsius(self):
        """Test converting Celsius to Celsius"""
        result = convert_temperature(25, 'Celsius', 'Celsius')
        assert result == 25
    
    def test_same_unit_fahrenheit(self):
        """Test converting Fahrenheit to Fahrenheit"""
        result = convert_temperature(77, 'Fahrenheit', 'Fahrenheit')
        assert result == 77
    
    def test_same_unit_kelvin(self):
        """Test converting Kelvin to Kelvin"""
        result = convert_temperature(300, 'Kelvin', 'Kelvin')
        assert result == 300
    
    # Negative temperatures
    def test_negative_celsius(self):
        """Test negative Celsius temperature"""
        result = convert_temperature(-40, 'Celsius', 'Fahrenheit')
        assert result == -40  # -40°C = -40°F (special case)
    
    def test_negative_fahrenheit(self):
        """Test negative Fahrenheit temperature"""
        result = convert_temperature(-40, 'Fahrenheit', 'Celsius')
        assert result == -40
    
    # Zero values
    def test_zero_celsius(self):
        """Test zero Celsius"""
        result = convert_temperature(0, 'Celsius', 'Kelvin')
        assert result == 273.15
    
    def test_zero_kelvin(self):
        """Test zero Kelvin (absolute zero)"""
        result = convert_temperature(0, 'Kelvin', 'Fahrenheit')
        assert result == -459.67
    
    # Decimal values
    def test_decimal_celsius_conversion(self):
        """Test decimal temperature conversion"""
        result = convert_temperature(37.5, 'Celsius', 'Fahrenheit')
        assert result == 99.5
    
    # Body temperature
    def test_body_temperature_celsius_to_fahrenheit(self):
        """Test normal body temperature: 37°C ≈ 98.6°F"""
        result = convert_temperature(37, 'Celsius', 'Fahrenheit')
        assert result == 98.6
    
    # Room temperature
    def test_room_temperature_conversions(self):
        """Test room temperature: 20°C = 68°F"""
        result = convert_temperature(20, 'Celsius', 'Fahrenheit')
        assert result == 68
    
    # Precision tests
    def test_temperature_precision(self):
        """Test that temperature results are rounded to 2 decimal places"""
        result = convert_temperature(25.123456, 'Celsius', 'Fahrenheit')
        assert isinstance(result, float)
        # Result should be 77.22
        assert result == 77.22
    
    # Invalid unit tests
    def test_invalid_from_unit(self):
        """Test conversion with invalid 'from' unit"""
        result = convert_temperature(100, 'invalid', 'Celsius')
        assert result is None
    
    def test_invalid_to_unit(self):
        """Test conversion with invalid 'to' unit"""
        result = convert_temperature(100, 'Celsius', 'invalid')
        assert result is None
    
    def test_both_invalid_units(self):
        """Test conversion with both invalid units"""
        result = convert_temperature(100, 'invalid1', 'invalid2')
        assert result is None
    
    # Case sensitivity
    def test_case_sensitive_celsius(self):
        """Test that temperature units are case sensitive"""
        result = convert_temperature(100, 'celsius', 'Fahrenheit')
        assert result is None  # Should fail
    
    # Extreme temperatures
    def test_very_high_temperature(self):
        """Test conversion with very high temperature"""
        result = convert_temperature(5000, 'Celsius', 'Fahrenheit')
        assert result == 9032
    
    def test_very_low_temperature(self):
        """Test conversion below absolute zero (theoretically impossible but mathematically valid)"""
        result = convert_temperature(-300, 'Celsius', 'Kelvin')
        assert result == -26.85

# ============================================================================
# FLASK ROUTE TESTS
# ============================================================================

class TestFlaskRoutes:
    """Test suite for Flask web application routes"""
    
    def test_home_route(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Unit Converter' in response.data
    
    def test_length_route_get(self, client):
        """Test GET request to length converter page"""
        response = client.get('/length')
        assert response.status_code == 200
        assert b'Length Converter' in response.data
    
    def test_weight_route_get(self, client):
        """Test GET request to weight converter page"""
        response = client.get('/weight')
        assert response.status_code == 200
        assert b'Weight Converter' in response.data
    
    def test_temperature_route_get(self, client):
        """Test GET request to temperature converter page"""
        response = client.get('/temperature')
        assert response.status_code == 200
        assert b'Temperature Converter' in response.data
    
    def test_length_route_post_valid(self, client):
        """Test POST request to length converter with valid data"""
        response = client.post('/length', data={
            'value': '10',
            'from_unit': 'meter',
            'to_unit': 'centimeter'
        })
        assert response.status_code == 200
        assert b'1000' in response.data  # 10m = 1000cm
    
    def test_weight_route_post_valid(self, client):
        """Test POST request to weight converter with valid data"""
        response = client.post('/weight', data={
            'value': '1',
            'from_unit': 'kilogram',
            'to_unit': 'gram'
        })
        assert response.status_code == 200
        assert b'1000' in response.data  # 1kg = 1000g
    
    def test_temperature_route_post_valid(self, client):
        """Test POST request to temperature converter with valid data"""
        response = client.post('/temperature', data={
            'value': '0',
            'from_unit': 'Celsius',
            'to_unit': 'Fahrenheit'
        })
        assert response.status_code == 200
        assert b'32' in response.data  # 0°C = 32°F
    
    def test_length_route_post_invalid_value(self, client):
        """Test POST request with invalid (non-numeric) value"""
        response = client.post('/length', data={
            'value': 'abc',
            'from_unit': 'meter',
            'to_unit': 'centimeter'
        })
        assert response.status_code == 200
        assert b'valid number' in response.data
    
    def test_length_route_post_negative_value(self, client):
        """Test POST request with negative value"""
        response = client.post('/length', data={
            'value': '-10',
            'from_unit': 'meter',
            'to_unit': 'centimeter'
        })
        assert response.status_code == 200
        assert b'positive value' in response.data
    
    def test_weight_route_post_negative_value(self, client):
        """Test POST request to weight converter with negative value"""
        response = client.post('/weight', data={
            'value': '-5',
            'from_unit': 'kilogram',
            'to_unit': 'gram'
        })
        assert response.status_code == 200
        assert b'positive value' in response.data
    
    def test_temperature_route_post_decimal(self, client):
        """Test POST request with decimal temperature value"""
        response = client.post('/temperature', data={
            'value': '37.5',
            'from_unit': 'Celsius',
            'to_unit': 'Fahrenheit'
        })
        assert response.status_code == 200
        assert b'99.5' in response.data
    
    def test_invalid_route(self, client):
        """Test that invalid route returns 404"""
        response = client.get('/invalid_route')
        assert response.status_code == 404
    
    def test_length_form_preserves_values(self, client):
        """Test that form preserves input values after submission"""
        response = client.post('/length', data={
            'value': '50',
            'from_unit': 'foot',
            'to_unit': 'meter'
        })
        assert response.status_code == 200
        assert b'value="50"' in response.data or b'50' in response.data
    
    def test_empty_form_submission(self, client):
        """Test form submission with missing value"""
        response = client.post('/length', data={
            'value': '',
            'from_unit': 'meter',
            'to_unit': 'centimeter'
        })
        # Should handle gracefully (HTML5 validation or backend validation)
        assert response.status_code == 200

# ============================================================================
# EDGE CASE AND BOUNDARY TESTS
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases and boundary conditions"""
    
    def test_very_large_length_value(self):
        """Test conversion with astronomically large values"""
        result = convert_length(1e15, 'meter', 'kilometer')
        assert result == 1e12
    
    def test_very_small_length_value(self):
        """Test conversion with extremely small values"""
        result = convert_length(1e-10, 'meter', 'millimeter')
        assert result == pytest.approx(1e-7, rel=1e-5)
    
    def test_very_large_weight_value(self):
        """Test conversion with very large weight"""
        result = convert_weight(1e10, 'gram', 'kilogram')
        assert result == 1e7
    
    def test_float_precision_length(self):
        """Test that floating point precision is handled correctly"""
        result = convert_length(0.1 + 0.2, 'meter', 'centimeter')
        # 0.1 + 0.2 = 0.30000000000000004 in Python
        assert pytest.approx(result, rel=1e-5) == 30
    
    def test_temperature_at_absolute_zero(self):
        """Test conversion at absolute zero boundary"""
        result = convert_temperature(-273.15, 'Celsius', 'Kelvin')
        assert result == 0
    
    def test_temperature_below_absolute_zero(self):
        """Test temperature below absolute zero (impossible but mathematically valid)"""
        result = convert_temperature(-300, 'Celsius', 'Kelvin')
        assert result < 0  # Should return negative Kelvin (mathematically)
    
    def test_all_length_units_conversion(self, length_units):
        """Test that all length units can convert to all other units"""
        for from_unit in length_units:
            for to_unit in length_units:
                result = convert_length(1, from_unit, to_unit)
                assert result is not None
                assert isinstance(result, (int, float))
    
    def test_all_weight_units_conversion(self, weight_units):
        """Test that all weight units can convert to all other units"""
        for from_unit in weight_units:
            for to_unit in weight_units:
                result = convert_weight(1, from_unit, to_unit)
                assert result is not None
                assert isinstance(result, (int, float))
    
    def test_all_temperature_units_conversion(self, temperature_units):
        """Test that all temperature units can convert to all other units"""
        for from_unit in temperature_units:
            for to_unit in temperature_units:
                result = convert_temperature(100, from_unit, to_unit)
                assert result is not None
                assert isinstance(result, (int, float))
    
    def test_conversion_reversibility_length(self):
        """Test that converting back gives original value (within precision)"""
        original = 42.5
        converted = convert_length(original, 'meter', 'foot')
        back = convert_length(converted, 'foot', 'meter')
        assert pytest.approx(back, rel=1e-5) == original
    
    def test_conversion_reversibility_weight(self):
        """Test that converting back gives original value"""
        original = 100
        converted = convert_weight(original, 'kilogram', 'pound')
        back = convert_weight(converted, 'pound', 'kilogram')
        assert pytest.approx(back, rel=1e-5) == original
    
    def test_conversion_reversibility_temperature(self):
        """Test that converting back gives original value"""
        original = 25
        converted = convert_temperature(original, 'Celsius', 'Fahrenheit')
        back = convert_temperature(converted, 'Fahrenheit', 'Celsius')
        assert pytest.approx(back, rel=1e-2) == original

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])