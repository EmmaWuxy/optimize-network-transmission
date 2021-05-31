// add -lwsock32 at the end when compile
/*
    Bind socket to port 8888 on localhost
*/
#include<io.h>
#include<stdio.h>
#include<winsock2.h>
#include <time.h>
 
#pragma comment(lib,"ws2_32.lib") //Winsock Library
 
int main(int argc , char *argv[])
{
    WSADATA wsa;
    SOCKET s;
    struct sockaddr_in server;
	char* receive_buffer_pre;
	char* receive_buffer;
	int recv_size = 1000000000;
	double time_spent = 0.0;

	receive_buffer_pre = (char*)malloc(10000);
	receive_buffer = (char*)malloc(recv_size); 
 
	//Initialize Winsock
    printf("\nInitialising Winsock...");
    if (WSAStartup(MAKEWORD(2,2),&wsa) != 0) //If any error occurs then the WSAStartup function would return a non zero value and WSAGetLastError can be used to get more information about what error happened
    {
        printf("Failed. Error Code : %d",WSAGetLastError());
        return 1;
    }
     
    printf("Initialised.\n");
     
    //Create a socket
    if((s = socket(AF_INET , SOCK_STREAM , 0 )) == INVALID_SOCKET)
    {
        printf("Could not create socket : %d" , WSAGetLastError());
    }
 
    printf("Socket created.");

	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = inet_addr("127.0.0.1"); //localhost
	server.sin_port = htons( 8888 );

	//Connect to remote server
	if (connect(s , (struct sockaddr *)&server , sizeof(server)) < 0)
	{
		perror("connect error");
		return 1;
	}
	
	puts("Connected\n");

	//Receive a small packet from the server
	if((recv_size = recv(s, receive_buffer_pre, 10000 , 0)) == SOCKET_ERROR)
	{
		puts("recv failed");
	}
	
	puts("Small packet received\n");

	//Receive formal data from the server
	clock_t begin = clock();

	while (recv_size>0) // the remaining part is greater than 0
    {
        int size= recv(s, receive_buffer, recv_size , 0);
        if(SOCKET_ERROR==size){
            puts("recv failed");
		}
        recv_size = recv_size - size;
        receive_buffer += size;
    }

	puts("All data received\n");

	clock_t end = clock();
	time_spent += (double)(end - begin) / CLOCKS_PER_SEC;
	printf("The elapsed time is %f seconds", time_spent);

	//Close socket
	closesocket(s);
	WSACleanup();

	//Free memory
	free(receive_buffer_pre);
	free(receive_buffer);
}