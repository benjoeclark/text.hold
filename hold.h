#ifndef HOLD_H
#define HOLD_H
#include <string>
#include <list>

class Hold
{
public:
    Hold(std::string holdContents);
    std::string getString();
private:
    std::string name;
    std::list<std::string> map;
};

std::string newHold(int width=10, int height=6);
#endif //HOLD_H
