# Fourier Drawing with AMD GPU using rocFFT

> Fork of [Flundrahn/manim-fourier-project](https://github.com/Flundrahn/manim-fourier-project), where the animation is done using Manim, but the Fourier transform computation is replaced with a custom HIP program utilizing AMD ROCm's rocFFT library to run on AMD GPUs.

This project demonstrates the usage of the ROCm rocFFT library to compute Fourier transform. It is done in a fun way by calculating the Fourier transform of the AMD logo, which is then used in Manim for animation. Each Fourier transform is used to draw epicycles, creating a reveal video of the AMD logo. 

### Setup ROCm

1. Launch AWS G4ad instance with 100 GB of root volume
2. Use [setup script](aws-setup.sh)
3. Get [rocm_sdk_builder](https://github.com/lamikr/rocm_sdk_builder) docker container for rdna1_rdna2

```bash
# have 100 GB of disk to pull docker image
# get rocm for rdna1 
sudo docker pull lamikr/rocm_sdk_builder:612_01_rdna1_rdna2

# start
sudo docker run -it --device=/dev/kfd --device=/dev/dri --group-add video docker.io/lamikr/rocm_sdk_builder:612_01_rdna1_rdna2 bash
```

### Setup Manim

```bash
pip install manim
```

### Compile ROCm fft  

```bash
hipcc fft.cpp -o fft -L/opt/rocm_sdk_612/rocfft/lib64 -lrocfft -mprintf-kind=buffered
```

### Run manim 

```bash
# -pqh = High quality , -pql = Low quality  
manim -pqh main.py FourierScene
```


## Credits

* Inspiration - [3Blue1Brown](https://www.youtube.com/watch?v=r6sGWTCMz2k)
* Manim animation scripts - [Flundrahn/manim-fourier-project](https://github.com/Flundrahn/manim-fourier-project)
* rocFFT - [ROCm Documentation](https://rocm.docs.amd.com/projects/rocFFT/en/latest/how-to/working-with-rocfft.html)
* ROCm - [rocm_sdk_builder](https://github.com/lamikr/rocm_sdk_builder)
