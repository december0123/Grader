#include <iomanip>
#include <iostream>
#include <string>

long double fun(double x)
{
    return x * x;
}

long double integral(long double start, long double stop, long double num_of_steps)
{
    long double result = 0.0;
    long double step = (stop - start) / num_of_steps;
    for (auto i = 1.0; i <= num_of_steps; ++i)
    {
        result += fun(start + i * step);
    }
    return result * step;
}

int main(int argc, char* argv[])
{
    std::cout << integral(std::stold(argv[1]), std::stold(argv[2]), std::stold(argv[3]));
}
