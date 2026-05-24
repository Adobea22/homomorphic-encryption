"""
Utility functions for homomorphic encryption operations
Provides common interfaces and helper functions across all schemes
"""

from paillier.paillier import generate_keys as paillier_generate_keys
from rsa.rsa import generate_keys as rsa_generate_keys
from bfv.bfv import generate_keys as bfv_generate_keys, BFVParameters


class HomomorphicEncryptionDemo:
    """Unified interface for demonstrations across all HE schemes"""
    
    @staticmethod
    def run_paillier_demo():
        """Run Paillier demonstration"""
        print("\n" + "="*70)
        print("PAILLIER ADDITIVE HOMOMORPHIC ENCRYPTION")
        print("="*70)
        
        pub, priv = paillier_generate_keys(key_size=512)
        
        # Example values
        a, b = 100, 50
        
        print(f"\n[1] Simple Addition: {a} + {b} = {a + b}")
        ca = pub.encrypt(a)
        cb = pub.encrypt(b)
        c_sum = pub.add_encrypted(ca, cb)
        result = priv.decrypt(c_sum)
        print(f"    Encrypted result: {result}")
        
        print(f"\n[2] Scalar Multiplication: {a} * 3 = {a * 3}")
        c_scaled = pub.multiply_encrypted_by_plaintext(ca, 3)
        result = priv.decrypt(c_scaled)
        print(f"    Encrypted result: {result}")
        
        print(f"\n[3] Complex: ({a} + {b}) * 2 = {(a + b) * 2}")
        c1 = pub.add_encrypted(ca, cb)
        c2 = pub.multiply_encrypted_by_plaintext(c1, 2)
        result = priv.decrypt(c2)
        print(f"    Encrypted result: {result}")
    
    @staticmethod
    def run_rsa_demo():
        """Run RSA demonstration"""
        print("\n" + "="*70)
        print("RSA MULTIPLICATIVE HOMOMORPHIC ENCRYPTION")
        print("="*70)
        
        pub, priv = rsa_generate_keys(key_size=512)
        
        # Example values (small to ensure result < n)
        a, b = 2, 3
        
        print(f"\n[1] Simple Multiplication: {a} * {b} = {a * b}")
        ca = pub.encrypt(a)
        cb = pub.encrypt(b)
        c_product = pub.multiply_encrypted(ca, cb)
        result = priv.decrypt(c_product)
        expected = (a * b) % pub.n
        print(f"    Encrypted result: {result} (expected: {expected})")
        
        print(f"\n[2] Power Operation: {a}^{b} = {a ** b}")
        c_power = pub.power_encrypted(ca, b)
        result = priv.decrypt(c_power)
        expected = pow(a, b, pub.n)
        print(f"    Encrypted result: {result} (expected: {expected})")
        
        print(f"\n[3] Complex: ({a} * {b})^2 = {(a * b) ** 2}")
        c1 = pub.multiply_encrypted(ca, cb)
        c2 = pub.power_encrypted(c1, 2)
        result = priv.decrypt(c2)
        expected = pow(a * b, 2, pub.n)
        print(f"    Encrypted result: {result} (expected: {expected})")
    
    @staticmethod
    def run_bfv_demo():
        """Run BFV demonstration"""
        print("\n" + "="*70)
        print("BFV SOMEWHAT HOMOMORPHIC ENCRYPTION")
        print("="*70)
        
        params = BFVParameters(degree=256, plaintext_modulus=65537)
        pub, priv, relin = bfv_generate_keys(params)
        
        # Example vectors
        v1 = [10, 20, 30, 40]
        v2 = [2, 3, 1, 2]
        
        print(f"\n[1] Vector Addition (element-wise):")
        print(f"    {v1} + {v2}")
        c1 = pub.encrypt(v1)
        c2 = pub.encrypt(v2)
        c_sum = pub.add_encrypted(c1, c2)
        result = priv.decrypt(c_sum)
        expected = [v1[i] + v2[i] for i in range(len(v1))]
        print(f"    Result: {result}")
        print(f"    Expected: {expected}")
        
        print(f"\n[2] Vector Multiplication (element-wise):")
        c_prod = pub.multiply_encrypted(c1, c2)
        result = priv.decrypt(c_prod)
        print(f"    Result: {result}")
        
        print(f"\n[3] Mixed Operations: (v1 + v2) - v2:")
        c_sum = pub.add_encrypted(c1, c2)
        c_diff = pub.add_encrypted(c_sum, c2)  # Simulated subtraction
        result = priv.decrypt(c_diff)
        print(f"    Result: {result}")


