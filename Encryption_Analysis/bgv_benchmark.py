import pandas as pd
from benchmark_helper_parameters import load_and_preprocess_cifar10, benchmark_algo_in_batches, plot_benchmark_results
from bfv import generate_keys, encrypt, decrypt 

def run_bgv_benchmark():
    # Use integer messages as in BFV.
    _, images_bgv = load_and_preprocess_cifar10(t=37)
    base_params = {"n": 2048, "q": 65537, "t": 37, "sigma": 3.2}
    variations = {
        "n": [1024, 4096],
        "q": [32768, 131072],
        "t": [17, 61],
        "sigma": [2.0, 5.0]
    }
    results = []
    params = generate_keys(**base_params)
    result = benchmark_algo_in_batches(encrypt, decrypt, params, images_bgv, "BGV")
    result["Parameter Variation"] = "standard"
    results.append(result)
    for param, values in variations.items():
        for value in values:
            varied_params = base_params.copy()
            varied_params[param] = value
            params = generate_keys(**varied_params)
            result = benchmark_algo_in_batches(encrypt, decrypt, params, images_bgv, "BGV")
            result["Parameter Variation"] = f"{param}={value}"
            results.append(result)
    df = pd.DataFrame(results)
    print("BGV Benchmark Results:")
    print(df)
    plot_benchmark_results(df, "BGV")