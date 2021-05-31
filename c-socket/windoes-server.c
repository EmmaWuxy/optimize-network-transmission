// add -lwsock32 at the end when compile
/*
    Bind socket to port 8888 on localhost
*/
#include<io.h>
#include<stdio.h>
#include<stdlib.h>i:
#include<winsock2.h>
 
#pragma comment(lib,"ws2_32.lib") //Winsock Library
 
int main(int argc , char *argv[])
{
    WSADATA wsa;
    SOCKET s , new_socket;
    struct sockaddr_in server , client;
    int c;
    int size_of_data = 1000000000;
    
    // Arrange data
    char data_pre[1000] = {0};
    char* data;
    data = (char*)malloc(size_of_data); 

    if (data == NULL) {
        printf("Memory not allocated.\n");
        exit(0);
    }

    for(int i = 0; i < size_of_data; i++){ 
        data[i] = 49;                           // assign random integers to the allocated memory
    }
 
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
 
    printf("Socket created.\n");
     
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    //server.sin_addr.s_addr = INADDR_ANY; bind() of INADDR_ANY binds the socket to all available interface
	server.sin_addr.s_addr = inet_addr("127.0.0.1"); //localhost
    server.sin_port = htons( 8888 );
     
    //Bind
    if( bind(s ,(struct sockaddr *)&server , sizeof(server)) == SOCKET_ERROR)
    {
        printf("Bind failed with error code : %d" , WSAGetLastError());
    }
     
    puts("Bind done");
 
    //Listen to incoming connections
    listen(s , 3);
     
    //Accept an incoming connection
    puts("Waiting for incoming connections...");
     
    c = sizeof(struct sockaddr_in);
    new_socket = accept(s , (struct sockaddr *)&client, &c);
    if (new_socket == INVALID_SOCKET)
    {
        printf("accept failed with error code : %d" , WSAGetLastError());
    }
     
    puts("Connection accepted");

    //Reply to client: send a small data packet to reduce the influence of overhead
    send(new_socket, data_pre, sizeof(data_pre), 0);
    puts("Successfully sent the small packet");
 
    //Reply to client: send large chunck of data

    while (size_of_data>0)
    {
        int sendSize= send(new_socket, data, size_of_data, 0);
        if(SOCKET_ERROR==sendSize){
            printf("recv failed with error code : %d" , WSAGetLastError());
        }
            
        size_of_data = size_of_data - sendSize; // for cyclic send and exit function
        data += sendSize;// is used to calculate the offset of the sent buffer
    }

    puts("Successfully sent all the data\n");


    // Socket close and free allocated memory
    closesocket(new_socket);
    closesocket(s);
    WSACleanup();
    free(data);
     
    return 0;
}