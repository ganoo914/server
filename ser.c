//this is small chatting server
#include <stdio.h>
#include <system/socket.h>

int main(int argc, char *argv[])
{
  int socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);
  
  if (socket_descriptor == -1) 
  {
    printf("Couldn't create socket \n");
  }
  
  return 0;
}
