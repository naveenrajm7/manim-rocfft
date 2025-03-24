import numpy as np
import csv

# Mathematical constants
PI = np.pi
"""The ratio of the circumference of a circle to its diameter."""

TAU = 2 * PI
"""The ratio of the circumference of a circle to its radius."""



def write_complex_points_to_csv(complex_points, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for c_point in complex_points:
            csvwriter.writerow([c_point.real, c_point.imag])

def read_transformed_points_from_csv(filename, freqs, n_samples):
    coefficients = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            real, imag = float(row[0]), float(row[1])
            coefficients.append(complex(real, imag))

    # Map frequencies to indices
    freq_to_index = {freq: (freq + n_samples) % n_samples for freq in freqs}

    # Extract the coefficients corresponding to the specified frequencies
    extracted_coefficients = [coefficients[freq_to_index[freq]] for freq in freqs]

    print("Extracted Fourier Coefficients:")
    for i, coef in enumerate(extracted_coefficients):
        print(i, coef)

    return extracted_coefficients


def dft_cpu(complex_points, freqs, dt):
    coefficients = []
    for freq in freqs:
        coef_sum = 0
        for t, c_point in enumerate(complex_points):
            coef_sum += c_point * np.exp(-TAU * 1j * freq * t * dt)
        coefficients.append(coef_sum * dt)
    return coefficients


def dft_gpu(complex_points, freqs, path_n_samples):
    # Write complex points to CSV
    write_complex_points_to_csv(complex_points, 'input.csv')

    # Run the C++ program to compute the Fourier transform using rocFFT
    import subprocess
    subprocess.run(["./fft"])

    # Read the transformed points from the output CSV
    coefficients = read_transformed_points_from_csv('output.csv', freqs, path_n_samples)

    return coefficients

def get_fourier_coefs(path, path_n_samples, freqs, use_gpu=False):
    dt = 1 / path_n_samples
    t_range = np.arange(0, 1, dt)

    points = np.array([
        path.point_from_proportion(t)
        for t in t_range
    ])

    # # Print the points
    # print("Points:")
    # for i, point in enumerate(points):
    #     print(i, point)

    complex_points = points[:, 0] + 1j * points[:, 1]

    # print("Complex Points:")
    # for i, c_point in enumerate(complex_points):
    #     print(i, c_point)

    if use_gpu:
        coefficients = dft_gpu(complex_points, freqs, path_n_samples)
    else:
        coefficients = dft_cpu(complex_points, freqs, dt)

    # print("Fourier Coefficients:")
    # for i, coef in enumerate(coefficients):
    #     print(i, coef)

    return coefficients