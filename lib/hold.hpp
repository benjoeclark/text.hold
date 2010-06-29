#include <string>
#include <list>

using namespace std;

class Hold
{
public:
    void append_line(string line)
    {
        data.push_back(line);
    }

    string get_string()
    {
        string output;
        list<string>::iterator data_it;
        for (data_it = data.begin(); data_it !=  data.end(); data_it++)
        {
            output += *data_it + '\n';
        }
        return output;
    };

private:
    list<string> data;
};
