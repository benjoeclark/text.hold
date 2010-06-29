#include <iostream>
#include <fstream>
#include <string>
#include "lib/hold.hpp"

using namespace std;

int main(int argc, char* argv[])
{
    ifstream hold_file;
    string hold_file_name(argv[argc-1]);
    string line;
    Hold hold;
    if (hold_file_name.rfind(".hold") == string::npos)
    {
        cout << "Invalid hold name" << endl;
        return 1;
    }
    hold_file.open(argv[argc-1]);
    if (hold_file.is_open())
    {
        while (! hold_file.eof())
        {
            getline(hold_file, line);
            hold.append_line(line);
            cout << line << endl;
        }
        hold_file.close();
    }
    cout << hold.get_string() << endl;
    return 0;
}
