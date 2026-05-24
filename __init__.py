"""
Homomorphic Encryption Package

This package provides implementations of three types of homomorphic encryption:
1. Paillier - Additively Homomorphic
2. RSA - Multiplicatively Homomorphic
3. BFV - Somewhat Homomorphic

Each scheme is in its own subpackage with examples.
"""

__version__ = "1.0.0"
__author__ = "Homomorphic Encryption Demo"

from paillier.paillier import generate_keys as paillier_generate_keys
from paillier.paillier import PaillierPublicKey, PaillierPrivateKey

from rsa.rsa import generate_keys as rsa_generate_keys
from rsa.rsa import RSAPublicKey, RSAPrivateKey

from bfv.bfv import generate_keys as bfv_generate_keys
from bfv.bfv import BFVPublicKey, BFVPrivateKey, BFVParameters

__all__ = [
    'paillier_generate_keys',
    'PaillierPublicKey',
    'PaillierPrivateKey',
    'rsa_generate_keys',
    'RSAPublicKey',
    'RSAPrivateKey',
    'bfv_generate_keys',
    'BFVPublicKey',
    'BFVPrivateKey',
    'BFVParameters',
]
