#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<time.h>
#include<arpa/inet.h>
#include<netinet/in.h>
#include<unistd.h>

int main(int argc , char *argv[])
{
	int s;
    struct sockaddr_in server;
    char success_message[] = "Received All";
    int test_amount = 1000000000;
    int buffer_size = test_amount + 1000;
	struct timespec begin, end;
	int size;

    //Allocate memory
	char* receive_buffer = (char*)malloc(buffer_size);
	
    //Create a socket
    s = socket(AF_INET , SOCK_STREAM , 0);
	if (s == -1)
	{
		printf("Could not create socket.");
        return 1;
	}
    printf("Socket created.");

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("132.206.51.95"); // IP of mimi
	server.sin_port = htons( 8888 );

	//Connect to remote server
	if (connect(s , (struct sockaddr *)&server , sizeof(server)) < 0)
	{
		perror("connect error. Error");
		return 1;
	}
	puts("Connected");
	
	//Receive small packet and do a handshake with server
	size = recv(s, receive_buffer, buffer_size, 0);
    buffer_size -= size;
    receive_buffer += size;
    printf("Small packet received: %d bytes. ", size);

    int network_byte_size = htons(size);
    int handshake_size = send(s, &network_byte_size, 2, 0);
    if(handshake_size<0){
        perror("Hand shake send failed. Error");
        return 1;
    }
    else if(handshake_size==0){
        puts("Handshake info send failed. Send out 0 bytes.");
        return 1;
    }
    puts("Hand shake sent.");
    

    //Receive formal data from the server
    clock_gettime(CLOCK_REALTIME, &begin);
    while (buffer_size>0) // the remaining part is greater than 0
    {	
        size= recv(s, receive_buffer, buffer_size , 0);
	
        if(size<0){
            perror("recv failed. Error");
            return 1;
	    }
	    if(size==0){
	        puts("Connection interrupted, receive 0 bytes.");
		return 1;
	    }

        buffer_size -= size;
        receive_buffer += size;
    }
    puts("All data received.");

    clock_gettime(CLOCK_REALTIME, &end);
    long seconds = end.tv_sec - begin.tv_sec;
    long nanoseconds = end.tv_nsec - begin.tv_nsec;
    double time_spent = seconds + nanoseconds*1e-9;

    printf("The elapsed time is %f seconds.\n", time_spent);
    
    // // Send a confirmation to the server that all data has received
    // if( send(s , success_message , sizeof(success_message) , 0) < 0)
    // {
    // 	puts("Send success message failed");
    // 	return 1;
    // }
    // puts("Success message sent.\n");
  
    // Socket close and free allocated memory
    close(s);
    //free(receive_buffer);

	return 0;
}
