#include "hold.h"
#include <string>
#include <list>
using namespace std;

Hold::Hold(char* hold_name)
{
    name = hold_name;
}

string Hold::get_string()
{
    return name;
}
