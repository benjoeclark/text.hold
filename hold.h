#ifndef HOLD_H
#define HOLD_H
#include <string>
#include <list>

class Hold
{
public:
    Hold(char* hold_name);
private:
    std::string name;
    std::list<std::string> map;
};
#endif //HOLD_H
