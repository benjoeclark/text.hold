#include "hold.h"
#include <string>
#include <list>
#include <iostream>
using namespace std;

Hold::Hold(string holdContents) {
    name = holdContents;
    width = holdContents.find_first_of('\n');
    height = 0;
    bool gettingMap = true;
    char lastChar = '\n';
    for (int i=0; i<holdContents.length(); i++) {
        if (holdContents[i] == '\n' && lastChar == '\n') {
            gettingMap = false;
        }
        if (gettingMap) {
            if (holdContents[i] == '\n') {
                height++;
            }
            else if (holdContents[i] == '#') {
                // a wall
            }
            else if (holdContents[i] == ' ') {
                // open space
            }
        }
        lastChar = holdContents[i];
    }
    cout << "width " << width << " height " << height << endl;
}

string Hold::getString() {
    return name;
}

string newHold(int width, int height) {
    string contents;
    for (int row=0; row<height; row++) {
        for (int col=0; col<width; col++) {
            contents += '#';
        }
        contents += '\n';
    }
    contents += "\n$\n";
    return contents;
}
