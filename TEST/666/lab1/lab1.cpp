#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    if (argc < 1)
    {
        return -1;
    }
    std::cout << argv[1];
}
