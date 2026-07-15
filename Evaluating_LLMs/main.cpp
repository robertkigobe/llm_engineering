
#include <bits/stdc++.h>
using namespace std;

int main() {
    const long long iterations = 200'000'000;
    constexpr double param1 = 4.0, param2 = 1.0;

    auto start = chrono::high_resolution_clock::now();

    double result = 1.0;
#pragma omp simd
    for (long long i = 1; i <= iterations; ++i) {
        double j = double(i) * param1 - param2;
        result -= 1.0 / j;
        j   = double(i) * param1 + param2;
        result += 1.0 / j;
    }
    result *= 4.0;

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout.setf(ios::fixed);
    cout << "Result: " << setprecision(12) << result << '\n';
    cout << "Execution Time: " << setprecision(6) << elapsed.count() << " seconds\n";

    return 0;
}
