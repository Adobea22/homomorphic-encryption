"""
BFV (Brakerski-Fan-Vercauteren) Somewhat Homomorphic Encryption
- Supports both addition and multiplication on encrypted data
- Simplified implementation for demonstration
"""

import random
import numpy as np
from math import gcd


def next_power_of_2(n):
    """Find next power of 2"""
    power = 1
    while power < n:
        power *= 2
    return power


def get_prime_near(target):
    """Get a prime number near target"""
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    candidate = target
    while not is_prime(candidate):
        candidate -= 1
    return candidate


class BFVParameters:
    """BFV scheme parameters"""
    
    def __init__(self, degree=256, plaintext_modulus=65537):
        """
        Initialize BFV parameters
        
        Args:
            degree: Polynomial degree (power of 2)
            plaintext_modulus: Modulus for plaintext (prime)
        """
        self.degree = degree
        self.t = plaintext_modulus  # Plaintext modulus
        self.q = get_prime_near(2**60)  # Ciphertext modulus (large prime)
        self.standard_deviation = 3.19
    
    def sample_from_error_distribution(self, size):
        """Sample error values from error distribution (approximated as Gaussian)"""
        return [int(random.gauss(0, self.standard_deviation)) % self.q for _ in range(size)]


class BFVKeyPair:
    """BFV key pair generator"""
    
    def __init__(self, params):
        """
        Generate BFV key pair
        
        Args:
            params: BFVParameters instance
        """
        self.params = params
        n = params.degree
        
        # Secret key: random polynomial
        self.secret_key = [random.randint(0, 1) for _ in range(n)]
        
        # Public key generation
        a = [random.randint(0, params.q - 1) for _ in range(n)]
        e = params.sample_from_error_distribution(n)
        
        # pk = (b, a) where b = -(a*s + e) mod q
        self.public_key_a = a
        self.public_key_b = [(-sum(a[i] * self.secret_key[i] for i in range(n)) - e[j]) % params.q 
                              for j in range(n)]
        
        # Relinearization key (simplified)
        self.relin_key = self._generate_relin_key()
    
    def _generate_relin_key(self):
        """Generate relinearization key (simplified)"""
        n = self.params.degree
        return [random.randint(0, self.params.q - 1) for _ in range(n)]
    
    def get_public_key(self):
        """Return public key"""
        return BFVPublicKey(self.params, self.public_key_a, self.public_key_b)
    
    def get_private_key(self):
        """Return private key"""
        return BFVPrivateKey(self.params, self.secret_key)
    
    def get_relin_key(self):
        """Return relinearization key"""
        return self.relin_key


class BFVPublicKey:
    """BFV public key for encryption"""
    
    def __init__(self, params, pk_a, pk_b):
        self.params = params
        self.pk_a = pk_a
        self.pk_b = pk_b
    
    def encrypt(self, plaintext_values):
        """
        Encrypt plaintext values
        
        Args:
            plaintext_values: List of integers to encrypt
        
        Returns:
            Ciphertext (c0, c1)
        """
        n = self.params.degree
        params = self.params
        
        # Encode plaintext to polynomial
        plaintext = [0] * n
        for i, val in enumerate(plaintext_values[:n]):
            plaintext[i] = val % params.t
        
        # Generate random values and errors
        u = [random.randint(0, 1) for _ in range(n)]
        e1 = params.sample_from_error_distribution(n)
        e2 = params.sample_from_error_distribution(n)
        
        # Encryption: (c0, c1) where
        # c0 = b*u + e1 + delta*plaintext
        # c1 = a*u + e2
        delta = params.q // params.t
        
        c0 = [(self.pk_b[i] * u[i] + e1[i] + delta * plaintext[i]) % params.q for i in range(n)]
        c1 = [(self.pk_a[i] * u[i] + e2[i]) % params.q for i in range(n)]
        
        return (c0, c1)
    
    def add_encrypted(self, ct1, ct2):
        """
        Add two ciphertexts: E(m1) + E(m2) = E(m1 + m2)
        
        Args:
            ct1: First ciphertext (c0, c1)
            ct2: Second ciphertext (c0, c1)
        
        Returns:
            Sum ciphertext
        """
        q = self.params.q
        n = self.params.degree
        
        c0_sum = [(ct1[0][i] + ct2[0][i]) % q for i in range(n)]
        c1_sum = [(ct1[1][i] + ct2[1][i]) % q for i in range(n)]
        
        return (c0_sum, c1_sum)
    
    def multiply_encrypted(self, ct1, ct2):
        """
        Multiply two ciphertexts: E(m1) * E(m2) = E(m1 * m2)
        (Simplified - without full relinearization)
        
        Args:
            ct1: First ciphertext (c0, c1)
            ct2: Second ciphertext (c0, c1)
        
        Returns:
            Product ciphertext
        """
        q = self.params.q
        t = self.params.t
        n = self.params.degree
        
        # Simplified polynomial multiplication (convolution)
        d0 = [0] * n
        d1 = [0] * n
        d2 = [0] * n
        
        for i in range(n):
            for j in range(n):
                idx = (i + j) % n
                d0[idx] = (d0[idx] + ct1[0][i] * ct2[0][j]) % q
                d1[idx] = (d1[idx] + ct1[0][i] * ct2[1][j] + ct1[1][i] * ct2[0][j]) % q
                d2[idx] = (d2[idx] + ct1[1][i] * ct2[1][j]) % q
        
        # Scale down by q/t
        scale = q // t
        d0_scaled = [(val * scale // q) % q for val in d0]
        d1_scaled = [(val * scale // q) % q for val in d1]
        d2_scaled = [(val * scale // q) % q for val in d2]
        
        # Simple relinearization: combine d1 and d2 into c1
        c0 = d0_scaled
        c1 = [(d1_scaled[i] + d2_scaled[i]) % q for i in range(n)]
        
        return (c0, c1)


class BFVPrivateKey:
    """BFV private key for decryption"""
    
    def __init__(self, params, secret_key):
        self.params = params
        self.secret_key = secret_key
    
    def decrypt(self, ciphertext):
        """
        Decrypt ciphertext
        
        Args:
            ciphertext: Ciphertext (c0, c1)
        
        Returns:
            Decrypted plaintext values
        """
        c0, c1 = ciphertext
        n = self.params.degree
        q = self.params.q
        t = self.params.t
        
        # Compute m' = (c0 + c1*secret_key) mod q
        m_prime = [0] * n
        for i in range(n):
            val = c0[i]
            for j in range(n):
                val = (val + c1[j] * self.secret_key[(i - j) % n]) % q
            m_prime[i] = val
        
        # Scale down: m = m' * t / q mod t
        plaintext = [(val * t // q) % t for val in m_prime]
        
        return plaintext[:4]  # Return first 4 values as example


def generate_keys(params=None):
    """
    Generate BFV key pair
    
    Args:
        params: BFVParameters instance (default parameters if None)
    
    Returns:
        Tuple of (public_key, private_key, relin_key)
    """
    if params is None:
        params = BFVParameters(degree=256, plaintext_modulus=65537)
    
    keygen = BFVKeyPair(params)
    return (keygen.get_public_key(), keygen.get_private_key(), keygen.get_relin_key())
