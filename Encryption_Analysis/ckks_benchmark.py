import pandas as pd
from benchmark_helper import load_and_preprocess_cifar10, benchmark_algo_in_batches, plot_benchmark_results
from ckks import generate_keys, encrypt, decrypt 


def run_ckks_benchmark():
    """
    Runs the CKKS benchmark using CIFAR-10 images.
    We benchmark the “standard” parameters as well as variations on parameters:
      - n: ring degree,
      - q: ciphertext modulus,
      - scale: encoding scaling factor,
      - sigma: noise standard deviation.
    """
    images = load_and_preprocess_cifar10()

    # Base parameters for our simplified CKKS scheme
    base_params = {
        "n": 2048,
        "q": 65537,
        "scale": 10000.0,  # scale factor for encoding messages
        "sigma": 3.2
    }

    # Parameter variations to see their impact on performance and accuracy.
    variations = {
        "n": [1024, 4096],
        "q": [32768, 131072],
        "scale": [5000.0, 20000.0],
        "sigma": [2.0, 5.0]
    }

    results = []

    # Benchmark with standard parameters.
    params = generate_keys(**base_params)
    result = benchmark_algo_in_batches(encrypt, decrypt, params, images, "CKKS")
    result["Parameter Variation"] = "standard"
    results.append(result)

    # Benchmark with variations.
    for param, values in variations.items():
        for value in values:
            varied_params = base_params.copy()
            varied_params[param] = value
            params = generate_keys(**varied_params)
            result = benchmark_algo_in_batches(encrypt, decrypt, params, images, "CKKS")
            result["Parameter Variation"] = f"{param}={value}"
            results.append(result)

    df = pd.DataFrame(results)
    print("CKKS Benchmark Results:")
    display(df)

    plot_benchmark_results(df, "CKKS")

# To run the benchmark, simply call:
# run_ckks_benchmark()