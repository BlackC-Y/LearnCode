#include <iostream>   //�̶�ǰ׺

#include <string>   //ʹ��stringģ�飿

using namespace std;   //ʹ�������ռ�

int main()
{    
    int divisor, dividend, quotient, remainder;
 
    cout << "���뱻����: ";
    cin >> dividend;
 
    cout << "�������: ";
    cin >> divisor;
 
    quotient = dividend / divisor;
    remainder = dividend % divisor;
 
    cout << "�� = " << quotient << endl;
    cout << "���� = " << remainder;
 
    return 0;
}