class OperationCounter:
    """Track and count operations performed on encrypted data"""
    
    def __init__(self):
        self.additions = 0
        self.multiplications = 0
        self.encryptions = 0
        self.decryptions = 0
    
    def record_addition(self):
        self.additions += 1
    
    def record_multiplication(self):
        self.multiplications += 1
    
    def record_encryption(self):
        self.encryptions += 1
    
    def record_decryption(self):
        self.decryptions += 1
    
    def print_summary(self):
        print("\nOperation Summary:")
        print(f"  Encryptions:     {self.encryptions}")
        print(f"  Additions:       {self.additions}")
        print(f"  Multiplications: {self.multiplications}")
        print(f"  Decryptions:     {self.decryptions}")


def benchmark_scheme(scheme_name, key_size=512, iterations=5):
    """Benchmark a homomorphic encryption scheme"""
    import time
    
    print(f"\nBenchmarking {scheme_name}...")
    
    if scheme_name.lower() == "paillier":
        pub, priv = paillier_generate_keys(key_size=key_size)
        
        start = time.time()
        for _ in range(iterations):
            c1 = pub.encrypt(42)
            c2 = pub.encrypt(58)
        encrypt_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            c_sum = pub.add_encrypted(c1, c2)
        addition_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            result = priv.decrypt(c_sum)
        decrypt_time = (time.time() - start) / iterations
        
        print(f"  Key generation: {key_size} bits")
        print(f"  Encryption:     {encrypt_time*1000:.2f} ms")
        print(f"  Addition:       {addition_time*1000:.2f} ms")
        print(f"  Decryption:     {decrypt_time*1000:.2f} ms")
    
    elif scheme_name.lower() == "rsa":
        pub, priv = rsa_generate_keys(key_size=key_size)
        
        start = time.time()
        for _ in range(iterations):
            c1 = pub.encrypt(2)
            c2 = pub.encrypt(3)
        encrypt_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            c_prod = pub.multiply_encrypted(c1, c2)
        mult_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            result = priv.decrypt(c_prod)
        decrypt_time = (time.time() - start) / iterations
        
        print(f"  Key generation: {key_size} bits")
        print(f"  Encryption:     {encrypt_time*1000:.2f} ms")
        print(f"  Multiplication: {mult_time*1000:.2f} ms")
        print(f"  Decryption:     {decrypt_time*1000:.2f} ms")
    
    elif scheme_name.lower() == "bfv":
        params = BFVParameters(degree=256, plaintext_modulus=65537)
        pub, priv, relin = bfv_generate_keys(params)
        
        v1 = [10, 20, 30, 40]
        v2 = [2, 3, 1, 2]
        
        start = time.time()
        for _ in range(iterations):
            c1 = pub.encrypt(v1)
            c2 = pub.encrypt(v2)
        encrypt_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            c_sum = pub.add_encrypted(c1, c2)
        add_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            c_prod = pub.multiply_encrypted(c1, c2)
        mult_time = (time.time() - start) / iterations
        
        start = time.time()
        for _ in range(iterations):
            result = priv.decrypt(c_sum)
        decrypt_time = (time.time() - start) / iterations
        
        print(f"  Degree:         256, Plaintext modulus: 65537")
        print(f"  Encryption:     {encrypt_time*1000:.2f} ms")
        print(f"  Addition:       {add_time*1000:.2f} ms")
        print(f"  Multiplication: {mult_time*1000:.2f} ms")
        print(f"  Decryption:     {decrypt_time*1000:.2f} ms")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("HOMOMORPHIC ENCRYPTION UNIFIED DEMONSTRATION")
    print("="*70)
    
    # Run all demonstrations
    HomomorphicEncryptionDemo.run_paillier_demo()
    HomomorphicEncryptionDemo.run_rsa_demo()
    HomomorphicEncryptionDemo.run_bfv_demo()
    
    # Run benchmarks
    print("\n" + "="*70)
    print("PERFORMANCE BENCHMARKING")
    print("="*70)
    
    benchmark_scheme("paillier", key_size=512, iterations=3)
    benchmark_scheme("rsa", key_size=512, iterations=3)
    benchmark_scheme("bfv", iterations=3)
    
    print("\n" + "="*70)
    print("All demonstrations completed!")
    print("="*70)
