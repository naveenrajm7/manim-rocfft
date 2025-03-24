#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include "hip/hip_runtime_api.h"
#include "hip/hip_vector_types.h"
#include "rocfft/rocfft.h"

// Function to read input data from a CSV file
std::vector<float2> readCSV(const std::string& filename, size_t& N) {
    std::vector<float2> data;
    std::ifstream file(filename);
    std::string line;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        float2 point;
        char comma;
        ss >> point.x >> comma >> point.y;
        data.push_back(point);
    }

    N = data.size();
    return data;
}

// Function to write output data to a CSV file
void writeCSV(const std::string& filename, const std::vector<float2>& data) {
    std::ofstream file(filename);
    for (const auto& point : data) {
        file << point.x << "," << point.y << "\n";
    }
}

int main()
{
    // rocFFT gpu compute
    // ========================================
    std::cout << "rocFFT gpu compute start" << std::endl;
    rocfft_setup();

    size_t N;
    std::vector<float2> cx = readCSV("input.csv", N);
    size_t Nbytes = N * sizeof(float2);

    // Create HIP device buffer
    float2 *x;
    hipMalloc(&x, Nbytes);

    // Print the input data
    // std::cout << "Input data:" << std::endl;
    // for (size_t i = 0; i < N; i++)
    // {
    //     std::cout << cx[i].x << ", " << cx[i].y << std::endl;
    // }

    // Copy data to device
    hipMemcpy(x, cx.data(), Nbytes, hipMemcpyHostToDevice);

    // Create rocFFT plan
    rocfft_plan plan = nullptr;
    size_t length = N;
    rocfft_plan_create(&plan, rocfft_placement_inplace,
         rocfft_transform_type_complex_forward, rocfft_precision_single,
         1, &length, 1, nullptr);

    // Check if the plan requires a work buffer
    size_t work_buf_size = 0;
    rocfft_plan_get_work_buffer_size(plan, &work_buf_size);
    void* work_buf = nullptr;
    rocfft_execution_info info = nullptr;
    if(work_buf_size)
    {
        rocfft_execution_info_create(&info);
        hipMalloc(&work_buf, work_buf_size);
        rocfft_execution_info_set_work_buffer(info, work_buf, work_buf_size);
    }

    // Execute plan
    rocfft_execute(plan, (void**) &x, nullptr, info);

    // Wait for execution to finish
    hipDeviceSynchronize();

    // Clean up work buffer
    if(work_buf_size)
    {
        hipFree(work_buf);
        rocfft_execution_info_destroy(info);
    }

    // Destroy plan
    rocfft_plan_destroy(plan);

    // Copy result back to host
    std::vector<float2> y(N);
    hipMemcpy(y.data(), x, Nbytes, hipMemcpyDeviceToHost);

    // Calculate dt
    float dt = 1.0f / static_cast<float>(N);

    // Scale the output by dt
    for (size_t i = 0; i < N; i++)
    {
        y[i].x *= dt;
        y[i].y *= dt;
    }

    // // Print results
    // std::cout << "Output data:" << std::endl;
    // for (size_t i = 0; i < N; i++)
    // {
    //     std::cout << y[i].x << ", " << y[i].y << std::endl;
    // }

    // Write output data to CSV file
    writeCSV("output.csv", y);

    // Free device buffer
    hipFree(x);

    rocfft_cleanup();

    std::cout << "rocFFT gpu compute end" << std::endl;
    return 0;
}
