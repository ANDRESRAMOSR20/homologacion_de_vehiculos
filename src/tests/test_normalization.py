import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from src.core.normalization.normalizer import normalizer

def test_basic_cleaning():
    assert normalizer.normalize("  HOLA   MUNDO  ") == "hola mundo"
    assert normalizer.normalize("Camión") == "camion"
    assert normalizer.normalize("Mazda 3") == "mazda 3"

def test_synonym_expansion():
    assert normalizer.normalize("mazda 3 aut") == "mazda 3 automatico"
    assert normalizer.normalize("vw gol std") == "vw gol standard"
    assert normalizer.normalize("jeep 4x4") == "jeep traccion cuatro ruedas"

def test_deduplication():
    assert normalizer.normalize("sedan sedan") == "sedan"
    assert normalizer.normalize("mazda mazda 3") == "mazda 3"

def test_complex_vehicle():
    input_text = "JEEP GRAND CHEROKEE 2023 SUMMIT RESERVE 4XE, L4, 2.0T, 375 CP, 5 PUERTAS, AUT, PHEV"
    normalized = normalizer.normalize(input_text)
    assert "hibrido enchufable" in normalized
    assert "caballos de fuerza" in normalized

def test_normalize_alphanumeric_split():
    assert normalizer.normalize("mazda3") == "mazda 3"
    assert normalizer.normalize("cx5") == "cx 5"
    assert normalizer.normalize("f150") == "f 150"

def test_empty_input():
    assert normalizer.normalize("") == ""
    assert normalizer.normalize(None) == ""
