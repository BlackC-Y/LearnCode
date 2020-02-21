#include <iostream>
using namespace std;

int main()
{
    int currVal = 0, val = 0;
    if (cin>>currVal)
    {
        int cnt = 1;
        cout << currVal << endl;
        while (cin>>val)
        {
            if (val == currVal)
                ++cnt;
            else
            {
                cout << currVal << " chuxian " << cnt << "  ci" << endl;
                currVal = val;
                cnt = 1;
            }
        }
        cout << currVal << " chuxian " << cnt << " ci " << endl;
    }
    return 0;
}