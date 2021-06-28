/*
	Live Server on port 8888
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <Python.h>

#define SIZE 1024

void error_handling(char * message);

void send_file(int sockfd)
{
    FILE *fp;
    char *filename = "../server/result.txt";
    char msg_a[SIZE];

    fp = fopen(filename, "r");
    if (fp == NULL)
    {
        perror("Error in creating file");
        exit(1);
    }
    fgets(msg_a, 1024, fp);

    printf("send\n");
    //write(sockfd, msg_a, sizeof(msg_a));
    int i = send(sockfd, msg_a, sizeof(msg_a), 0);
    printf("%d", i);
    return;
}

void run_python(int sockfd)
{
    //send_file(sockfd);
    printf("run.. python\n");
    Py_Initialize();
    PyRun_SimpleString("import sys; sys.path.append('.')");
    PyRun_SimpleString("import preprocess_model;");
    Py_Finalize();
    //send_file(sockfd);
    return;
}

void write_file(int sockfd)
{
    int n;
    FILE *fp;
    char *filename = "../server/sample.txt";
    char buffer[SIZE];

    fp = fopen(filename, "w");
    if (fp == NULL)
    {
        perror("Error in creating file");
        exit(1);
    }

    while(1)
    {
        n = recv(sockfd, buffer, SIZE, 0);
        printf("%d\n", n);
        if (n <= 0)
        {
            printf("n is smaller than zero\n");
            break;
            return;
        }
        //printf("write....");
        fprintf(fp, "%s", buffer);
        bzero(buffer, SIZE);
    }
    run_python(sockfd);
    //send_file(sockfd);
    return;
}

int main(int argc, char* argv[])
{
	int serv_sock;
	int clnt_sock;
    //int read_size;
    //char client_message[2000];

    FILE *fp;
    char *filename = "count.txt";
    char count_buf[100];

	//if AF_INET, use it
	struct sockaddr_in serv_addr;
	struct sockaddr_in clnt_addr;
	socklen_t clnt_addr_size;

	//make TCP socket
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
	if(serv_sock == -1)
		error_handling("socket error");

	//after init, remote ip & port
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET; //type: ipv4
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); //ip address
    serv_addr.sin_port = htons(atoi(argv[1])); //port

    //binding
    if(bind(serv_sock, (struct sockaddr*) &serv_addr, sizeof(serv_addr))==-1)
        error_handling("bind error");
    else
        printf("binding\n");
    
    //connection suspend_listen
    if(listen(serv_sock, 5) == -1)
        error_handling("listen error");

    //connect
    clnt_addr_size = sizeof(clnt_addr);
    clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);
    if(clnt_sock == -1)
        error_handling("accept error");
    else
        printf("connect\n");

    fp = fopen(filename, "r");
    fgets(count_buf, 8, fp);
    fclose(fp);
    printf("char: %c\n", count_buf[0]);
    printf("string: %s\n", count_buf);

    if (strcmp(count_buf, "file") == 0)
    {
        printf("clnt_sock\n");
        fp = fopen(filename, "w");
        fprintf(fp, "send");
        fclose(fp);
        write_file(clnt_sock);
    }
    else
    {
        printf("send_file\n");
        fp = fopen(filename, "w");
        fprintf(fp, "file");
        fclose(fp);
        send_file(clnt_sock);
    }

    //fgets(count_buf, sizeof(count_buf), fp);
    //printf("%c", count_buf[0]);

    //Py_Initialize();
    //PyRun_SimpleString("import sys; sys.path.append('.')");
    //PyRun_SimpleString("import preprocess_model;");
    //Py_Finalize();

    //send data
    //char msg_a[] = "accuracy: 0.8073394298553467 loss: 0.3763086795806885";
    //write(clnt_sock, msg, sizeof(msg));
    //send(clnt_sock, msg_a, sizeof(msg_a), 0);

    //send data
    //char msg[] = "Hello this is server";
    //write(clnt_sock, msg, sizeof(msg));
    //send(clnt_sock, msg, sizeof(msg), 0);
    //send_file(clnt_sock);
    //close socket

    close(clnt_sock);
    close(serv_sock);
    return 0;
}

void error_handling(char *message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}