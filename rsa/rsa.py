"""
RSA Homomorphic Encryption
- Multiplicatively Homomorphic: E(m1) * E(m2) = E(m1 * m2)
- Useful for scenarios where multiplication properties are needed
"""

import random
from math import gcd


def is_prime(n, k=10):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def extended_gcd(a, b):
    """Extended Euclidean algorithm"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(a, m):
    """Compute modular inverse using extended Euclidean algorithm"""
    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m


class RSAKeyPair:
    """RSA key pair generator"""
    
    def __init__(self, key_size=2048):
        """
        Generate RSA key pair
        
        Args:
            key_size: Size of modulus in bits
        """
        self.key_size = key_size
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        
        self.n = self.p * self.q
        self.e = 65537  # Common public exponent
        self.phi = (self.p - 1) * (self.q - 1)
        
        # Ensure gcd(e, phi) = 1
        while gcd(self.e, self.phi) != 1:
            self.e += 2
        
        self.d = mod_inverse(self.e, self.phi)
    
    def generate_prime(self):
        """Generate a random prime of appropriate bit size"""
        while True:
            num = random.getrandbits(self.key_size // 2)
            num |= (1 << (self.key_size // 2 - 1)) | 1
            if is_prime(num):
                return num
    
    def get_public_key(self):
        """Return public key (n, e)"""
        return RSAPublicKey(self.n, self.e)
    
    def get_private_key(self):
        """Return private key (n, d)"""
        return RSAPrivateKey(self.n, self.d)


class RSAPublicKey:
    """RSA public key for encryption"""
    
    def __init__(self, n, e):
        self.n = n
        self.e = e
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using RSA
        
        Args:
            plaintext: Integer message (0 <= m < n)
        
        Returns:
            Ciphertext
        """
        assert 0 <= plaintext < self.n, f"Plaintext must be < {self.n}"
        return pow(plaintext, self.e, self.n)
    
    def multiply_encrypted(self, c1, c2):
        """
        Multiply two encrypted numbers (MULTIPLICATIVE HOMOMORPHISM)
        E(m1) * E(m2) = E(m1 * m2) mod n
        
        Args:
            c1: First ciphertext
            c2: Second ciphertext
        
        Returns:
            Encrypted product
        """
        return (c1 * c2) % self.n
    
    def power_encrypted(self, ciphertext, exponent):
        """
        Raise encrypted value to a power
        E(m)^k = E(m^k) mod n
        
        Args:
            ciphertext: Encrypted message
            exponent: Power to raise to
        
        Returns:
            Encrypted result
        """
        return pow(ciphertext, exponent, self.n)


class RSAPrivateKey:
    """RSA private key for decryption"""
    
    def __init__(self, n, d):
        self.n = n
        self.d = d
    
    def decrypt(self, ciphertext):
        """
        Decrypt RSA ciphertext
        
        Args:
            ciphertext: Encrypted message
        
        Returns:
            Plaintext message
        """
        return pow(ciphertext, self.d, self.n)


def generate_keys(key_size=512):
    """
    Generate RSA key pair
    
    Args:
        key_size: Key size in bits
    
    Returns:
        Tuple of (public_key, private_key)
    """
    keygen = RSAKeyPair(key_size)
    return keygen.get_public_key(), keygen.get_private_key()
