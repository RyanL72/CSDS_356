import numpy as np


def poly_mod(x, mod, n):
    """
    Reduces polynomial x modulo (x^n + 1) and coefficient-wise modulo mod.
    (This simulates the underlying ring arithmetic.)
    """
    x = np.array(x)[:n]
    # For coefficients beyond degree n-1, reduce using x^n ≡ -1.
    for i in range(n, len(x)):
        x[i - n] -= x[i]
    return np.remainder(x, mod)

def generate_keys(n, q, scale, sigma, seed=None):
    """
    Generate a secret key and corresponding public key.
    For CKKS, note that messages will be scaled by 'scale' for approximate arithmetic.
    """
    if seed is not None:
        np.random.seed(seed)
        
    sk = np.random.randint(0, 2, size=n)  # binary secret key
    e = np.random.normal(0, sigma, n)     # error polynomial (real-valued noise)
    a = np.random.randint(0, q, size=n)     # uniformly random polynomial
    
    pk0 = poly_mod(-a * sk + e, q, n)
    pk1 = a.copy()

    return {
        "n": n,
        "q": q,
        "scale": scale,   # scaling factor for message encoding
        "sigma": sigma,
        "sk": sk,
        "pk": (pk0, pk1),
        "seed": seed
    }

def encrypt(params, m):
    """
    Encrypts a real-valued message vector m.
    The message is first encoded by multiplying by the scale factor.
    """
    n, q, scale, sigma = params['n'], params['q'], params['scale'], params['sigma']
    pk0, pk1 = params['pk']
    
    # Encode message: scale the message (which may be a vector of floats)
    m_poly = np.zeros(n, dtype=float)
    m_poly[:len(m)] = np.array(m) * scale

    u = np.random.randint(0, 2, size=n)  # small binary polynomial
    e1 = np.random.normal(0, sigma, n)
    e2 = np.random.normal(0, sigma, n)

    # The ciphertext components: note that we add m_poly (already scaled) into c0.
    c0 = poly_mod(pk0 * u + e1 + m_poly, q, n)
    c1 = poly_mod(pk1 * u + e2, q, n)

    return (c0, c1)

def decrypt(params, ciphertext):
    """
    Decrypts the ciphertext to recover an approximation of the original real-valued message.
    The result is then decoded by dividing by the scale factor.
    """
    n, q, scale = params['n'], params['q'], params['scale']
    sk = params['sk']
    c0, c1 = ciphertext

    m_poly = poly_mod(c0 + c1 * sk, q, n)
    # Decode by dividing out the scale factor.
    m_decoded = m_poly / scale
    return m_decoded[:n]

