"""
Example: Paillier Additive Homomorphic Encryption Demo
Demonstrates encryption, addition, and scalar multiplication on encrypted data
"""

from paillier import generate_keys


def main():
    print("=" * 60)
    print("PAILLIER ADDITIVE HOMOMORPHIC ENCRYPTION DEMO")
    print("=" * 60)
    
    # Generate keys
    print("\n[*] Generating Paillier keys (key_size=512 bits)...")
    public_key, private_key = generate_keys(key_size=512)
    print("[✓] Keys generated successfully")
    
    # Example 1: Basic encryption and decryption
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Encryption & Decryption")
    print("=" * 60)
    
    message1 = 42
    message2 = 58
    
    print(f"\nOriginal messages: m1 = {message1}, m2 = {message2}")
    
    c1 = public_key.encrypt(message1)
    c2 = public_key.encrypt(message2)
    print(f"Encrypted: c1 = {c1}, c2 = {c2}")
    
    d1 = private_key.decrypt(c1)
    d2 = private_key.decrypt(c2)
    print(f"Decrypted: m1 = {d1}, m2 = {d2}")
    
    # Example 2: Addition on encrypted data
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Additive Homomorphism (addition on encrypted data)")
    print("=" * 60)
    
    print(f"\nWe have: E({message1}) and E({message2})")
    
    # Encrypt both messages
    c1 = public_key.encrypt(message1)
    c2 = public_key.encrypt(message2)
    
    # Add encrypted values
    c_sum = public_key.add_encrypted(c1, c2)
    print(f"\nE({message1}) * E({message2}) = E({message1} + {message2})")
    print(f"Ciphertext of sum: {c_sum}")
    
    # Decrypt the result
    sum_result = private_key.decrypt(c_sum)
    print(f"Decrypted: {sum_result}")
    print(f"Expected: {message1 + message2}, Got: {sum_result} ✓")
    
    # Example 3: Scalar multiplication
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Scalar Multiplication (E(m)^k = E(k*m))")
    print("=" * 60)
    
    message = 15
    scalar = 7
    
    print(f"\nMessage: m = {message}, Scalar: k = {scalar}")
    
    c_msg = public_key.encrypt(message)
    print(f"E({message}) encrypted")
    
    # Scalar multiplication
    c_scaled = public_key.multiply_encrypted_by_plaintext(c_msg, scalar)
    print(f"\nE({message})^{scalar} = E({scalar} * {message})")
    print(f"Ciphertext after scaling: {c_scaled}")
    
    # Decrypt the result
    scaled_result = private_key.decrypt(c_scaled)
    print(f"Decrypted: {scaled_result}")
    print(f"Expected: {scalar * message} (mod {public_key.n}), Got: {scaled_result} ✓")
    
    # Example 4: Complex operation
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Complex Operation: (m1 + m2) * k = E(m1 + m2)^k")
    print("=" * 60)
    
    m1, m2, k = 10, 20, 3
    
    print(f"\nValues: m1={m1}, m2={m2}, k={k}")
    print(f"Operation: (m1 + m2) * k = ({m1} + {m2}) * {k} = {(m1 + m2) * k}")
    
    # Encrypt
    c1 = public_key.encrypt(m1)
    c2 = public_key.encrypt(m2)
    
    # Add: E(m1) * E(m2) = E(m1 + m2)
    c_sum = public_key.add_encrypted(c1, c2)
    
    # Scale: E(m1 + m2)^k = E(k * (m1 + m2))
    c_result = public_key.multiply_encrypted_by_plaintext(c_sum, k)
    
    # Decrypt
    result = private_key.decrypt(c_result)
    print(f"\nComputed result: {result}")
    print(f"Expected: {(m1 + m2) * k}, Got: {result} ✓")
    
    # Example 5: Multiple additions
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Multiple Additions: m1 + m2 + m3 + m4")
    print("=" * 60)
    
    values = [5, 10, 15, 20]
    
    print(f"\nValues: {values}")
    print(f"Sum: {sum(values)}")
    
    # Encrypt all values
    encrypted = [public_key.encrypt(val) for val in values]
    
    # Add all encrypted values
    result_encrypted = encrypted[0]
    for c in encrypted[1:]:
        result_encrypted = public_key.add_encrypted(result_encrypted, c)
    
    # Decrypt
    result = private_key.decrypt(result_encrypted)
    print(f"\nComputed sum: {result}")
    print(f"Expected: {sum(values)}, Got: {result} ✓")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
