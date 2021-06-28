#ifdef __WIN32__
# include <winsock.h>
#else
# include <sys/socket.h>
#endif

#include <sys/>
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma once
#ifdef WIN32

#define POLLIN      0x001
#define POLLFD      0x002
#define POLLERR     0x008

struct pollfd
{
	Socket fd;
	short events;
	short revents;
};

int poll(struct pollfd* fds, unsigned int nfds, int timeout);

#else
#include <poll.h>
#endif


#ifdef WIN32
int poll(struct pollfd* fds, unsigned int nfds, int timeout)
{
	FD_SET  rset;
	unsigned int    i;
	int   n, iCount = 0;
	struct timeval  sttTimeout;
	sttTimeout.tv_sec = timeout / 1000;
	sttTimeout.tv_usec = (timeout % 1000) * 1000;

	FD_ZERO(&rset);
	for (i = 0; i < nfds; ++i)
	{
		if (fds[i].fd != -1)
			FD_SET(fds[i].fd, &rset);
	}

	n = select(0, &rset, NULL, NULL, &sttTimeout);
	if (n <= 0)
	{
		return n;
	}

	for (i = 0; i < nfds; ++i)
	{
		if (FD_ISSET(fds[i].fd, &rset))
		{
			fds[i].revents = POLLIN;
			++iCount;
		}
		else
		{
			fds[i].revents = 0;
		}
	}

	return iCount;
}
#endif