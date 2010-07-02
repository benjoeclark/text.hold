#include "hold.h"
#include "game.h"
#include <string>
#include <iostream>
using namespace std;

Game::Game(Hold* initialHold)
{
    hold = initialHold;
}

string Game::run()
{
    cout << hold->getString() << endl;
    return string("");
}
