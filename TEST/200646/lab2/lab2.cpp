#include <iostream>
#include <regex>
#include <string>

int main(int argc, char* argv[])
{
    if (argc < 4)
    {
        std::cerr << "Za mala liczba argumentow.\nUzycie: lab2 NAPIS_DO_ZMIANY ZESTAW_ZNAKOW NA_CO_ZMIENIC" << std::endl;
        return -1;
    }
    std::string input{argv[1]};

    std::string change_from{argv[2]};

    std::string change_to{argv[3]};

    std::regex r("["+change_from+"]");
    std::cout << std::regex_replace(input, r, change_to);
}
