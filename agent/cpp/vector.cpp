// agent/cpp/vector.cpp
//
// Compile (Linux/macOS):
//   g++ -O3 -shared -std=c++17 -fPIC vector.cpp -o libvector.so
//
// On Windows (MSVC):
//   cl /LD /O2 vector.cpp /link /OUT:vector.dll
//
// ------------------------------------------------------------

#include <cmath>
#include <cstddef>

extern "C" {

/**
 * Compute cosine similarity between two double arrays.
 * @param vec1  Pointer to first vector
 * @param vec2  Pointer to second vector
 * @param n     Length of vectors
 * @return      Cosine similarity in range [-1, 1]
 */
double cosine_similarity(const double* vec1, const double* vec2, std::size_t n)
{
    double dot = 0.0;
    double mag1 = 0.0;
    double mag2 = 0.0;

    for (std::size_t i = 0; i < n; ++i)
    {
        dot  += vec1[i] * vec2[i];
        mag1 += vec1[i] * vec1[i];
        mag2 += vec2[i] * vec2[i];
    }

    double denom = std::sqrt(mag1) * std::sqrt(mag2);
    return (denom == 0.0) ? 0.0 : dot / denom;
}

} // extern "C"
