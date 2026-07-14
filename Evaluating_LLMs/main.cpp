
#include <iostream>
#include <vector>
#include <thread>
#include <numeric>
#include <chrono>
#include <iomanip>

// Calculates a partial sum for a sub-range of the total iterations.
// This function uses a mathematically simplified formula for performance.
// The original update per iteration is: result += 1/(4*i+1) - 1/(4*i-1)
// This simplifies to: result -= 2 / (16*i^2 - 1)
// This version is faster due to fewer divisions and is also more numerically stable.
double calculate_partial(long long start_i, long long end_i) {
    double partial_sum = 0.0;
    for (long long i = start_i; i < end_i; ++i) {
        double i_d = static_cast<double>(i);
        partial_sum -= 2.0 / (16.0 * i_d * i_d - 1.0);
    }
    return partial_sum;
}

int main() {
    // Fast I/O
    std::ios_base::sync_with_stdio(false);

    const long long iterations = 200'000'000;

    auto start_time = std::chrono::high_resolution_clock::now();

    // Determine the number of threads to use, fallback to 1 if undetectable
    unsigned int num_threads = std::thread::hardware_concurrency();
    if (num_threads == 0) {
        num_threads = 1;
    }

    std::vector<std::thread> threads;
    std::vector<double> partial_results(num_threads);
    
    // Distribute the total iterations evenly among the threads
    const long long N = iterations;
    const unsigned int P = num_threads;
    
    for (unsigned int i = 0; i < P; ++i) {
        long long start_i = 1 + (i * N) / P;
        long long end_i = 1 + ((i + 1) * N) / P;
        
        // Launch a thread only if there is work to do for this range
        if (start_i < end_i) {
             threads.emplace_back([i, start_i, end_i, &partial_results] {
                partial_results[i] = calculate_partial(start_i, end_i);
            });
        }
        // Note: if a thread gets no work, its partial_results element remains 0.0
    }

    // Wait for all worker threads to complete
    for (auto& t : threads) {
        t.join();
    }
    
    // Aggregate results from all threads.
    // The series starts with 1.0, to which we add all partial sums.
    double result = std::accumulate(partial_results.begin(), partial_results.end(), 1.0);

    result *= 4.0;

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end_time - start_time;

    // Print the final result and execution time, matching the Python script's format
    std::cout << "Result: " << std::fixed << std::setprecision(12) << result << std::endl;
    std::cout << "Execution Time: " << std::fixed << std::setprecision(6) << duration.count() << " seconds" << std::endl;

    return 0;
}
