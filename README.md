# Homomorphic Encryption Project

## Overview
This project implements **Paillier Homomorphic Encryption**, a cryptographic system that allows mathematical operations to be performed on encrypted data without decrypting it first.

## What is Homomorphic Encryption?

Homomorphic encryption is a form of encryption that permits users to perform computations on encrypted data without first decrypting it. The results of operations remain in encrypted form and, when decrypted, match the results of operations performed on the plaintext.

### Real-World Applications
- **Cloud Computing**: Perform computations on sensitive data in the cloud without exposing it
- **Electronic Voting**: Tally encrypted votes without revealing individual choices
- **Medical Data Analysis**: Analyze patient data while maintaining privacy
- **Financial Services**: Compute statistics on encrypted financial data
- **Machine Learning**: Train models on encrypted datasets

## Paillier Cryptosystem

The Paillier cryptosystem is a **partially homomorphic** encryption scheme with the following properties:

### Supported Operations
1. **Additive Homomorphism**: E(m₁) ⊗ E(m₂) = E(m₁ + m₂)
   - Adding two encrypted numbers gives the encryption of their sum
   
2. **Scalar Multiplication**: E(m)^k = E(k × m)
   - Raising an encrypted number to a power k gives the encryption of k times that number

### Mathematical Foundation

#### Key Generation
1. Choose two large prime numbers p and q
2. Compute n = p × q
3. Compute λ = lcm(p-1, q-1)
4. Choose generator g = n + 1
5. Compute μ = (L(g^λ mod n²))⁻¹ mod n
   - Where L(x) = (x-1)/n

**Public Key**: (n, g)
**Private Key**: (λ, μ)

#### Encryption
Given plaintext m and public key (n, g):
1. Choose random r where gcd(r, n) = 1
2. Ciphertext: c = g^m × r^n mod n²

#### Decryption
Given ciphertext c and private key (λ, μ):
1. Plaintext: m = L(c^λ mod n²) × μ mod n

## Project Structure

```
homomorphic-encryption/
│
├── homomorphic_encryption.py    # Core implementation
├── interactive_demo.py          # Interactive calculator
├── secure_salary_demo.py        # Practical salary computation example
└── README.md                    # This file
```

## Files Description

### 1. homomorphic_encryption.py
Core implementation of the Paillier cryptosystem with:
- Key generation (512-bit default)
- Encryption and decryption
- Homomorphic addition
- Homomorphic scalar multiplication
- Demonstration with voting example

### 2. interactive_demo.py
Interactive command-line calculator that lets you:
- Add encrypted numbers
- Multiply encrypted numbers by constants
- Perform complex calculations: (a + b) × k + c
- Calculate encrypted averages

### 3. secure_salary_demo.py
Practical demonstration showing:
- Secure salary aggregation
- Computing bonuses on encrypted data
- Privacy-preserving analytics

## Installation & Usage

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (pure Python implementation)

### Running the Demos

#### 1. Basic Demonstration
```bash
python3 homomorphic_encryption.py
```
This runs a comprehensive demonstration showing:
- Key generation
- Encryption/decryption
- Homomorphic addition
- Homomorphic multiplication
- Combined operations
- Encrypted voting example

#### 2. Interactive Calculator
```bash
python3 interactive_demo.py
```
Allows you to experiment with encrypted calculations interactively.

#### 3. Salary Computation Example
```bash
python3 secure_salary_demo.py
```
Demonstrates computing payroll statistics on encrypted data.

## Example Usage

```python
from homomorphic_encryption import PaillierHomomorphicEncryption

# Initialize the system
paillier = PaillierHomomorphicEncryption(key_size=512)

# Encrypt two numbers
a = 15
b = 27
enc_a = paillier.encrypt(a)
enc_b = paillier.encrypt(b)

# Add them without decryption
enc_sum = paillier.add_encrypted(enc_a, enc_b)

# Decrypt the result
result = paillier.decrypt(enc_sum)
print(f"Result: {result}")  # Output: 42

# Multiply by constant
enc_doubled = paillier.multiply_encrypted_by_constant(enc_a, 2)
doubled = paillier.decrypt(enc_doubled)
print(f"Doubled: {doubled}")  # Output: 30
```

## Performance Considerations

- **Key Size**: 512-bit keys are used for demonstration. For production:
  - Use 2048-bit or 3072-bit keys for security
  - Larger keys = more security but slower operations
  
- **Operation Complexity**:
  - Encryption: O(log n)
  - Decryption: O(log n)
  - Addition: O(1) on ciphertext
  - Multiplication: O(log k) where k is the constant

## Security Notes

⚠️ **Important Security Considerations**:

1. **Key Size**: This demo uses 512-bit keys for speed. Production systems should use 2048+ bits.

2. **Random Number Generation**: Uses Python's `random` module. For cryptographic applications, use `secrets` or `os.urandom`.

3. **Timing Attacks**: This implementation doesn't protect against side-channel attacks.

4. **Multiplicative Homomorphism**: Paillier only supports addition and scalar multiplication, not multiplication of two encrypted values.

## Limitations

- **Partially Homomorphic**: Only supports addition and scalar multiplication
- **Ciphertext Expansion**: Encrypted data is larger than plaintext
- **Computational Overhead**: Operations on encrypted data are slower
- **No Division**: Cannot divide encrypted values

## For Your Project Report

### Key Concepts to Include:

1. **What Problem Does It Solve?**
   - Enables computation on encrypted data
   - Maintains privacy in cloud computing
   - Allows data analysis without data exposure

2. **How It Works** (High-Level):
   - Uses mathematical properties of modular arithmetic
   - Addition in plaintext = multiplication in ciphertext
   - Scalar multiplication in plaintext = exponentiation in ciphertext

3. **Practical Applications**:
   - Secure voting systems
   - Privacy-preserving medical research
   - Confidential financial analytics
   - Secure machine learning

4. **Advantages**:
   - Strong mathematical security foundation
   - Deterministic operations on encrypted data
   - No need to share decryption keys

5. **Challenges**:
   - Computational overhead
   - Limited to certain operations
   - Large ciphertext sizes

## Testing the Implementation

Run all three scripts to verify:
```bash
# Run comprehensive demo
python3 homomorphic_encryption.py

# Test interactive features
python3 interactive_demo.py

# See practical application
python3 secure_salary_demo.py
```

All outputs should show ✓ SUCCESS for correctness verification.

## Further Reading

- **Original Paper**: "Public-Key Cryptosystems Based on Composite Degree Residuosity Classes" by Pascal Paillier (1999)
- **Fully Homomorphic Encryption**: Look into BGV, BFV, and CKKS schemes
- **Libraries**: python-phe, SEAL (Microsoft), HElib

## Authors & License

Created for educational purposes - Cybersecurity Project
University of Mines and Technology

## Questions?

For any questions about the implementation or concepts:
- Review the inline comments in the code
- Check the demonstration outputs
- Experiment with the interactive demo

---

**Note**: This is an educational implementation. For production use, consider established libraries like python-phe or Microsoft SEAL.
