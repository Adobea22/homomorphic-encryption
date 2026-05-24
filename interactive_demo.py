#!/usr/bin/env python3
"""
Interactive Homomorphic Encryption Demo
Allows users to experiment with encrypted calculations
"""

import sys
sys.path.append('.')
from homomorphic_encryption import PaillierHomomorphicEncryption

def print_banner():
    print("\n" + "="*70)
    print("  INTERACTIVE HOMOMORPHIC ENCRYPTION CALCULATOR")
    print("="*70)
    print("\n  Perform calculations on encrypted data without decrypting!")
    print("="*70 + "\n")

def main():
    print_banner()
    
    # Initialize encryption system
    print("[*] Initializing Paillier cryptosystem (512-bit keys)...")
    paillier = PaillierHomomorphicEncryption(key_size=512)
    print()
    
    while True:
        print("\n" + "-"*70)
        print("  MENU")
        print("-"*70)
        print("1. Encrypt two numbers and add them")
        print("2. Encrypt a number and multiply by constant")
        print("3. Complex calculation: (a + b) * k + c")
        print("4. Encrypted average calculation")
        print("5. Exit")
        print("-"*70)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n[*] Homomorphic Addition")
            try:
                a = int(input("Enter first number (a): "))
                b = int(input("Enter second number (b): "))
                
                print(f"\n[*] Encrypting {a} and {b}...")
                enc_a = paillier.encrypt(a)
                enc_b = paillier.encrypt(b)
                
                print("[*] Adding encrypted values: E(a) + E(b)...")
                enc_result = paillier.add_encrypted(enc_a, enc_b)
                
                result = paillier.decrypt(enc_result)
                print(f"\n[+] Result: {result}")
                print(f"    Expected: {a + b}")
                print(f"    Status: {'✓ CORRECT' if result == a + b else '✗ INCORRECT'}")
                
            except ValueError:
                print("[!] Invalid input. Please enter integers.")
        
        elif choice == '2':
            print("\n[*] Homomorphic Scalar Multiplication")
            try:
                a = int(input("Enter number to encrypt (a): "))
                k = int(input("Enter constant multiplier (k): "))
                
                print(f"\n[*] Encrypting {a}...")
                enc_a = paillier.encrypt(a)
                
                print(f"[*] Multiplying encrypted value by {k}: E(a)^k...")
                enc_result = paillier.multiply_encrypted_by_constant(enc_a, k)
                
                result = paillier.decrypt(enc_result)
                print(f"\n[+] Result: {result}")
                print(f"    Expected: {a * k}")
                print(f"    Status: {'✓ CORRECT' if result == a * k else '✗ INCORRECT'}")
                
            except ValueError:
                print("[!] Invalid input. Please enter integers.")
        
        elif choice == '3':
            print("\n[*] Complex Calculation: (a + b) * k + c")
            try:
                a = int(input("Enter first number (a): "))
                b = int(input("Enter second number (b): "))
                k = int(input("Enter multiplier (k): "))
                c = int(input("Enter third number (c): "))
                
                print(f"\n[*] Encrypting {a}, {b}, and {c}...")
                enc_a = paillier.encrypt(a)
                enc_b = paillier.encrypt(b)
                enc_c = paillier.encrypt(c)
                
                print("[*] Computing E(a+b)...")
                enc_sum = paillier.add_encrypted(enc_a, enc_b)
                
                print(f"[*] Computing E((a+b)*k) = E(a+b)^k...")
                enc_mult = paillier.multiply_encrypted_by_constant(enc_sum, k)
                
                print("[*] Computing E((a+b)*k + c)...")
                enc_result = paillier.add_encrypted(enc_mult, enc_c)
                
                result = paillier.decrypt(enc_result)
                expected = (a + b) * k + c
                
                print(f"\n[+] Result: {result}")
                print(f"    Expected: ({a} + {b}) * {k} + {c} = {expected}")
                print(f"    Status: {'✓ CORRECT' if result == expected else '✗ INCORRECT'}")
                
            except ValueError:
                print("[!] Invalid input. Please enter integers.")
        
        elif choice == '4':
            print("\n[*] Encrypted Average Calculation")
            try:
                n = int(input("How many numbers? "))
                if n <= 0:
                    print("[!] Please enter a positive number.")
                    continue
                
                numbers = []
                print()
                for i in range(n):
                    num = int(input(f"Enter number {i+1}: "))
                    numbers.append(num)
                
                print(f"\n[*] Encrypting all {n} numbers...")
                encrypted_nums = [paillier.encrypt(num) for num in numbers]
                
                print("[*] Computing encrypted sum...")
                enc_sum = encrypted_nums[0]
                for i in range(1, len(encrypted_nums)):
                    enc_sum = paillier.add_encrypted(enc_sum, encrypted_nums[i])
                
                total = paillier.decrypt(enc_sum)
                average = total / n
                expected_avg = sum(numbers) / n
                
                print(f"\n[+] Encrypted sum decrypts to: {total}")
                print(f"    Average: {average:.2f}")
                print(f"    Expected average: {expected_avg:.2f}")
                print(f"    Status: {'✓ CORRECT' if abs(average - expected_avg) < 0.01 else '✗ INCORRECT'}")
                
            except ValueError:
                print("[!] Invalid input. Please enter valid integers.")
        
        elif choice == '5':
            print("\n[*] Exiting... Goodbye!\n")
            break
        
        else:
            print("\n[!] Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user. Exiting...\n")
        sys.exit(0)
