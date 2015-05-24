#include <iomanip>
#include <iostream>
#include <string>

long double fun(double x)
{
    return x * x;
}

long double integral(double start, double stop, double step)
{
    long double result = 0.0;
    for (auto i = start; i <= stop; i += step)
    {
        result += fun(i);
    }
    return result;
}

int main(int argc, char* argv[])
{
    std::cout << integral(std::stold(argv[1]), std::stold(argv[2]), std::stold(argv[3]));
}
