#include <iostream> 
#include <cstdlib>  
using namespace std;
                                        
int main()
{
	int *intptr = new int(50);
 	//宣告一指向整數的指標,在該記憶體中存入整數值50
 	float *floatptr = new float;
 	//宣告一指向浮點數的指標,但未指定記憶體中儲存的資料值
 	cout << "intptr 指向的資料值：" << *intptr << "\n\n";
 	*floatptr = 0.5;
 	cout << "floatptr 指向的資料值：" << *floatptr << "\n\n";

	delete intptr;
	delete floatptr;
  
  	return 0;
}
