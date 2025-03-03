import pandas as pd
from benchmark_helper import load_and_preprocess_cifar10, benchmark_algo_in_batches, plot_benchmark_results
from tfhe import generate_keys, encrypt, decrypt

def run_tfhe_benchmark():
    t = 37  # Maximum pixel value
    images = load_and_preprocess_cifar10(t=t)

    base_params = {
        "n": 500,        # Secret key size (TFHE uses binary keys)
        "std_dev": 0.001,  # Gaussian noise standard deviation
        "t": t           # Maximum pixel value
    }

    variations = {
        "n": [400, 600],               # Different secret key sizes
        "std_dev": [0.0005, 0.002],     # Different noise levels
    }

    results = []

    # Generate base TFHE keys
    params = generate_keys(**base_params)
    result = benchmark_algo_in_batches(encrypt, decrypt, params, images, "TFHE")
    result["Parameter Variation"] = "standard"
    results.append(result)

    # Iterate through parameter variations
    for param, values in variations.items():
        for value in values:
            varied_params = base_params.copy()
            varied_params[param] = value
            params = generate_keys(**varied_params)

            result = benchmark_algo_in_batches(encrypt, decrypt, params, images, "TFHE")
            result["Parameter Variation"] = f"{param}={value}"
            results.append(result)

    df = pd.DataFrame(results)
    print("TFHE Benchmark Results:")
    print(df)

    plot_benchmark_results(df, "TFHE")