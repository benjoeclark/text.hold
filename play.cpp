#include "hold.h"
#include "game.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
    if (argc == 1)
    {
        cout << "Provide a hold name" << endl;
    }
    Hold hold(argv[argc-1]);
    Game game(&hold);
    game.run();
}
