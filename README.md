# Performance Benchmarking of Cryptographic Mechanisms

This project provides a comprehensive performance analysis of various cryptographic algorithms, including symmetric encryption (**AES**), asymmetric encryption (**RSA**), and hashing functions (**SHA-256**). 

The primary goal is to evaluate how execution time scales with file size (from 8 bytes to 2MB) and to compare the computational overhead of different security approaches.

## Features

**AES-256 (CTR Mode):** Benchmarking of symmetric encryption and decryption.
**Custom RSA Implementation:** Hybrid-style encryption using RSA for randomness and SHA-256 for block generation (XOR-based).
**SHA-256 Hashing:** Performance measurement of message digest generation.
**Statistical Analysis:** All tests include 30+ iterations to ensure statistically significant results (mean and standard deviation).
**Data Visualization:** Automated generation of log-scale plots for clear performance comparison.

## Tech Stack

**Language:** Python 3.x
**Libraries:** 
    * `cryptography` (Primitive algorithms)
    * `hashlib` (Hashing)
    * `matplotlib` (Data visualization)
    * `timeit` / `time` (High-precision benchmarking)

## Project Structure

'ParteA.py`: Utility to generate random test files of varying sizes.
`ParteB.py`: AES-256 CTR implementation and benchmarking.
`ParteC.py`: RSA-based encryption and decryption logic.
`ParteD.py`: SHA-256 performance measurement.
`plots.py`: Main script to execute all benchmarks and generate comparative graphs.

## Key Findings

From our benchmarks (detailed in the report):
1.  **AES-256** remains the most efficient choice for large-scale data confidentiality.
2.  **SHA-256** shows the fastest execution times, as it lacks the overhead of key management.
3.  **RSA** exhibits significant computational cost, particularly during decryption, highlighting its practical limitation to small data chunks or key wrapping.

## How to Run

Install dependencies: pip install cryptography matplotlib

Generate test files: python ParteA.py

Run benchmarks and generate plots: python plots.py
