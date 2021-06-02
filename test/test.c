#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <netinet/in.h>

int main()
{
   int x = 1000;
   int a = htons(x);
   printf("converted to network byte order: %d", a);
   int t = ntohs(a);
   printf("converted back: %d",t);

}