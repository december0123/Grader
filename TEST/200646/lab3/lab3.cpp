#include <iomanip>
#include <iostream>
#include <string>
#include <sstream>

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        std::cout << "ZOPA" << std::endl;
        return -1;
    }
    std::stringstream ss;
    ss << std::hex << argv[1];
    unsigned long long a;
    ss >> a;
    ss.str(std::string());
    ss.clear();
    ss << std::hex << argv[2];
    unsigned long long b;
    ss >> b;
    ss.str(std::string());
    ss.clear();
    unsigned long long c = a + b;
    std::cout << "0x" << std::hex << c;
}
