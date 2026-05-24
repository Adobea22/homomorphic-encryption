#!/usr/bin/env python3
"""
Practical Application: Secure Salary Computation
Demonstrates computing statistics on encrypted salary data
"""

import sys
sys.path.append('.')
from homomorphic_encryption import PaillierHomomorphicEncryption

def print_banner():
    print("\n" + "="*70)
    print("  SECURE SALARY COMPUTATION SYSTEM")
    print("="*70)
    print("\n  Compute salary statistics without revealing individual salaries")
    print("="*70 + "\n")

def main():
    print_banner()
    
    # Sample scenario
    print("[*] Scenario: Company wants to compute total payroll")
    print("    without revealing individual employee salaries")
    print()
    
    # Employee salary data (in thousands)
    employees = {
        "Alice": 45,
        "Bob": 52,
        "Charlie": 48,
        "Diana": 55,
        "Eve": 50
    }
    
    print("[*] Employee data:")
    for name, salary in employees.items():
        print(f"    {name}: ${salary}k")
    print()
    
    # Initialize encryption
    print("[*] Initializing homomorphic encryption system...")
    paillier = PaillierHomomorphicEncryption(key_size=512)
    print()
    
    # Encrypt all salaries
    print("[*] Encrypting all employee salaries...")
    encrypted_salaries = {}
    for name, salary in employees.items():
        encrypted_salaries[name] = paillier.encrypt(salary)
        print(f"    {name}'s salary encrypted")
    print()
    
    # Compute total on encrypted data
    print("[*] Computing total payroll on ENCRYPTED data...")
    print("    (No individual salaries are visible during computation)")
    print()
    
    total_encrypted = list(encrypted_salaries.values())[0]
    for enc_salary in list(encrypted_salaries.values())[1:]:
        total_encrypted = paillier.add_encrypted(total_encrypted, enc_salary)
    
    # Decrypt only the final result
    print("[*] Decrypting final total...")
    total_payroll = paillier.decrypt(total_encrypted)
    expected_total = sum(employees.values())
    
    print()
    print("="*70)
    print("  RESULTS")
    print("="*70)
    print(f"Total Payroll (computed on encrypted data): ${total_payroll}k")
    print(f"Expected Total: ${expected_total}k")
    print(f"Status: {'✓ CORRECT' if total_payroll == expected_total else '✗ INCORRECT'}")
    print()
    
    # Compute average
    average = total_payroll / len(employees)
    print(f"Average Salary: ${average:.2f}k")
    print()
    
    # Compute bonus (10% increase)
    print("="*70)
    print("  COMPUTING 10% BONUS (ON ENCRYPTED DATA)")
    print("="*70)
    print()
    
    bonus_factor = 110  # 110% of original (10% increase)
    encrypted_with_bonus = {}
    
    for name, enc_salary in encrypted_salaries.items():
        # Multiply encrypted salary by 110 then divide by 100
        enc_new = paillier.multiply_encrypted_by_constant(enc_salary, bonus_factor)
        encrypted_with_bonus[name] = enc_new
    
    print("[*] New salaries with 10% bonus:")
    for name in employees.keys():
        original = employees[name]
        new_salary = paillier.decrypt(encrypted_with_bonus[name]) / 100
        expected_new = original * 1.10
        print(f"    {name}: ${new_salary:.2f}k (Expected: ${expected_new:.2f}k) {'✓' if abs(new_salary - expected_new) < 0.01 else '✗'}")
    print()
    
    # Compute new total
    total_with_bonus_enc = list(encrypted_with_bonus.values())[0]
    for enc_salary in list(encrypted_with_bonus.values())[1:]:
        total_with_bonus_enc = paillier.add_encrypted(total_with_bonus_enc, enc_salary)
    
    new_total = paillier.decrypt(total_with_bonus_enc) / 100
    expected_new_total = sum(employees.values()) * 1.10
    
    print(f"New Total Payroll: ${new_total:.2f}k")
    print(f"Expected: ${expected_new_total:.2f}k")
    print(f"Status: {'✓ CORRECT' if abs(new_total - expected_new_total) < 0.01 else '✗ INCORRECT'}")
    print()
    
    print("="*70)
    print("  KEY BENEFITS")
    print("="*70)
    print("✓ Individual salaries remain encrypted during computation")
    print("✓ Only aggregate results are decrypted")
    print("✓ Privacy-preserving data analysis")
    print("✓ Useful for secure cloud computing, audits, surveys")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
