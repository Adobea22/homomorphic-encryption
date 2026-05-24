#!/usr/bin/env python3
"""
Paillier Homomorphic Encryption Implementation
Demonstrates basic operations on encrypted data
"""

import random
import math

class PaillierHomomorphicEncryption:
    """
    Implementation of Paillier cryptosystem for homomorphic encryption.
    Supports addition on encrypted values and multiplication by plaintext constants.
    """
    
    def __init__(self, key_size=512):
        """Initialize with key generation"""
        self.key_size = key_size
        self.public_key, self.private_key = self.generate_keypair()
        
    def is_prime(self, n, k=5):
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
    
    def generate_prime(self, bits):
        """Generate a prime number of specified bit length"""
        while True:
            candidate = random.getrandbits(bits)
            candidate |= (1 << bits - 1) | 1  # Set MSB and LSB
            if self.is_prime(candidate):
                return candidate
    
    def lcm(self, a, b):
        """Least common multiple"""
        return abs(a * b) // math.gcd(a, b)
    
    def L(self, x, n):
        """L function for Paillier decryption: L(x) = (x-1)/n"""
        return (x - 1) // n
    
    def mod_inverse(self, a, m):
        """Compute modular multiplicative inverse"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m
    
    def generate_keypair(self):
        """Generate Paillier public and private keys"""
        print(f"[*] Generating {self.key_size}-bit Paillier keypair...")
        
        # Generate two large primes p and q
        p = self.generate_prime(self.key_size // 2)
        q = self.generate_prime(self.key_size // 2)
        
        # Compute n = p * q
        n = p * q
        n_squared = n * n
        
        # Compute λ = lcm(p-1, q-1)
        lambda_n = self.lcm(p - 1, q - 1)
        
        # Choose random g in Z*_{n^2}
        # For simplicity, use g = n + 1 (common choice)
        g = n + 1
        
        # Compute μ = (L(g^λ mod n^2))^(-1) mod n
        mu = self.mod_inverse(self.L(pow(g, lambda_n, n_squared), n), n)
        
        public_key = {'n': n, 'g': g, 'n_squared': n_squared}
        private_key = {'lambda': lambda_n, 'mu': mu}
        
        print(f"[+] Keys generated successfully!")
        print(f"    Public key (n): {n}")
        print(f"    Bit length: {n.bit_length()} bits\n")
        
        return public_key, private_key
    
    def encrypt(self, plaintext):
        """
        Encrypt a plaintext integer.
        E(m) = g^m * r^n mod n^2
        """
        n = self.public_key['n']
        g = self.public_key['g']
        n_squared = self.public_key['n_squared']
        
        # Ensure plaintext is in valid range [0, n)
        plaintext = plaintext % n
        
        # Choose random r in Z*_n
        r = random.randrange(1, n)
        while math.gcd(r, n) != 1:
            r = random.randrange(1, n)
        
        # Compute ciphertext: c = g^m * r^n mod n^2
        ciphertext = (pow(g, plaintext, n_squared) * pow(r, n, n_squared)) % n_squared
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        """
        Decrypt a ciphertext.
        D(c) = L(c^λ mod n^2) * μ mod n
        """
        n = self.public_key['n']
        n_squared = self.public_key['n_squared']
        lambda_n = self.private_key['lambda']
        mu = self.private_key['mu']
        
        # Compute plaintext: m = L(c^λ mod n^2) * μ mod n
        plaintext = (self.L(pow(ciphertext, lambda_n, n_squared), n) * mu) % n
        
        return plaintext
    
    def add_encrypted(self, ciphertext1, ciphertext2):
        """
        Add two encrypted values homomorphically.
        E(m1 + m2) = E(m1) * E(m2) mod n^2
        """
        n_squared = self.public_key['n_squared']
        return (ciphertext1 * ciphertext2) % n_squared
    
    def multiply_encrypted_by_constant(self, ciphertext, constant):
        """
        Multiply encrypted value by a plaintext constant.
        E(k * m) = E(m)^k mod n^2
        """
        n_squared = self.public_key['n_squared']
        return pow(ciphertext, constant, n_squared)


def demonstrate_homomorphic_operations():
    """Demonstrate homomorphic encryption operations"""
    
    print("="*70)
    print("  PAILLIER HOMOMORPHIC ENCRYPTION DEMONSTRATION")
    print("="*70)
    print()
    
    # Initialize the cryptosystem
    paillier = PaillierHomomorphicEncryption(key_size=512)
    
    # Test values
    m1 = 42
    m2 = 58
    k = 5
    
    print("[*] Encrypting values...")
    print(f"    Plaintext m1: {m1}")
    print(f"    Plaintext m2: {m2}")
    print(f"    Constant k: {k}")
    print()
    
    # Encrypt values
    c1 = paillier.encrypt(m1)
    c2 = paillier.encrypt(m2)
    
    print(f"[+] Encrypted values:")
    print(f"    E(m1): {c1}")
    print(f"    E(m2): {c2}")
    print()
    
    # Test decryption
    print("[*] Testing decryption...")
    d1 = paillier.decrypt(c1)
    d2 = paillier.decrypt(c2)
    print(f"    D(E(m1)): {d1} (Expected: {m1}) ✓" if d1 == m1 else f"    D(E(m1)): {d1} (Expected: {m1}) ✗")
    print(f"    D(E(m2)): {d2} (Expected: {m2}) ✓" if d2 == m2 else f"    D(E(m2)): {d2} (Expected: {m2}) ✗")
    print()
    
    # HOMOMORPHIC ADDITION
    print("="*70)
    print("  HOMOMORPHIC ADDITION: E(m1) + E(m2) = E(m1 + m2)")
    print("="*70)
    print()
    
    c_add = paillier.add_encrypted(c1, c2)
    result_add = paillier.decrypt(c_add)
    expected_add = m1 + m2
    
    print(f"[*] Computing E({m1}) ⊕ E({m2})...")
    print(f"    Result ciphertext: {c_add}")
    print(f"    Decrypted result: {result_add}")
    print(f"    Expected (m1 + m2): {expected_add}")
    print(f"    Status: {'✓ SUCCESS' if result_add == expected_add else '✗ FAILED'}")
    print()
    
    # HOMOMORPHIC MULTIPLICATION BY CONSTANT
    print("="*70)
    print("  HOMOMORPHIC SCALAR MULTIPLICATION: E(k * m1) = E(m1)^k")
    print("="*70)
    print()
    
    c_mult = paillier.multiply_encrypted_by_constant(c1, k)
    result_mult = paillier.decrypt(c_mult)
    expected_mult = k * m1
    
    print(f"[*] Computing E({m1})^{k}...")
    print(f"    Result ciphertext: {c_mult}")
    print(f"    Decrypted result: {result_mult}")
    print(f"    Expected ({k} * {m1}): {expected_mult}")
    print(f"    Status: {'✓ SUCCESS' if result_mult == expected_mult else '✗ FAILED'}")
    print()
    
    # COMBINED OPERATIONS
    print("="*70)
    print("  COMBINED OPERATION: k*m1 + m2")
    print("="*70)
    print()
    
    c_combined = paillier.add_encrypted(c_mult, c2)
    result_combined = paillier.decrypt(c_combined)
    expected_combined = k * m1 + m2
    
    print(f"[*] Computing E({k}*{m1}) ⊕ E({m2})...")
    print(f"    Decrypted result: {result_combined}")
    print(f"    Expected ({k}*{m1} + {m2}): {expected_combined}")
    print(f"    Status: {'✓ SUCCESS' if result_combined == expected_combined else '✗ FAILED'}")
    print()
    
    # PRACTICAL EXAMPLE: Encrypted voting
    print("="*70)
    print("  PRACTICAL EXAMPLE: ENCRYPTED VOTING SYSTEM")
    print("="*70)
    print()
    
    print("[*] Scenario: 5 voters, each vote is encrypted")
    votes = [1, 0, 1, 1, 0]  # 1 = Yes, 0 = No
    print(f"    Votes: {votes}")
    print()
    
    encrypted_votes = [paillier.encrypt(v) for v in votes]
    print("[+] All votes encrypted")
    
    # Homomorphically sum all votes
    total_encrypted = encrypted_votes[0]
    for i in range(1, len(encrypted_votes)):
        total_encrypted = paillier.add_encrypted(total_encrypted, encrypted_votes[i])
    
    total_votes = paillier.decrypt(total_encrypted)
    print(f"[+] Total 'Yes' votes (computed on encrypted data): {total_votes}")
    print(f"    Expected: {sum(votes)}")
    print(f"    Status: {'✓ CORRECT' if total_votes == sum(votes) else '✗ INCORRECT'}")
    print()
    
    print("="*70)
    print("  DEMONSTRATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    demonstrate_homomorphic_operations()
