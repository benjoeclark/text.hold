#ifndef GAME_H
#define GAME_H
#include "hold.h"
#include <string>
#include <list>

class Game
{
public:
    Game(Hold* initial_hold);
    void run();
private:
    Hold* hold;
};
#endif //GAME_H
