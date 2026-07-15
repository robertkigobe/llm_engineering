
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <iomanip>

// Worker function for each thread to compute a partial sum.
// The calculation is based on an optimized formula for the series:
// Original term for iteration i: 1/(4i+1) - 1/(4i-1)
// Optimized term: -2 / (16i^2 - 1)
// This optimization reduces two divisions to one per iteration.
void partial_sum_worker(const long long start_i, const long long end_i, double* result) {
    // Use four accumulators to break the dependency chain on a single sum variable.
    // This helps the compiler to better pipeline instructions and use SIMD (vectorization).
    double s0 = 0.0, s1 = 0.0, s2 = 0.0, s3 = 0.0;
    
    long long i = start_i;
    // Process 4 iterations at a time.
    for (; i <= end_i - 3; i += 4) {
        const double i0 = static_cast<double>(i);
        const double i1 = static_cast<double>(i + 1);
        const double i2 = static_cast<double>(i + 2);
        const double i3 = static_cast<double>(i + 3);
        s0 -= 2.0 / (16.0 * i0 * i0 - 1.0);
        s1 -= 2.0 / (16.0 * i1 * i1 - 1.0);
        s2 -= 2.0 / (16.0 * i2 * i2 - 1.0);
        s3 -= 2.0 / (16.0 * i3 * i3 - 1.0);
    }
    
    double local_sum = s0 + s1 + s2 + s3;
    
    // Handle remaining iterations that are not a multiple of 4.
    for (; i <= end_i; ++i) {
        const double di = static_cast<double>(i);
        local_sum -= 2.0 / (16.0 * di * di - 1.0);
    }
    
    *result = local_sum;
}


double calculate(const long long iterations) {
    // Use all available hardware threads for maximum parallelism.
    unsigned int num_threads = std::thread::hardware_concurrency();
    if (num_threads == 0) {
        num_threads = 1; // Fallback if hardware_concurrency is not supported.
    }

    std::vector<std::thread> threads;
    threads.reserve(num_threads);
    std::vector<double> partial_results(num_threads);

    const long long chunk_size = iterations / num_threads;
    long long start = 1;
    
    // Divide the total iterations into chunks for each thread.
    for (unsigned int i = 0; i < num_threads; ++i) {
        const long long end = (i == num_threads - 1) ? iterations : start + chunk_size - 1;
        threads.emplace_back(partial_sum_worker, start, end, &partial_results[i]);
        start = end + 1;
    }

    // Wait for all threads to complete their work.
    for (auto& t : threads) {
        t.join();
    }

    // Combine the partial results from all threads.
    double total_sum = 1.0;
    for (const double res : partial_results) {
        total_sum += res;
    }
    
    return total_sum;
}

int main() {
    // Fast I/O, though not critical for this specific program.
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    constexpr long long iterations = 200'000'000;
    
    const auto start_time = std::chrono::high_resolution_clock::now();
    
    // The Python code calculates an approximation of pi/4.
    // The final multiplication by 4 gives the approximation of pi.
    const double result = calculate(iterations) * 4.0;
    
    const auto end_time = std::chrono::high_resolution_clock::now();
    
    const std::chrono::duration<double> duration = end_time - start_time;
    
    std::cout << "Result: " << std::fixed << std::setprecision(12) << result << std::endl;
    std::cout << "Execution Time: " << std::fixed << std::setprecision(6) << duration.count() << " seconds" << std::endl;
    
    return 0;
}
