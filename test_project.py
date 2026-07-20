import pytest
from project import validate_color, format_template_key, convert_color_to_rgb

def test_validate_color():
    assert validate_color("black") == "black"
    assert validate_color("WHITE ") == "white"
    with pytest.raises(ValueError):
        validate_color("blue")
    with pytest.raises(ValueError):
        validate_color("red")

def test_format_template_key():
    assert format_template_key("Scared Taylor") == "scared_taylor"
    assert format_template_key("  Mind  ") == "mind"
    assert format_template_key("taylor_bunduda") == "taylor_bunduda"

def test_convert_color_to_rgb():
    assert convert_color_to_rgb("white") == (255, 255, 255)
    assert convert_color_to_rgb("black") == (0, 0, 0)
    assert convert_color_to_rgb("qualquer_outra_coisa") == (0, 0, 0)
