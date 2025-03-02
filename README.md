# CSDS_356
Data Privacy Spring 2025

# Overview 
We are experimenting with training datasets that are homomorphic encrypted. We are testing on various types of datasets and encryption algorithms.

# Types of data sets
- Tabular Data
    - UCI Adult Income Dataset (Income prediction)
    - Breast Cancer Wisconsin Dataset (Medical classification)
    - Diabetes Dataset (Numeric Regression)
- Image Data
    - MNIST (handwritten images)
    - CIFAR-10 (Object Recognition)
    - Fashion-MNIST (Clothing classification)
- Text Data
    - IMDB Movie Reviews (sentiment analysis)
    - AG News Dataset
- Time series Data 
    - Stock Market Data (Yahoo Finance)
    - COVID-19 Time Series Data

# Homomorphic Encryption Algorithms

## Partial Homomorphic Encryption (PHE)
These schemes support only one type of operation (either addition or multiplication).

- **RSA**  
  Supports multiplicative homomorphism.  
  Primarily used for digital signatures and secure communications, but supports limited homomorphic multiplication.

- **Paillier Encryption**  
  Supports additive homomorphism.  
  Enables the addition of plaintexts by performing operations on the ciphertexts.

- **ElGamal Encryption**  
  Supports multiplicative homomorphism.  
  Used in cryptographic applications where multiplicative homomorphism is beneficial.

- **Goldwasser–Micali**  
  Homomorphic with respect to XOR operations (for bit-level encryption).  
  An early probabilistic encryption scheme with limited homomorphic properties.

---

## Somewhat Homomorphic Encryption (SWHE)
SWHE schemes allow both addition and multiplication but can only support a limited number of operations before noise accumulation forces decryption.

- **Boneh-Goh-Nissim (BGN) Scheme**  
  Supports unlimited additions and one multiplication.  
  A classic example demonstrating the trade-off between functionality and noise growth.

- **DGHV Scheme (van Dijk–Gentry–Halevi–Vaikuntanathan)**  
  Integer-based encryption supporting a limited number of operations.  
  Demonstrates SWHE in a simple mathematical setting.

- **Smart–Vercauteren Scheme**  
  Supports a bounded number of both additions and multiplications before requiring decryption.  
  An early scheme leading to fully homomorphic encryption research.

- **Leveled (Unbootstrapped) Variants of FHE Schemes**  
  Many modern FHE schemes (like BFV, BGV, CKKS) can function as SWHE when used without bootstrapping.  
  These schemes support a predefined computation depth before noise accumulation becomes too high.

---

## Fully Homomorphic Encryption (FHE)
FHE schemes support arbitrary computations on encrypted data, though they tend to be computationally intensive due to noise management requirements.

- **Gentry’s Original FHE Scheme**  
  The first fully homomorphic encryption scheme using bootstrapping.  
  Introduced the concept of arbitrary computations on encrypted data.

- **BFV (Brakerski/Fan-Vercauteren)**  
  Efficient FHE for integer arithmetic.  
  Widely implemented in libraries like Microsoft SEAL.

- **BGV (Brakerski-Gentry-Vaikuntanathan)**  
  Lattice-based FHE scheme with flexible noise management.  
  Used in HElib, balancing efficiency and functionality.

- **CKKS (Cheon-Kim-Kim-Song)**  
  Supports approximate arithmetic on real numbers, ideal for machine learning.  
  Enables efficient encrypted computations with some approximation error.

- **TFHE (Fast FHE with Boolean gates)**  
  Optimized for Boolean circuit evaluations.  
  Well-suited for applications requiring rapid binary operations.

- **FHEW (Fast Homomorphic Encryption over the Torus)**  
  Optimized for fast bootstrapping in Boolean circuits.  
  Reduces the overhead associated with bootstrapping.

- **HEAAN**  
  Designed for approximate homomorphic encryption (similar to CKKS).  
  Useful in applications where slight approximation errors are acceptable.

- **LTV (Lopez-Alt, Tromer, Vaikuntanathan)**  
  An FHE variant refining lattice-based approaches.  
  A step toward practical FHE solutions.

---

## Summary

- **PHE algorithms** (e.g., Paillier, RSA) provide single-operation homomorphism.
- **SWHE algorithms** (e.g., BGN, DGHV, Smart–Vercauteren, and leveled variants of BFV/BGV/CKKS) support both addition and multiplication but are limited in depth.
- **FHE algorithms** (e.g., Gentry’s scheme, BFV, BGV, CKKS, TFHE, FHEW, HEAAN, LTV) allow arbitrary computations on encrypted data with bootstrapping or noise-management techniques.

This list covers many of the core schemes that have shaped homomorphic encryption research, though new optimizations and implementations continue to emerge.
