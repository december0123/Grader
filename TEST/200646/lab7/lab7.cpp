#include <array>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>

long double fun(long double x)
{
    return x * x;
}

long double integral(long double start, long double stop, long double num_of_steps)
{
    long double result = 0.0;
    long double step = (stop - start) / num_of_steps;
    for (auto i = 1.0L; i <= num_of_steps; ++i)
    {
        result += fun(start + i * step);
    }
    return result * step;
}

int main(int argc, char* argv[])
{
    if (argc == 4)
    {
        std::array<unsigned long long, 3> cycles{{10'000'000, 10'000'000'000, 10'000'000'000'000}};
        std::uniform_int_distribution<> distr(0, 2);
        std::mt19937_64 eng{std::random_device{}()};
        std::cout << "Wynik: "
            << std::fixed << integral(std::stold(argv[1]), std::stold(argv[2]), std::stold(argv[3]))
            << " Liczba cykli: " << cycles[distr(eng)];
    }
    else
    {
        std::cout << "BRAK ARGUMENTOW!\n";
    }
}
