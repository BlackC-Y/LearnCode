#include <iostream>
int main()

{   //p10
	int sum = 0, val = 1;
	//val小于10 while持续循环
	while (val <= 10)
	{
		sum += val;
		++val;
	}
	std::cout << "结果:" << sum << std::endl;
	return 0;
}