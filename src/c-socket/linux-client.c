#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<time.h>
#include<arpa/inet.h>
#include<netinet/in.h>
#include<unistd.h>

void transmit(int socket, int target_size)
{
    int32_t size = target_size;
    int size_sent = send(socket, (char*)&size, 4, 0);
    if(size_sent<0){
        perror("Send confirm data failed. Error");
        exit(1);
	}
    if(size_sent==0){
        puts("Did not managed to send out the confirm data. size_sent=0\n");
        exit(1);
    }
}

void receive(int socket, char* receive_buffer, int target_size, int buffer_size)
{   
    int goal = target_size;
    while (target_size>0)
    {	
        int size= recv(socket, receive_buffer, buffer_size , 0);
        if(size<0){
            perror("recv failed. Error");
            exit(1);
	    }
	    if(size==0){
	        puts("Connection interrupted, receive 0 bytes.");
		    exit(1);
	    }
        buffer_size -= size;
        receive_buffer += size;
        target_size -= size;
    }
    printf("All data received: %d bytes\n", goal);
}

int main(int argc , char *argv[])
{   
    int target_size = atoi(argv[1]);
	int s;
    struct sockaddr_in server;
	struct timespec begin, end;
	int size;

    //Allocate memory
	char* receive_buffer = (char*)malloc(target_size+1000);
	
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
	receive(s, receive_buffer, 1000, target_size+1000);
    transmit(s, 1000);
    
    //Formal data
    clock_gettime(CLOCK_REALTIME, &begin);

    for(int i=0; i<3; i++){
        //Receive formal data from server
        receive(s, receive_buffer+1000, target_size, target_size);
        //Send ack to the server
        transmit(s, target_size);
    }

    clock_gettime(CLOCK_REALTIME, &end);
    
    //Calculate elapsed time
    long seconds = end.tv_sec - begin.tv_sec;
    long nanoseconds = end.tv_nsec - begin.tv_nsec;
    double time_spent = seconds + nanoseconds*1e-9;

    printf("The elapsed time is %f seconds.\n", time_spent);
    
    // Socket close and free allocated memory
    close(s);
    free(receive_buffer);

	return 0;
}
