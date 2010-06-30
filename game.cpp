#include "hold.h"
#include "game.h"
#include <string>
#include <iostream>
using namespace std;

Game::Game(Hold* initial_hold)
{
    hold = initial_hold;
}

void Game::run()
{
    string command;
    cout << hold->get_string() << endl;
    cout << "#>";
    cin >> command;
}
