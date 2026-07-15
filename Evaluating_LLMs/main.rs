use std::time::Instant;

// LCG struct implementing the generator
struct Lcg {
    value: u64,
    a: u64,
    c: u64,
    m: u64,
}

impl Lcg {
    #[inline(always)]
    fn new(seed: u64) -> Self {
        Lcg {
            value: seed,
            a: 1664525,
            c: 1013904223,
            m: 1u64 << 32,
        }
    }

    #[inline(always)]
    fn next(&mut self) -> u64 {
        // Perform the LCG calculation with wrapping arithmetic for u64 mod 2^32
        self.value = self
            .a
            .wrapping_mul(self.value)
            .wrapping_add(self.c) % self.m;
        self.value
    }
}

// Kadane's algorithm variant for maximum subarray sum
fn max_subarray_sum(n: usize, seed: u64, min_val: i64, max_val: i64) -> i64 {
    let range = (max_val - min_val + 1) as u64;

    // Generate the random numbers vector
    let mut lcg = Lcg::new(seed);
    let mut arr = Vec::with_capacity(n);
    for _ in 0..n {
        let val = (lcg.next() % range) as i64 + min_val;
        arr.push(val);
    }

    // O(n) Kadane's algorithm for max subarray sum
    let mut max_sum = i64::MIN;
    let mut current_sum = 0i64;

    for &v in arr.iter() {
        current_sum = current_sum.saturating_add(v);
        if current_sum > max_sum {
            max_sum = current_sum;
        }
        if current_sum < 0 {
            current_sum = 0;
        }
    }

    max_sum
}

fn total_max_subarray_sum(n: usize, initial_seed: u64, min_val: i64, max_val: i64) -> i64 {
    let mut total_sum = 0i64;
    let mut lcg = Lcg::new(initial_seed);

    for _ in 0..20 {
        let seed = lcg.next();
        total_sum += max_subarray_sum(n, seed, min_val, max_val);
    }

    total_sum
}

fn main() {
    let n = 10_000;
    let initial_seed = 42u64;
    let min_val = -10i64;
    let max_val = 10i64;

    let start = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let elapsed = start.elapsed();

    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", elapsed.as_secs_f64());
}