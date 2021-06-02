#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include <arpa/inet.h>
#include<netinet/in.h>
#include <unistd.h>

int main(int argc, char const *argv[])
{
    int s, new_socket, c;
    struct sockaddr_in server, client;
    int test_amount = 1000000000;
    int size_of_data = test_amount + 1000;
    int size_sent;
    int size_received;
    int16_t handshake_size = 0;
    
    // Arrange data
    char* data_pre = (char*)malloc(1000);
     if (data_pre == NULL) {
        printf("Small memory chunck not allocated.\n");
        return 1;
    }

    char* data = (char*)malloc(size_of_data); 
    if (data == NULL) {
        printf("Big memory chunck not allocated.\n");
        return 1;
    }

    //char* receive_buffer_pro = (char*)malloc(1000); 

    for(int i=0; i<1000; i++){
    	data_pre[i] = 48;  			// assign '0' to the allocated memory
    }

    for(int i = 0; i < size_of_data; i++){ 
        data[i] = 49;                           // assign '1' to the allocated memory
    }

    // Create a socket
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

    //Send a small data packet to client to reduce the influence of overhead
    while (size_of_data>test_amount)
    {
        size_sent = send(new_socket, data_pre, 1000, 0);
        printf("size_sent:%d\n", size_sent);
        if(size_sent<0){
            perror("Small packet set failed. Error");
            return 1;
        }
        if(size_sent==0){
            puts("Did not managed to send out the small packet. size_sent=0");
        }
        size_of_data -= size_sent;
        data_pre += size_sent;
    }

    //Do a handshake with client
    size_received = recv(new_socket, (char*)&handshake_size, 2, 0);
    if(size_received<0){
        perror("Handshake failed. Error");
    }
    else if(size_received==0){
        puts("Handshake failed. Receive 0 bytes.\n");
    }

    handshake_size = ntohs(handshake_size);
    if(handshake_size != 1000){
        puts("The client did not fullly receive the small packet.");
        return 1;
    }
    puts("Handshake done.");

    //Send large chunck of data to client
    while (size_of_data>0) // the remaining part is greater than 0
    {
        size_sent= send(new_socket , data , size_of_data , 0);
	    printf("size_sent:%d\n", size_sent);
        if(size_sent<0){
            perror("Send formal data failed. Error");
            return 1;
		}
        if(size_sent==0){
            puts("Did not managed to send out all data. size_sent=0\n");
        }
        size_of_data -= size_sent;
        data += size_sent;
    }
    
    puts("Successfully sent all the data");

    // // Receive confirmation from client that all data has received
    // if( recv(new_socket, receive_buffer_pro , 10000 , 0) < 0)
    // {
    //     perror("Success message recv failed. Error");
    //     return 1;
    // }
    // puts("Success message received\n");


    // Socket close and free allocated memory
    close(new_socket);
    close(s);

    return 0;
}
