#include <stdio.h>
#include <stdlib.h>
#include <time.h>
  
int main()
{
   char data_pre[1000] = {0};
   printf("size to send: %d", sizeof(data_pre));
   printf("the 100th element of the array: %d", data_pre[1000]);

}