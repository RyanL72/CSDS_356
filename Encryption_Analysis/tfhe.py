import numpy as np

def generate_keys(n=500, std_dev=0.001, t=37, seed=None):
    """Generate TFHE secret and public keys."""
    if seed is not None:
        np.random.seed(seed)

    sk = np.random.randint(0, 2, size=n)  # Secret key is a binary vector
    a = np.random.uniform(-0.5, 0.5, size=n)  # Public key component (random torus values)
    e = np.random.normal(0, std_dev, size=n)  # Gaussian error

    b = (a * sk + e) % 1  # Modulo 1 since we're working over the torus

    return {
        "n": n,
        "std_dev": std_dev,
        "t": t,  # Add the t parameter
        "sk": sk,
        "pk": (a, b),
        "seed": seed
    }

def encrypt(params, m):
    """TFHE encryption: Encode integer pixel values as torus values, add noise, and use public key."""
    n, std_dev = params['n'], params['std_dev']
    a, b = params['pk']

    # Normalize pixel values to the torus [0, 1)
    m_torus = m / (2 * params['t'])  # Scale to [0, 0.5) to avoid overflow

    u = np.random.uniform(-0.5, 0.5, size=(len(m), n))  # Random masking values
    e = np.random.normal(0, std_dev, size=(len(m), n))  # Gaussian noise

    c0 = (b + e + m_torus[:, None]) % 1  # Encrypt each pixel separately
    c1 = (a + u) % 1  # Add masking randomness

    return (c0, c1)

def decrypt(params, ciphertext):
    """TFHE decryption: Compute inner product with secret key and extract messages."""
    sk = params['sk']
    c0, c1 = ciphertext

    # Compute decryption for all elements in the batch
    decrypted_torus = (c0 - np.sum(c1 * sk, axis=1, keepdims=True)) % 1  # Ensure correct broadcasting

    # Rescale back to integer pixel values
    decrypted_pixels = np.round(decrypted_torus * (2 * params['t'])).astype(int)

    # Clip values to ensure they are within [0, t-1]
    decrypted_pixels = np.clip(decrypted_pixels, 0, params['t'] - 1)

    return decrypted_pixels.flatten()