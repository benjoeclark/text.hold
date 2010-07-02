#include "hold.h"
#include <string>
#include <list>
using namespace std;

Hold::Hold(string holdContents)
{
    name = holdContents;
}

string Hold::getString()
{
    return name;
}

string newHold(int width, int height)
{
    string contents;
    for (int row=0; row<height; row++)
    {
        for (int col=0; col<width; col++)
        {
            contents += '#';
        }
        contents += '\n';
    }
    contents += "\n$\n";
    return contents;
}
