#include <iostream>
int main()

{   //p10
	int sum = 0, val = 1;
	//valС��10 while����ѭ��
	while (val <= 10)
	{
		sum += val;
		++val;
	}
	std::cout << "���:" << sum << std::endl;
	return 0;
}