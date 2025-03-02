import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error
from torchvision.datasets import CIFAR10
from torchvision import transforms

def load_and_preprocess_cifar10(t=37):
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.ToTensor()
    ])
    dataset = CIFAR10(root="./data", train=True, download=True, transform=transform)

    images = np.array([dataset[i][0].numpy().flatten() for i in range(len(dataset))])
    images = np.round(images * (t - 1)).astype(int)  # Scale [0,1] to [0,t-1]
    return images

def benchmark_algo_in_batches(encrypt, decrypt, params, images, algo_name):
    num_images = len(images)
    batch_size = 100
    num_batches = num_images // batch_size

    encrypt_times, decrypt_times, errors = [], [], []

    for batch_idx in range(num_batches):
        batch = images[batch_idx * batch_size : (batch_idx + 1) * batch_size]

        batch_encrypt_time = 0
        batch_decrypt_time = 0
        batch_errors = []

        for img in batch:
            start = time.time()
            ciphertext = encrypt(params, img)
            batch_encrypt_time += time.time() - start

            start = time.time()
            decrypted = decrypt(params, ciphertext)
            batch_decrypt_time += time.time() - start

            mse = mean_squared_error(img, decrypted[:len(img)])
            batch_errors.append(mse)

        encrypt_times.append(batch_encrypt_time / batch_size)
        decrypt_times.append(batch_decrypt_time / batch_size)
        errors.extend(batch_errors)

    return {
        "Algorithm": algo_name,
        "avg_encrypt_time_per_100": np.mean(encrypt_times),
        "avg_decrypt_time_per_100": np.mean(decrypt_times),
        "avg_mse": np.mean(errors)
    }

def plot_benchmark_results(df, algo_name):
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].barh(df["Parameter Variation"], df["avg_encrypt_time_per_100"])
    axs[0].set_title(f"{algo_name} - Avg Encrypt Time per 100 Images (s)")

    axs[1].barh(df["Parameter Variation"], df["avg_decrypt_time_per_100"])
    axs[1].set_title(f"{algo_name} - Avg Decrypt Time per 100 Images (s)")

    axs[2].barh(df["Parameter Variation"], df["avg_mse"])
    axs[2].set_title(f"{algo_name} - Avg MSE (Error)")

    for ax in axs:
        ax.grid(True)

    plt.tight_layout()
    plt.show()

