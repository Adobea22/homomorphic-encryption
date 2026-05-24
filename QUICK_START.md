# Homomorphic Encryption - Quick Start Guide

## Overview

This project provides three implementations of homomorphic encryption schemes in Python:

1. **Paillier** - Additive homomorphic encryption
2. **RSA** - Multiplicative homomorphic encryption
3. **BFV** - Somewhat homomorphic encryption (supports both operations)

## Installation

No external dependencies required. Just Python 3.6+

## Quick Examples

### 1. Paillier - Adding Encrypted Numbers

```bash
cd paillier
python example_paillier.py
```

**What it does:**
- Encrypts two numbers: 42 and 58
- Adds them without decrypting: E(42) * E(58) = E(100)
- Decrypts the result to get 100

**Output:**
```
Original messages: m1 = 42, m2 = 58
E(42) * E(58) = E(42 + 58)
Decrypted result: 100 ✓
```

### 2. RSA - Multiplying Encrypted Numbers

```bash
cd rsa
python example_rsa.py
```

**What it does:**
- Encrypts two numbers: 3 and 5
- Multiplies them without decrypting: E(3) * E(5) = E(15)
- Decrypts the result to get 15

**Output:**
```
Messages: m1 = 3, m2 = 5
E(3) * E(5) = E(3 * 5)
Decrypted result: 15 ✓
```

### 3. BFV - Adding and Multiplying Encrypted Vectors

```bash
cd bfv
python example_bfv.py
```

**What it does:**
- Encrypts vectors [10, 20, 30, 40] and [2, 3, 1, 2]
- Adds and multiplies them element-wise without decrypting
- Decrypts results

**Output:**
```
Vector addition: [10, 20, 30, 40] + [2, 3, 1, 2] = [12, 23, 31, 42]
```

## File Structure

```
homomorphic_encryption/
├── paillier/
│   ├── paillier.py              # Paillier implementation
│   ├── example_paillier.py      # Usage examples (run this!)
│   └── __init__.py
├── rsa/
│   ├── rsa.py                   # RSA implementation
│   ├── example_rsa.py           # Usage examples (run this!)
│   └── __init__.py
├── bfv/
│   ├── bfv.py                   # BFV implementation
│   ├── example_bfv.py           # Usage examples (run this!)
│   └── __init__.py
├── utils.py                      # Utility functions and benchmarks
├── __init__.py
└── README.md                     # Full documentation
```

## Key Concepts

### Homomorphic Encryption Property

In traditional encryption:
```
Encrypt(m1) = c1
Encrypt(m2) = c2
Decrypt(c1 + c2) ≠ m1 + m2
```

With Homomorphic Encryption:
```
Encrypt(m1) * Encrypt(m2) = Encrypt(m1 + m2)  [Paillier]
Encrypt(m1) * Encrypt(m2) = Encrypt(m1 * m2)  [RSA]
```

### How It Works

1. Generate public and private keys
2. Encrypt data with public key
3. Perform operations on encrypted data
4. Decrypt result with private key

## Use Cases

| Scheme | Use Case |
|--------|----------|
| Paillier | Secure voting, encrypted sum, privacy-preserving aggregation |
| RSA | Digital signatures, encrypted bit operations |
| BFV | Machine learning on encrypted data, complex computations |

## Running Your Own Code

### Paillier Example

```python
from paillier.paillier import generate_keys

# Generate keys
pub_key, priv_key = generate_keys(key_size=512)

# Encrypt two numbers
c1 = pub_key.encrypt(100)
c2 = pub_key.encrypt(50)

# Add without decrypting
c_sum = pub_key.add_encrypted(c1, c2)

# Decrypt result
result = priv_key.decrypt(c_sum)
print(result)  # Output: 150
```

### RSA Example

```python
from rsa.rsa import generate_keys

# Generate keys
pub_key, priv_key = generate_keys(key_size=512)

# Encrypt two numbers
c1 = pub_key.encrypt(5)
c2 = pub_key.encrypt(7)

# Multiply without decrypting
c_product = pub_key.multiply_encrypted(c1, c2)

# Decrypt result
result = priv_key.decrypt(c_product)
print(result)  # Output: 35
```

### BFV Example

```python
from bfv.bfv import generate_keys, BFVParameters

# Generate keys
params = BFVParameters(degree=256, plaintext_modulus=65537)
pub_key, priv_key, relin_key = generate_keys(params)

# Encrypt vectors
c1 = pub_key.encrypt([1, 2, 3, 4])
c2 = pub_key.encrypt([2, 3, 4, 5])

# Add encrypted vectors
c_sum = pub_key.add_encrypted(c1, c2)

# Decrypt result
result = priv_key.decrypt(c_sum)
print(result)  # Output: [3, 5, 7, 9]
```

## Performance Notes

- **Paillier**: Fast encryption/decryption, suitable for addition-based applications
- **RSA**: Very fast, but limited to multiplication
- **BFV**: Slower, but supports both addition and multiplication

## Advanced: Running Benchmarks

```bash
python utils.py
```

This will:
- Run demonstrations for all three schemes
- Benchmark encryption, operations, and decryption
- Show performance differences

## Common Issues

### "Key size too small"
- Paillier requires generating two large primes (can take time)
- Use `key_size=512` for testing, `key_size=2048` for security

### "Import errors"
- Make sure you're running from the correct directory
- The `__init__.py` files enable proper module imports

### "BFV is very slow"
- Normal! BFV uses polynomials and is more complex
- Use smaller polynomial degrees for faster results
- This is by design - security vs performance tradeoff

## Next Steps

1. Run the examples to see homomorphic encryption in action
2. Modify the example scripts to try different values
3. Read the README.md for detailed technical information
4. Study the source code to understand the cryptographic details
5. Implement your own applications using these primitives

## Resources

- **Paillier Paper**: "Public-Key Cryptosystems Based on Composite Degree Residuosity Classes"
- **RSA Paper**: "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems"
- **BFV Paper**: "(Leveled) Fully Homomorphic Encryption without Bootstrapping"
- **Python HE Library**: phe, TenSEAL, SEAL

## Troubleshooting

**Q: Why is BFV so slow?**
A: Polynomial operations over large fields are computationally intensive. This is expected.

**Q: Can I use larger key sizes?**
A: Yes, but generation will take longer. Use 512-bit for demo, 2048-bit for real use.

**Q: Why are my decrypted values slightly different?**
A: BFV has noise that grows with operations. Results are approximate due to the scheme design.

**Q: Can I perform unlimited operations?**
A: - Paillier: Yes, additions
- RSA: Limited multiplications
- BFV: Limited by noise budget

---

**Enjoy exploring homomorphic encryption!**
