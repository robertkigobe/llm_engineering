
#include <cstdio>
#include <chrono>

int main() {
    constexpr int iterations = 200'000'000;
    constexpr double param1 = 4.0, param2 = 1.0;
    double result = 1.0;

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 1; i <= iterations; ++i) {
        double j = i * param1 - param2;
        result -= 1.0 / j;
        j = i * param1 + param2;
        result += 1.0 / j;
    }

    result *= 4.0;

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff = end - start;

    std::printf("Result: %.12f\n", result);
    std::printf("Execution Time: %.6f seconds\n", diff.count());

    return 0;
}
