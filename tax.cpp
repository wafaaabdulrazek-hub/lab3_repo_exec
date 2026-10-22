#include <iostream>
#include <string>

double calculateTax(double price, std::string country) {
    if (country == "EG") {
        return price * 0.14;
    }
    return 0.0;
}

int main() {
    std::cout << calculateTax(100, "EG") << std::endl;
    std::cout << calculateTax(100, "US") << std::endl;
    return 0;
}