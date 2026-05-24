"""
Example: RSA Multiplicative Homomorphic Encryption Demo
Demonstrates encryption, multiplication, and power operations on encrypted data
"""

from rsa import generate_keys


def main():
    print("=" * 60)
    print("RSA MULTIPLICATIVE HOMOMORPHIC ENCRYPTION DEMO")
    print("=" * 60)
    
    # Generate keys
    print("\n[*] Generating RSA keys (key_size=512 bits)...")
    public_key, private_key = generate_keys(key_size=512)
    print("[✓] Keys generated successfully")
    print(f"    Modulus n: {public_key.n}")
    print(f"    Public exponent e: {public_key.e}")
    
    # Example 1: Basic encryption and decryption
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Encryption & Decryption")
    print("=" * 60)
    
    message1 = 7
    message2 = 13
    
    print(f"\nOriginal messages: m1 = {message1}, m2 = {message2}")
    
    c1 = public_key.encrypt(message1)
    c2 = public_key.encrypt(message2)
    print(f"Encrypted: c1 = {c1}, c2 = {c2}")
    
    d1 = private_key.decrypt(c1)
    d2 = private_key.decrypt(c2)
    print(f"Decrypted: m1 = {d1}, m2 = {d2}")
    
    # Example 2: Multiplication on encrypted data (multiplicative homomorphism)
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multiplicative Homomorphism (multiplication on encrypted data)")
    print("=" * 60)
    
    print(f"\nWe have: E({message1}) and E({message2})")
    
    # Note: In RSA, we need smaller values for multiplication to stay within n
    message1 = 3
    message2 = 5
    
    # Encrypt both messages
    c1 = public_key.encrypt(message1)
    c2 = public_key.encrypt(message2)
    
    print(f"\nMessages (adjusted): m1 = {message1}, m2 = {message2}")
    
    # Multiply encrypted values
    c_product = public_key.multiply_encrypted(c1, c2)
    print(f"\nE({message1}) * E({message2}) = E({message1} * {message2})")
    print(f"Ciphertext of product: {c_product}")
    
    # Decrypt the result
    product_result = private_key.decrypt(c_product)
    expected = (message1 * message2) % public_key.n
    print(f"Decrypted: {product_result}")
    print(f"Expected: {expected}, Got: {product_result} {'✓' if product_result == expected else '✗'}")
    
    # Example 3: Power operation
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Power Operation (E(m)^k = E(m^k))")
    print("=" * 60)
    
    message = 2
    exponent = 5
    
    print(f"\nMessage: m = {message}, Exponent: k = {exponent}")
    
    c_msg = public_key.encrypt(message)
    print(f"E({message}) encrypted")
    
    # Power operation
    c_power = public_key.power_encrypted(c_msg, exponent)
    print(f"\nE({message})^{exponent} = E({message}^{exponent})")
    print(f"Ciphertext after power: {c_power}")
    
    # Decrypt the result
    power_result = private_key.decrypt(c_power)
    expected = pow(message, exponent, public_key.n)
    print(f"Decrypted: {power_result}")
    print(f"Expected: {expected}, Got: {power_result} {'✓' if power_result == expected else '✗'}")
    
    # Example 4: Complex operation
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Complex Operation: (m1 * m2) ^ k = E(m1 * m2)^k")
    print("=" * 60)
    
    m1, m2, k = 2, 3, 2
    
    print(f"\nValues: m1={m1}, m2={m2}, k={k}")
    print(f"Operation: (m1 * m2) ^ k = ({m1} * {m2}) ^ {k} = {pow(m1 * m2, k)}")
    
    # Encrypt
    c1 = public_key.encrypt(m1)
    c2 = public_key.encrypt(m2)
    
    # Multiply: E(m1) * E(m2) = E(m1 * m2)
    c_product = public_key.multiply_encrypted(c1, c2)
    
    # Power: E(m1 * m2)^k = E((m1 * m2)^k)
    c_result = public_key.power_encrypted(c_product, k)
    
    # Decrypt
    result = private_key.decrypt(c_result)
    expected = pow(m1 * m2, k, public_key.n)
    print(f"\nComputed result: {result}")
    print(f"Expected: {expected}, Got: {result} {'✓' if result == expected else '✗'}")
    
    # Example 5: Chain multiplication
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Chain Multiplication: m1 * m2 * m3")
    print("=" * 60)
    
    values = [2, 2, 2]
    
    print(f"\nValues: {values}")
    print(f"Product: {2 * 2 * 2}")
    
    # Encrypt all values
    encrypted = [public_key.encrypt(val) for val in values]
    
    # Multiply all encrypted values
    result_encrypted = encrypted[0]
    for c in encrypted[1:]:
        result_encrypted = public_key.multiply_encrypted(result_encrypted, c)
    
    # Decrypt
    result = private_key.decrypt(result_encrypted)
    expected_prod = 1
    for v in values:
        expected_prod = (expected_prod * v) % public_key.n
    
    print(f"\nComputed product: {result}")
    print(f"Expected: {expected_prod}, Got: {result} {'✓' if result == expected_prod else '✗'}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
