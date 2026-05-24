"""
Example: BFV Somewhat Homomorphic Encryption Demo
Demonstrates encryption, addition, and multiplication on encrypted data
"""

from bfv import generate_keys, BFVParameters


def main():
    print("=" * 60)
    print("BFV SOMEWHAT HOMOMORPHIC ENCRYPTION DEMO")
    print("=" * 60)
    
    # Generate keys with default parameters
    print("\n[*] Generating BFV keys...")
    params = BFVParameters(degree=256, plaintext_modulus=65537)
    public_key, private_key, relin_key = generate_keys(params)
    print("[✓] Keys generated successfully")
    print(f"    Polynomial degree: {params.degree}")
    print(f"    Plaintext modulus: {params.t}")
    print(f"    Ciphertext modulus: {params.q}")
    
    # Example 1: Basic encryption and decryption
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Encryption & Decryption")
    print("=" * 60)
    
    plaintext1 = [10, 5, 15, 20]
    plaintext2 = [2, 7, 3, 5]
    
    print(f"\nOriginal plaintexts:")
    print(f"  m1 = {plaintext1}")
    print(f"  m2 = {plaintext2}")
    
    c1 = public_key.encrypt(plaintext1)
    c2 = public_key.encrypt(plaintext2)
    print(f"\n[*] Messages encrypted")
    
    d1 = private_key.decrypt(c1)
    d2 = private_key.decrypt(c2)
    print(f"\nDecrypted:")
    print(f"  m1 = {d1}")
    print(f"  m2 = {d2}")
    
    # Example 2: Addition on encrypted data
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Additive Homomorphism (addition on encrypted data)")
    print("=" * 60)
    
    plaintext1 = [1, 2, 3, 4]
    plaintext2 = [5, 6, 7, 8]
    
    print(f"\nMessages:")
    print(f"  m1 = {plaintext1}")
    print(f"  m2 = {plaintext2}")
    print(f"  Expected sum (component-wise): {[plaintext1[i] + plaintext2[i] for i in range(4)]}")
    
    # Encrypt
    c1 = public_key.encrypt(plaintext1)
    c2 = public_key.encrypt(plaintext2)
    print(f"\n[*] Messages encrypted")
    
    # Add encrypted values
    c_sum = public_key.add_encrypted(c1, c2)
    print(f"[*] Performed addition on encrypted data: E(m1) + E(m2)")
    
    # Decrypt
    sum_result = private_key.decrypt(c_sum)
    print(f"\nDecrypted sum: {sum_result}")
    expected = [plaintext1[i] + plaintext2[i] for i in range(len(plaintext1))]
    print(f"Expected:     {expected}")
    
    # Example 3: Multiplication on encrypted data
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Multiplicative Homomorphism (multiplication on encrypted data)")
    print("=" * 60)
    print("\nNote: BFV supports noise-bounded multiplication")
    
    plaintext1 = [2, 3, 1, 2]
    plaintext2 = [1, 1, 2, 1]
    
    print(f"\nMessages:")
    print(f"  m1 = {plaintext1}")
    print(f"  m2 = {plaintext2}")
    
    # Encrypt
    c1 = public_key.encrypt(plaintext1)
    c2 = public_key.encrypt(plaintext2)
    print(f"\n[*] Messages encrypted")
    
    # Multiply encrypted values
    c_product = public_key.multiply_encrypted(c1, c2)
    print(f"[*] Performed multiplication on encrypted data: E(m1) * E(m2)")
    
    # Decrypt
    product_result = private_key.decrypt(c_product)
    print(f"\nDecrypted product: {product_result}")
    
    # Example 4: Mixed operations
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Mixed Operations (Addition then Multiplication)")
    print("=" * 60)
    
    plaintext1 = [1, 2, 1, 1]
    plaintext2 = [1, 1, 1, 1]
    plaintext3 = [2, 2, 2, 2]
    
    print(f"\nMessages:")
    print(f"  m1 = {plaintext1}")
    print(f"  m2 = {plaintext2}")
    print(f"  m3 = {plaintext3}")
    print(f"  Operation: (m1 + m2) * m3")
    
    # Encrypt all
    c1 = public_key.encrypt(plaintext1)
    c2 = public_key.encrypt(plaintext2)
    c3 = public_key.encrypt(plaintext3)
    
    # Add first two
    c_sum = public_key.add_encrypted(c1, c2)
    print(f"\n[*] Step 1: E(m1) + E(m2)")
    
    # Multiply by third
    c_result = public_key.multiply_encrypted(c_sum, c3)
    print(f"[*] Step 2: (E(m1) + E(m2)) * E(m3)")
    
    # Decrypt
    result = private_key.decrypt(c_result)
    print(f"\nDecrypted result: {result}")
    
    # Example 5: Vector data processing
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Vector Processing (SIMD-like operations)")
    print("=" * 60)
    
    # Simulate processing multiple data points
    data1 = [10, 20, 30, 40]
    data2 = [2, 2, 2, 2]
    
    print(f"\nProcessing vectors element-wise:")
    print(f"  data1 = {data1}")
    print(f"  data2 = {data2} (multiplier)")
    
    # Encrypt vectors
    c_data1 = public_key.encrypt(data1)
    c_data2 = public_key.encrypt(data2)
    
    print(f"\n[*] Both vectors encrypted")
    
    # Perform element-wise operations
    c_result = public_key.multiply_encrypted(c_data1, c_data2)
    print(f"[*] Element-wise multiplication performed")
    
    # Decrypt
    result = private_key.decrypt(c_result)
    print(f"\nDecrypted result: {result}")
    expected = [data1[i] * data2[i] for i in range(len(data1))]
    print(f"Expected (approx): {expected}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    
    print("""
SUMMARY OF HOMOMORPHIC ENCRYPTION SCHEMES:
============================================

1. PAILLIER (Partially Homomorphic):
   - Supports: Addition E(m1) + E(m2) = E(m1 + m2)
   - Supports: Scalar multiplication E(m)^k = E(k*m)
   - Use case: Voting, auction, privacy-preserving sum

2. RSA (Partially Homomorphic):
   - Supports: Multiplication E(m1) * E(m2) = E(m1 * m2)
   - Supports: Exponentiation E(m)^k = E(m^k)
   - Use case: Encrypted bit operations, small computation

3. BFV (Somewhat Homomorphic):
   - Supports: Both addition and multiplication (with noise management)
   - Limitations: Cannot perform unlimited operations (noise growth)
   - Use case: Complex encrypted computations with limited depth
""")


if __name__ == "__main__":
    main()
