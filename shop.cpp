#include "shop.h"
#include <string>
#include <iostream>
using namespace std;

Shop::Shop(string holdContents)
{
    hold = holdContents;
}

string Shop::run()
{
    int coinage = getCoinage();
    bool finished = false;
    char c;
    while (!finished)
    {
        cout << "You have " << coinage << " coinage to spend" << endl;
        cout << "Enter a symbol for a description" << endl;
        cin >> c;
        bool validSelection = false;
        switch(c) {
            case 'k' :
                cout << "Kobold" << endl;
                validSelection = true;
                break;
        }
        if (validSelection) {
            cout << "Purchase?" << endl;
            cin >> c;
            if (c == 'y') {
                finished = true;
            }
        }
    }
    return string("");
}

int Shop::getCoinage()
{
    int coinage = 0;
    for (int i=0; i<hold.length(); i++)
    {
        if (hold[i] == '$')
        {
            coinage++;
            hold[i] = ' ';
        }
    }
    return coinage;
}
