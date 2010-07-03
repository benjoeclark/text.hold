#ifndef SHOP_H
#define SHOP_H
#include <string>
#include <list>

class Shop
{
public:
    Shop(std::string holdContents);
    std::string run();
private:
    int getCoinage();
    std::string hold;
};
#endif //SHOP_H
