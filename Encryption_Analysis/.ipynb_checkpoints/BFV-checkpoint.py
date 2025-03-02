import numpy as np

def poly_mod(x, mod, n):
    """Reduces polynomial x modulo (x^n + 1) and coefficient-wise modulo mod"""
    x = np.array(x)[:n]
    for i in range(n, len(x)):
        x[i - n] -= x[i]  # x^n ≡ -1, so x^n + 1 = 0
    return np.remainder(x, mod)

def generate_keys(n, q, t, sigma, seed=None):
    if seed is not None:
        np.random.seed(seed)
        
    sk = np.random.randint(0, 2, size=n)
    e = np.random.normal(0, sigma, n).astype(int)
    a = np.random.randint(0, q, size=n)

    pk0 = poly_mod(-a * sk + e, q, n)
    pk1 = a.copy()

    return {
        "n": n,
        "q": q,
        "t": t,
        "sigma": sigma,
        "sk": sk,
        "pk": (pk0, pk1),
        "seed": seed
    }

def encrypt(params, m):
    n, q, t, sigma = params['n'], params['q'], params['t'], params['sigma']
    pk0, pk1 = params['pk']

    m_poly = np.zeros(n, dtype=int)
    m_poly[:len(m)] = m

    u = np.random.randint(0, 2, size=n)
    e1 = np.random.normal(0, sigma, n).astype(int)
    e2 = np.random.normal(0, sigma, n).astype(int)

    c0 = poly_mod(pk0 * u + e1 + (t * m_poly), q, n)
    c1 = poly_mod(pk1 * u + e2, q, n)

    return (c0, c1)

def decrypt(params, ciphertext):
    n, q, t = params['n'], params['q'], params['t']
    sk = params['sk']
    c0, c1 = ciphertext

    m_poly = poly_mod(c0 + c1 * sk, q, n)
    m_poly = np.round(m_poly * (t / q)).astype(int)

    return np.remainder(m_poly, t)[:n]
