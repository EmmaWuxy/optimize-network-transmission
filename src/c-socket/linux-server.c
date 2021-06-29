#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include <arpa/inet.h>
#include<netinet/in.h>
#include <unistd.h>

void transmit(int socket, char* data, int test_size)
{
    int goal = test_size;
    while (test_size>0)
    {
        int size_sent= send(socket , data , test_size , 0);
        if(size_sent<0){
            perror("Send data failed. Error");
            exit(1);
		}
        if(size_sent==0){
            puts("Did not managed to send out all data. size_sent=0");
            exit(1);
        }
        test_size -= size_sent;
        data += size_sent;
    }
    printf("Successfully sent %d bytes\n", goal);
}

void receive(int socket, int test_size)
{
    int32_t handshake_size = 0;
    int size_received = recv(socket, (char*)&handshake_size, 4, 0);
    if(size_received<0){
        perror("Handshake failed. Error");
        exit(1);
    }
    else if(size_received==0){
        puts("Handshake failed. Receive 0 bytes.");
        exit(1);
    }
    puts("Handshake done.");
}

int main(int argc, char const *argv[])
{   
    int test_size = atoi(argv[1]);
    int s, new_socket, c;
    struct sockaddr_in server, client;
    int8_t close_request = 0;

    // Arrange data
    char* data_pre = (char*)malloc(1000);
     if (data_pre == NULL) {
        printf("Small memory chunck not allocated.\n");
        return 1;
    }

    char* data = (char*)malloc(test_size); 
    if (data == NULL) {
        printf("Big memory chunck not allocated.\n");
        return 1;
    }

    for(int i=0; i<1000; i++){
    	data_pre[i] = 48;  			       // assign '0' to the allocated memory
    }

    for(int i = 0; i < test_size; i++){ 
        data[i] = 49;                      // assign '1' to the allocated memory
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

    //Send 1000 bytes to client to reduce the influence of overhead
    transmit(new_socket, data_pre, 1000);

    //Receive the ack from the client of receiving 1000 characters
    receive(new_socket, 1000);

    for(int i=0; i<3; i++){
        //Send large chunck of data to client
        transmit(new_socket, data, test_size);
        //Receive the ack from the client of receving test_size characters, check if the client receive all bytes
        receive(new_socket, test_size);
    }
    
    //Send back a request for closing
    transmit(new_socket, (char*)&close_request, 1);

    // Socket close
    close(new_socket);
    close(s);

    return 0;
}
