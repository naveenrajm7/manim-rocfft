from manim import *
from fourier_transform import get_fourier_coefs

def test():
     # Define your own set of data points
    custom_points = [
        np.array([0, 0, 0]),
        np.array([1, 0, 0]),
        np.array([1, 1, 0]),
        np.array([0, 1, 0]),
        np.array([0, 0, 0])
    ]

    # Create a custom path using VMobject
    custom_path = VMobject()
    custom_path.set_points_as_corners(custom_points)

    # Log the Fourier coefficients
    n_samples = 5
    n_vectors = 4
    freqs = list(range(-n_vectors // 2, n_vectors // 2 + 1, 1))
    coefficients = get_fourier_coefs(custom_path, n_samples, freqs)

# To run this script, use the following command in the terminal:
# manim -pql test_fourierscene.py TestFourierScene
test()