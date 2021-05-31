#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include <time.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc , char *argv[])
{
	int s;
    struct sockaddr_in server;
    char* receive_buffer_pre;
	char* receive_buffer;
    char success_message[] = "Received All";
	int recv_size = 100000;
	struct timespec begin, end;

	receive_buffer_pre = (char*)malloc(10000);
	receive_buffer = (char*)malloc(recv_size);
       
	
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

	//Connect to remote server
	if (connect(s , (struct sockaddr *)&server , sizeof(server)) < 0)
	{
		perror("connect error. Error");
		return 1;
	}
	puts("Connected");
	
    //Receive a small packet from the server
    if( recv(s, receive_buffer_pre , 10000 , 0) < 0)
	{
		puts("Small packet recv failed");
        return 1;
	}
	puts("Small packet received\n");
	
    //Receive formal data from the server
    clock_gettime(CLOCK_REALTIME, &begin);

    while (recv_size>0) // the remaining part is greater than 0
    {
        int size= recv(s, receive_buffer, recv_size , 0);
	    printf("size is %d bytes\n", size);
	
        if(size<0){
            perror("recv failed. Error");
            return 1;
	    }
	    if(size==0){
	    break;
	    }
        recv_size = recv_size - size;
        receive_buffer += size;
        printf("The recv_size is %d bytes\n", recv_size);
    }

    puts("All data received\n");

    clock_gettime(CLOCK_REALTIME, &end);
    long seconds = end.tv_sec - begin.tv_sec;
    long nanoseconds = end.tv_nsec - begin.tv_nsec;
    double time_spent = seconds + nanoseconds*1e-9;

    printf("The elapsed time is %f seconds.\n", time_spent);
    
    // Send a confirmation to the server that all data has received
    if( send(s , success_message , sizeof(success_message) , 0) < 0)
    {
    	puts("Send success message failed");
    	return 1;
    }
    puts("Success message sent.\n");
  
    // Socket close and free allocated memory
    close(s);
    free(receive_buffer_pre);
    //free(receive_buffer);

	return 0;
}