#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char const *argv[])
{
    int s, new_socket, c;
    struct sockaddr_in server, client;
    int size_of_data = 100000;
    
    // Arrange data
    char data_pre[1000] = {0};
    char receive_buffer_pro[1000] = {0};
    char* data;
    data = (char*)malloc(size_of_data); 

    if (data == NULL) {
        printf("Memory not allocated.\n");
        return 1;
    }

    for(int i = 0; i < size_of_data; i++){ 
        data[i] = 49;                           // assign '1' to the allocated memory
    }

    //Create a socket
    s = socket(AF_INET , SOCK_STREAM , 0);
	if (s == -1)
	{
		printf("Could not create socket");
        return 1;
	}
    printf("Socket created.");

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("132.206.51.95"); // IP of mimi
	server.sin_port = htons( 8888 );

    //Bind
    bind(s, (struct sockaddr*)&server, sizeof(server)); 
    puts("Bind done");

    //Listen to incoming connection
    listen(s, 3); 

    //Accept an incoming connection
    puts("Waiting for incoming connections...");

    c = sizeof(struct sockaddr_in);
    new_socket = accept(s, (struct sockaddr *)&client, &c);
    if(new_socket < 0){
        perror("accept failed");
        return 1;
    }

    puts("Connection accepted");

    //Reply to client: send a small data packet to reduce the influence of overhead
    if( send(new_socket , data_pre , sizeof(data_pre) , 0) < 0)
    {
    	puts("Send small packet failed");
    	return 1;
    }
    puts("Successfully sent the small packet");

    //Reply to client: send large chunck of data
    while (size_of_data>0) // the remaining part is greater than 0
    {
        int size= send(new_socket , data , size_of_data , 0);
        printf("size: %d bytes\n", size);
    
        if(size<0){
            perror("Send formal data failed. Error");
            return 1;
		}
        size_of_data = size_of_data - size;
        data += size;
        printf("size_of_Data: %d bytes\n", size_of_data);
    }
    
    puts("Successfully sent all the data");

    // Receive confirmation from client that all data has received
    if( recv(new_socket, receive_buffer_pro , 10000 , 0) < 0)
    {
        perror("Success message recv failed. Error");
        return 1;
    }
    puts("Success message received\n");


    // Socket close and free allocated memory
    close(new_socket);
    close(s);
    //free(data);

    return 0;
}
