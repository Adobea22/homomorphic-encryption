"""
Paillier Homomorphic Encryption
- Additively Homomorphic: E(m1) * E(m2) = E(m1 + m2)
- Scalar multiplication: E(m)^k = E(k*m)
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
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
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


def lcm(a, b):
    """Least common multiple"""
    return abs(a * b) // gcd(a, b)


def mod_inverse(a, m):
    """Extended Euclidean algorithm for modular inverse"""
    if gcd(a, m) != 1:
        raise ValueError("Modular inverse does not exist")
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m


class PaillierKeyPair:
    """Paillier cryptosystem key pair"""
    
    def __init__(self, key_size=2048):
        """
        Generate Paillier key pair
        
        Args:
            key_size: Size of primes in bits
        """
        self.key_size = key_size
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        
        self.n = self.p * self.q
        self.n_squared = self.n * self.n
        self.lambda_ = lcm(self.p - 1, self.q - 1)
        
        # Generate g
        self.g = self.generate_generator()
        
        # Compute mu for decryption
        self.mu = mod_inverse(self.l_function(pow(self.g, self.lambda_, self.n_squared), self.n), self.n)
    
    def generate_prime(self):
        """Generate a random prime of key_size bits"""
        while True:
            num = random.getrandbits(self.key_size // 2)
            num |= (1 << (self.key_size // 2 - 1)) | 1  # Ensure it's odd and has correct bit length
            if is_prime(num):
                return num
    
    def generate_generator(self):
        """Generate a valid generator g"""
        while True:
            g = random.randint(2, self.n * self.n - 1)
            if gcd(g, self.n_squared) == 1:
                if gcd(self.l_function(pow(g, self.lambda_, self.n_squared), self.n), self.n) == 1:
                    return g
    
    @staticmethod
    def l_function(u, n):
        """L function used in Paillier"""
        return (u - 1) // n
    
    def get_public_key(self):
        """Return public key (n, g)"""
        return PaillierPublicKey(self.n, self.g, self.n_squared)
    
    def get_private_key(self):
        """Return private key (lambda, mu)"""
        return PaillierPrivateKey(self.lambda_, self.mu, self.n, self.n_squared)


class PaillierPublicKey:
    """Public key for encryption"""
    
    def __init__(self, n, g, n_squared):
        self.n = n
        self.g = g
        self.n_squared = n_squared
    
    def encrypt(self, plaintext):
        """
        Encrypt a plaintext message
        
        Args:
            plaintext: Integer message to encrypt (0 <= m < n)
        
        Returns:
            Ciphertext (encrypted message)
        """
        assert 0 <= plaintext < self.n, f"Plaintext must be < {self.n}"
        
        r = random.randint(1, self.n - 1)
        while gcd(r, self.n) != 1:
            r = random.randint(1, self.n - 1)
        
        ciphertext = (pow(self.g, plaintext, self.n_squared) * pow(r, self.n, self.n_squared)) % self.n_squared
        return ciphertext
    
    def add_encrypted(self, c1, c2):
        """
        Add two encrypted numbers: E(m1) * E(m2) = E(m1 + m2)
        
        Args:
            c1: First ciphertext
            c2: Second ciphertext
        
        Returns:
            Encrypted sum
        """
        return (c1 * c2) % self.n_squared
    
    def multiply_encrypted_by_plaintext(self, ciphertext, scalar):
        """
        Multiply encrypted number by plaintext: E(m)^k = E(k*m)
        
        Args:
            ciphertext: Encrypted message
            scalar: Integer plaintext scalar
        
        Returns:
            Encrypted result of scalar multiplication
        """
        return pow(ciphertext, scalar, self.n_squared)


class PaillierPrivateKey:
    """Private key for decryption"""
    
    def __init__(self, lambda_, mu, n, n_squared):
        self.lambda_ = lambda_
        self.mu = mu
        self.n = n
        self.n_squared = n_squared
    
    def decrypt(self, ciphertext):
        """
        Decrypt a ciphertext
        
        Args:
            ciphertext: Encrypted message
        
        Returns:
            Decrypted plaintext
        """
        a = pow(ciphertext, self.lambda_, self.n_squared)
        l_u = PaillierKeyPair.l_function(a, self.n)
        plaintext = (l_u * self.mu) % self.n
        return plaintext


# Utility function for key generation
def generate_keys(key_size=512):
    """
    Generate Paillier key pair
    
    Args:
        key_size: Key size in bits (default 512 for faster generation)
    
    Returns:
        Tuple of (public_key, private_key)
    """
    keygen = PaillierKeyPair(key_size)
    return keygen.get_public_key(), keygen.get_private_key()
