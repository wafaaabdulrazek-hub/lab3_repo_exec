double calculateTax(double price, std::string country) {
    if (country == "EG") {
        return price * 0.14;
    }
    return 0.0;

}