#include "hold.h"
#include "game.h"
#include <string>
#include <fstream>
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
    if (argc == 1)
    {
        cout << "Provide a hold name" << endl;
    }
    string name(argv[argc-1]);
    // get only the part of the string before the '.'
    // this ensures we are not creating a .hold.hold
    name = name.substr(0, name.rfind('.'));
    string hold_file_name(name + ".hold");
    string backup_file_name(name + ".bak");
    ifstream hold_file(hold_file_name.c_str());
    if (hold_file.is_open())
    {
        string hold_contents, line;
        ofstream backup_file(backup_file_name.c_str());
        // get hold contents and back them up
        while (!hold_file.eof())
        {
            getline(hold_file, line);
            backup_file << line + '\n';
            hold_contents += line + '\n';
        }
        hold_file.close();
        backup_file.close();
        // play the game
        Hold hold(hold_contents);
        Game game(&hold);
        game.run();
    }
    else
    {
        // hold does not already exist, create a new one
        ofstream new_file(hold_file_name.c_str());
        new_file << newHold();
        new_file.close();
    }
}
