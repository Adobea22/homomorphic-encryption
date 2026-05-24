# QUICK REFERENCE GUIDE
## Homomorphic Encryption Project

### Getting Started (Quick)

```bash
# Run main demonstration
python3 homomorphic_encryption.py

# Interactive calculator
python3 interactive_demo.py

# Practical example
python3 secure_salary_demo.py
```

---

### Basic Usage

```python
from homomorphic_encryption import PaillierHomomorphicEncryption

# 1. Initialize
paillier = PaillierHomomorphicEncryption(key_size=512)

# 2. Encrypt
a = 15
b = 27
enc_a = paillier.encrypt(a)
enc_b = paillier.encrypt(b)

# 3. Add (homomorphically)
enc_sum = paillier.add_encrypted(enc_a, enc_b)

# 4. Decrypt
result = paillier.decrypt(enc_sum)
# result = 42

# 5. Multiply by constant
enc_doubled = paillier.multiply_encrypted_by_constant(enc_a, 2)
doubled = paillier.decrypt(enc_doubled)
# doubled = 30
```

---

### Key Concepts

**Homomorphic Addition:**
```
E(a) × E(b) = E(a + b)
```
Multiply ciphertexts → get sum when decrypted

**Homomorphic Scalar Multiplication:**
```
E(a)^k = E(k × a)
```
Raise ciphertext to power k → get k×a when decrypted

---

### Files Overview

| File | Purpose |
|------|---------|
| `homomorphic_encryption.py` | Core implementation + demo |
| `interactive_demo.py` | User-friendly calculator |
| `secure_salary_demo.py` | Real-world application |
| `README.md` | Full documentation |
| `PROJECT_REPORT.md` | Academic report |
| `QUICK_REFERENCE.md` | This file |

---

### Common Operations

**Basic Addition:**
```python
# Add two encrypted numbers
result = paillier.add_encrypted(enc_a, enc_b)
```

**Multiply by Constant:**
```python
# Multiply encrypted number by 5
result = paillier.multiply_encrypted_by_constant(enc_a, 5)
```

**Complex Calculation:** (a + b) × k + c
```python
# Step 1: Add a and b
enc_sum = paillier.add_encrypted(enc_a, enc_b)

# Step 2: Multiply by k
enc_mult = paillier.multiply_encrypted_by_constant(enc_sum, k)

# Step 3: Add c
enc_result = paillier.add_encrypted(enc_mult, enc_c)

# Step 4: Decrypt
result = paillier.decrypt(enc_result)
```

---

### Security Notes

⚠️ **512-bit keys**: Demo only  
✓ **2048+ bits**: Production use  
⚠️ **Random module**: Not cryptographically secure  
✓ **Use secrets module**: For production  

---

### Troubleshooting

**Problem**: Decryption gives wrong result  
**Solution**: Check that you're using the same Paillier instance

**Problem**: Encryption is slow  
**Solution**: Normal for large keys; 512-bit is faster for demos

**Problem**: Import error  
**Solution**: Files must be in same directory

---

### Key Features

✓ Pure Python implementation  
✓ No external dependencies  
✓ Educational code with comments  
✓ Multiple demonstrations  
✓ Practical applications  

---

### Applications

1. **Cloud Computing**: Process encrypted data
2. **E-Voting**: Count votes privately
3. **Medical Data**: Analyze without exposure
4. **Finance**: Audit encrypted records
5. **Statistics**: Compute on sensitive data

---

### Performance (512-bit)

| Operation | Time |
|-----------|------|
| Key Generation | 2-5 sec |
| Encryption | <10 ms |
| Decryption | <10 ms |
| Addition | <1 ms |
| Multiplication | ~5 ms |

---

### Mathematical Foundation

**Key Generation:**
```
p, q = large primes
n = p × q
λ = lcm(p-1, q-1)
g = n + 1
μ = (L(g^λ mod n²))⁻¹ mod n
```

**Encryption:**
```
c = g^m × r^n mod n²
(where r is random)
```

**Decryption:**
```
m = L(c^λ mod n²) × μ mod n
(where L(x) = (x-1)/n)
```

---

### For Your Presentation

**Key Points to Mention:**

1. **What**: Encryption that allows computation
2. **Why**: Privacy in cloud computing
3. **How**: Mathematical properties (additive homomorphism)
4. **Demo**: Show live calculations
5. **Uses**: Voting, medical data, finance

**Demo Script:**
```bash
# Show this live:
python3 interactive_demo.py

# Choose option 1 (addition)
# Enter: 42 and 58
# Result: 100 ✓
```

---

### Exam/Report Tips

**Understand These:**
- Definition of homomorphic encryption
- Difference between partial and fully homomorphic
- Paillier's additive property
- Real-world applications
- Security trade-offs

**Be Ready to Explain:**
- Why multiplication in ciphertext = addition in plaintext
- Why we need randomization (r)
- What makes it secure (RSA assumption)
- Limitations (no division, ciphertext expansion)

---

### Quick Terminology

- **E(m)**: Encrypted value of m
- **D(c)**: Decrypted value of ciphertext c
- **⊗**: Homomorphic operation
- **n**: Public modulus (p × q)
- **λ**: Private lambda value
- **Ciphertext**: Encrypted data
- **Plaintext**: Unencrypted data

---

### Resources for Further Study

- Original Paillier paper (1999)
- Microsoft SEAL library
- IBM Homomorphic Encryption toolkit
- Fully Homomorphic Encryption (FHE) research

---

**Created by**: Akey Wisdom Selasi  
**Institution**: University of Mines and Technology  
**Course**: Cybersecurity  
**Date**: February 2026
