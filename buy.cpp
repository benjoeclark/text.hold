#include "shop.h"
#include "hold.h"
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
        // start the shop
        cout << "started the shop" << endl;
        Shop shop(hold_contents);
        cout << "contents " << hold_contents.length() << hold_contents << endl;
        hold_contents = shop.run();
        cout << "contents " << hold_contents.length() << hold_contents << endl;
        if (hold_contents.length() > 0)
        {
            ofstream hold_file(hold_file_name.c_str());
            hold_file << hold_contents;
            hold_file.close();
        }
    }
    else
    {
        // hold does not already exist, create a new one
        cout << "Hold does not exist" << endl;
    }
}
