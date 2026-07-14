
#include <iostream>
#include <iomanip>
#include <chrono>

// This function is a high-performance C++ implementation of the Python 'calculate' function.
// It uses an algebraic simplification to reduce the number of divisions per iteration from two to one.
// The loop is also unrolled by a factor of four to increase instruction-level parallelism.
// These optimizations are particularly effective with the -Ofast compiler flag, which allows
// re-associating floating-point operations.
double calculate(long long iterations, int param1, int param2) {
    const double p1 = static_cast<double>(param1);
    const double p2 = static_cast<double>(param2);
    
    const double neg_2_p2 = -2.0 * p2;
    const double p1_sq = p1 * p1;
    const double p2_sq = p2 * p2;

    double s1 = 0.0, s2 = 0.0, s3 = 0.0, s4 = 0.0;
    
    long long i = 1;
    const long long limit = iterations - 3;

    for (; i <= limit; i += 4) {
        double i1d = static_cast<double>(i);
        double i2d = i1d + 1.0;
        double i3d = i1d + 2.0;
        double i4d = i1d + 3.0;

        s1 += neg_2_p2 / (p1_sq * i1d * i1d - p2_sq);
        s2 += neg_2_p2 / (p1_sq * i2d * i2d - p2_sq);
        s3 += neg_2_p2 / (p1_sq * i3d * i3d - p2_sq);
        s4 += neg_2_p2 / (p1_sq * i4d * i4d - p2_sq);
    }
    
    double total_sum = s1 + s2 + s3 + s4;

    // Handle remaining iterations
    for (; i <= iterations; ++i) {
        double id = static_cast<double>(i);
        total_sum += neg_2_p2 / (p1_sq * id * id - p2_sq);
    }
    
    return 1.0 + total_sum;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    const long long iterations = 200'000'000;
    const int param1 = 4;
    const int param2 = 1;

    const auto start_time = std::chrono::high_resolution_clock::now();
    
    const double result = calculate(iterations, param1, param2) * 4.0;

    const auto end_time = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> diff = end_time - start_time;

    std::cout << "Result: " << std::fixed << std::setprecision(12) << result << '\n';
    std::cout << "Execution Time: " << std::fixed << std::setprecision(6) << diff.count() << " seconds" << '\n';
    
    return 0;
}
