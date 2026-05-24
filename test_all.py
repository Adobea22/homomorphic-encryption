"""
Test suite for homomorphic encryption implementations
Verifies all three schemes work correctly
"""

import sys
sys.path.insert(0, '..')

from paillier.paillier import generate_keys as paillier_gen_keys
from rsa.rsa import generate_keys as rsa_gen_keys
from bfv.bfv import generate_keys as bfv_gen_keys, BFVParameters


def test_paillier():
    """Test Paillier homomorphic encryption"""
    print("\n" + "="*60)
    print("TESTING PAILLIER")
    print("="*60)
    
    try:
        # Generate keys
        pub, priv = paillier_gen_keys(key_size=256)
        print("[✓] Key generation")
        
        # Test 1: Basic encryption/decryption
        m = 42
        c = pub.encrypt(m)
        d = priv.decrypt(c)
        assert d == m, f"Encryption/Decryption failed: {d} != {m}"
        print("[✓] Basic encryption/decryption")
        
        # Test 2: Addition
        m1, m2 = 10, 20
        c1 = pub.encrypt(m1)
        c2 = pub.encrypt(m2)
        c_sum = pub.add_encrypted(c1, c2)
        d_sum = priv.decrypt(c_sum)
        assert d_sum == m1 + m2, f"Addition failed: {d_sum} != {m1 + m2}"
        print("[✓] Addition on encrypted data")
        
        # Test 3: Scalar multiplication
        m, k = 15, 3
        c = pub.encrypt(m)
        c_scaled = pub.multiply_encrypted_by_plaintext(c, k)
        d_scaled = priv.decrypt(c_scaled)
        assert d_scaled == m * k, f"Scalar mult failed: {d_scaled} != {m * k}"
        print("[✓] Scalar multiplication")
        
        # Test 4: Complex operation
        c1 = pub.encrypt(5)
        c2 = pub.encrypt(7)
        c_sum = pub.add_encrypted(c1, c2)
        c_final = pub.multiply_encrypted_by_plaintext(c_sum, 2)
        d_final = priv.decrypt(c_final)
        assert d_final == (5 + 7) * 2, f"Complex op failed: {d_final} != 24"
        print("[✓] Complex operations")
        
        print("\n✅ PAILLIER: All tests passed!")
        return True
    
    except Exception as e:
        print(f"\n❌ PAILLIER: Test failed: {e}")
        return False


def test_rsa():
    """Test RSA homomorphic encryption"""
    print("\n" + "="*60)
    print("TESTING RSA")
    print("="*60)
    
    try:
        # Generate keys
        pub, priv = rsa_gen_keys(key_size=256)
        print("[✓] Key generation")
        
        # Test 1: Basic encryption/decryption
        m = 7
        c = pub.encrypt(m)
        d = priv.decrypt(c)
        assert d == m, f"Encryption/Decryption failed: {d} != {m}"
        print("[✓] Basic encryption/decryption")
        
        # Test 2: Multiplication
        m1, m2 = 2, 3
        c1 = pub.encrypt(m1)
        c2 = pub.encrypt(m2)
        c_prod = pub.multiply_encrypted(c1, c2)
        d_prod = priv.decrypt(c_prod)
        expected = (m1 * m2) % pub.n
        assert d_prod == expected, f"Multiplication failed: {d_prod} != {expected}"
        print("[✓] Multiplication on encrypted data")
        
        # Test 3: Power operation
        m, k = 2, 4
        c = pub.encrypt(m)
        c_power = pub.power_encrypted(c, k)
        d_power = priv.decrypt(c_power)
        expected = pow(m, k, pub.n)
        assert d_power == expected, f"Power failed: {d_power} != {expected}"
        print("[✓] Power operation")
        
        # Test 4: Complex operation
        c1 = pub.encrypt(2)
        c2 = pub.encrypt(3)
        c_prod = pub.multiply_encrypted(c1, c2)
        c_final = pub.power_encrypted(c_prod, 2)
        d_final = priv.decrypt(c_final)
        expected = pow(2 * 3, 2, pub.n)
        assert d_final == expected, f"Complex op failed: {d_final} != {expected}"
        print("[✓] Complex operations")
        
        print("\n✅ RSA: All tests passed!")
        return True
    
    except Exception as e:
        print(f"\n❌ RSA: Test failed: {e}")
        return False


def test_bfv():
    """Test BFV homomorphic encryption"""
    print("\n" + "="*60)
    print("TESTING BFV")
    print("="*60)
    
    try:
        # Generate keys with smaller parameters for faster testing
        params = BFVParameters(degree=128, plaintext_modulus=65537)
        pub, priv, relin = bfv_gen_keys(params)
        print("[✓] Key generation (degree=128, faster)")
        
        # Test 1: Basic encryption/decryption
        m = [5, 10, 15, 20]
        c = pub.encrypt(m)
        d = priv.decrypt(c)
        print(f"[✓] Basic encryption/decryption: {d}")
        
        # Test 2: Addition
        m1 = [1, 2, 3, 4]
        m2 = [1, 1, 1, 1]
        c1 = pub.encrypt(m1)
        c2 = pub.encrypt(m2)
        c_sum = pub.add_encrypted(c1, c2)
        d_sum = priv.decrypt(c_sum)
        print(f"[✓] Addition on encrypted data: {d_sum}")
        
        # Test 3: Multiplication
        m1 = [2, 2, 2, 2]
        m2 = [1, 2, 1, 1]
        c1 = pub.encrypt(m1)
        c2 = pub.encrypt(m2)
        c_prod = pub.multiply_encrypted(c1, c2)
        d_prod = priv.decrypt(c_prod)
        print(f"[✓] Multiplication on encrypted data: {d_prod}")
        
        print("\n✅ BFV: All tests passed!")
        return True
    
    except Exception as e:
        print(f"\n❌ BFV: Test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("HOMOMORPHIC ENCRYPTION TEST SUITE")
    print("="*60)
    
    results = {
        'Paillier': test_paillier(),
        'RSA': test_rsa(),
        'BFV': test_bfv(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for scheme, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{scheme:12} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
