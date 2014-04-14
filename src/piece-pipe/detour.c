/*
 * $Id: detour.c,v 1.14 2012/11/27 00:48:40 phil Exp $
 *
 * @Copyright@
 * 
 * 				Rocks(r)
 * 		         www.rocksclusters.org
 * 		       version 6.1.1 (Sand Boa)
 * 
 * Copyright (c) 2000 - 2014 The Regents of the University of California.
 * All rights reserved.	
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice unmodified and in its entirety, this list of conditions and the
 * following disclaimer in the documentation and/or other materials provided 
 * with the distribution.
 * 
 * 3. All advertising and press materials, printed or electronic, mentioning
 * features or use of this software must display the following acknowledgement: 
 * 
 * 	"This product includes software developed by the Rocks(r)
 * 	Cluster Group at the San Diego Supercomputer Center at the
 * 	University of California, San Diego and its contributors."
 * 
 * 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
 * neither the name or logo of this software nor the names of its
 * authors may be used to endorse or promote products derived from this
 * software without specific prior written permission.  The name of the
 * software includes the following terms, and any derivatives thereof:
 * "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
 * the associated name, interested parties should contact Technology 
 * Transfer & Intellectual Property Services, University of California, 
 * San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
 * Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
 * 
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * @Copyright@
 *
 * $Log: detour.c,v $
 * Revision 1.14  2012/11/27 00:48:40  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.13  2012/05/06 05:48:45  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.12  2011/07/23 02:30:48  phil
 * Viper Copyright
 *
 * Revision 1.11  2010/09/07 23:53:08  bruno
 * star power for gb
 *
 * Revision 1.10  2009/05/01 19:07:08  mjk
 * chimi con queso
 *
 * Revision 1.9  2008/10/18 00:56:01  mjk
 * copyright 5.1
 *
 * Revision 1.8  2008/03/06 23:41:44  mjk
 * copyright storm on
 *
 * Revision 1.7  2007/06/23 04:03:24  mjk
 * mars hill copyright
 *
 * Revision 1.6  2006/09/11 22:47:22  mjk
 * monkey face copyright
 *
 * Revision 1.5  2006/08/10 00:09:40  mjk
 * 4.2 copyright
 *
 * Revision 1.4  2005/10/12 18:08:41  mjk
 * final copyright for 4.1
 *
 * Revision 1.3  2005/09/16 01:02:20  mjk
 * updated copyright
 *
 * Revision 1.2  2005/05/24 21:21:57  mjk
 * update copyright, release is not any closer
 *
 * Revision 1.1  2005/03/01 02:02:49  mjk
 * moved from core to base
 *
 * Revision 1.15  2004/04/20 05:24:30  bruno
 * for the first time in 3.5 years, we've decided this code needs an update.
 *
 * set detour to only accept connections from the localhost.
 *
 * Revision 1.14  2004/03/25 03:15:47  bruno
 * touch 'em all!
 *
 * update version numbers to 3.2.0 and update copyrights
 *
 * Revision 1.13  2003/08/15 22:34:46  mjk
 * 3.0.0 copyright
 *
 * Revision 1.12  2003/05/22 16:39:28  mjk
 * copyright
 *
 * Revision 1.11  2003/02/17 18:43:04  bruno
 * updated copyright to 2003
 *
 * Revision 1.10  2002/10/18 21:33:26  mjk
 * Rocks 2.3 Copyright
 *
 * Revision 1.9  2002/02/21 21:33:27  bruno
 * added new copyright
 *
 * Revision 1.8  2001/05/09 20:17:19  bruno
 * bumped copyright 2.1
 *
 * Revision 1.7  2001/04/10 14:16:31  bruno
 * updated copyright
 *
 * Revision 1.6  2001/02/14 20:16:34  mjk
 * Release 2.0 Copyright
 *
 * Revision 1.5  2000/10/23 20:04:16  bruno
 * added code to make CR/LF look pretty
 *
 * Revision 1.4  2000/10/23 14:13:30  bruno
 * increased the read from stdin buffer from 1 to 1024
 *
 * Revision 1.3  2000/10/20 00:07:32  mjk
 * Cleaned usage() command
 * Fixed detach in spec file
 *
 * Revision 1.2  2000/10/19 22:52:20  bruno
 * tweaks
 *
 * Revision 1.1  2000/10/19 13:31:41  bruno
 * added detour and spec file
 *
 */
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <libiberty.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <arpa/telnet.h>

#ifndef max
#define max(a,b)	(a) > (b) ? (a) : (b)
#endif

#define DEFAULT_PORT	8000

#define	BUFLEN		1024

static const char	*usage_name    = "Network Detour";
static const char	*usage_version = VERSION " (" __DATE__ "" __TIME__ ")";
static const char	*usage_text = "[-h] [-p port]";
static const char	*usage_help =
"\t-h\thelp\n"
"\t-p <port>\tport number to listen for connections\n"
;

static void
usage(FILE *fout, const char *name)
{
	fprintf(fout,"%s - version %s\nUsage: %s %s\n",
		usage_name, usage_version, name, usage_text);
}

static void
help(FILE *fout, const char *name)
{
	usage(fout, name);
	fprintf(fout, "%s", usage_help);
}

static int
net_redirect(int infd, int outfd)
{
	int		readbytes, writebytes;
	int		i;
	unsigned char	buf[1];

	if ((readbytes = read(infd, buf, 1)) <= 0) {
		/*
		 * either an error occured (-1), or the other end of the
		 * network connection was shutdown (0). either way, stop
		 * processing.
		 */
		return(-1);
	}

	switch(buf[0]) {
	case IAC:
		/*
		 * if we get an "interpret as command" character from the
		 * network, then eat it and the next two characters
		 */
		for (i = 0; i < 2; i++) {
			if ((readbytes = read(infd, buf, 1)) <= 0) {
				return(-1);
			}
		}
		break;

	case 0x0d:
		/*
		 * carriage return from the client. eat the next byte 0x00
		 * and output a native carriage return
		 */
		if ((readbytes = read(infd, buf, 1)) <= 0) {
			return(-1);
		}

		buf[0] = '\n';
		if ((writebytes = write(outfd, buf, 1)) <= 0) {
			return(-1);
		}


		break;

	default:
		if ((writebytes = write(outfd, buf, readbytes)) <= 0) {
			return(-1);
		}
		break;
	}

	return(0);
}

static int
process_ack(int client, unsigned char *expected_ack, unsigned int ack_length)
{
	int		i;
	unsigned char	c;

	/*
	 * pick up the ack from the client
	 */
	for (i = 0; i < ack_length; ++i) {
		if (read(client, &c, 1) == -1) {

			fprintf(stderr, "process_ack:read:errno (%d)\n", errno);
			return(-1);
		}

		if (c != expected_ack[i]) {
			fprintf(stderr, "process_ack:");
			fprintf(stderr, "expected (0x%x), got (0x%x)\n",
				expected_ack[i], c);

			return(-1);
		}
	}

	return(0);
}

/*
 * this function tells the client to go into 'character at a time mode',
 * meaning every keystroke will be transferred in a packet.
 */
static int
negotiate_telnet_options(int client)
{
	unsigned char	suppress_go_ahead[] = { IAC, WILL, TELOPT_SGA };
	unsigned char	ack_suppress_go_ahead[] = { IAC, DO, TELOPT_SGA };

	unsigned char	will_echo[] = { IAC, WILL, TELOPT_ECHO };
	unsigned char	ack_will_echo[] = { IAC, DO, TELOPT_ECHO };

	if (write(client, suppress_go_ahead, 
			sizeof(suppress_go_ahead)) == -1) {

		fprintf(stderr, "negotiate_telnet_options:write:suppress_go_ahead:errno (%d)\n", errno);

		return(-1);
	}

	if (process_ack(client, ack_suppress_go_ahead,
			sizeof(ack_suppress_go_ahead)) == -1) {

		fprintf(stderr, "negotiate_telnet_options:process_ack:suppress_go_ahead\n");

		return(-1);
	}

	if (write(client, will_echo, 
			sizeof(will_echo)) == -1) {

		fprintf(stderr, "negotiate_telnet_options:write:suppress_go_ahead:errno (%d)\n", errno);

		return(-1);
	}

	if (process_ack(client, ack_will_echo, sizeof(ack_will_echo)) == -1) {
		fprintf(stderr,
			"negotiate_telnet_options:process_ack:will_echo\n");

		return(-1);
	}

	return(0);
}

static int
stdin_redirect(int infd, int outfd)
{
	int	readbytes;
	char	buf[1];

	readbytes = read(infd, buf, sizeof(buf));
	switch(readbytes) {
	case 0:
		/*
		 * stdin was closed -- exit
		 */
		exit(0);

	case -1:
		/*
		 * hard error -- tell the caller
		 */
		return(-1);

	default:
		/*
		 * received data -- fall through
		 */
		break;
	}

	if (buf[0] == '\n') {
		unsigned char	cr = '\r';

		/*
		 * special processing so CR/LF look good on the other side
		 */
		if (write(outfd, &cr, 1) <= 0) {
			/*
			 * either an error occured (-1), or the other end of the
			 * network connection was shutdown (0). either way, stop
			 * processing.
			 */
			return(-1);
		}
	}

	if (write(outfd, buf, readbytes) <= 0) {
		/*
		 * either an error occured (-1), or the other end of the
		 * network connection was shutdown (0). either way, stop
		 * processing.
		 */
		return(-1);
	}

	return(0);
}

static int
detour(int client)
{
	fd_set	rset;

	/*
	 * wait for input from either standard in or the network connection
	 */
	FD_ZERO(&rset);
	FD_SET(STDIN_FILENO, &rset);
	FD_SET(client, &rset);

	if (select(max(STDIN_FILENO,client)+1, &rset, NULL, NULL, NULL) == -1) {
		fprintf(stderr, "detour:select:errno (%d)\n", errno);
		return(-1);
	}

	if (FD_ISSET(STDIN_FILENO, &rset)) {
		if (stdin_redirect(STDIN_FILENO, client) == -1) {
			return(-1);
		}
	}

	if (FD_ISSET(client, &rset)) {
		if (net_redirect(client, STDOUT_FILENO) == -1) {
			return(-1);
		}
	}

	return(0);
}

static int
connection_mgmt(short port)
{
	struct sockaddr_in	sin;
	int			s;
	int			client;


	/*
	 * open a socket to listen for connections
	 */
	if ((s = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
		fprintf(stderr,
			"connection_mgmt:socket:errno (0x%x)\n", errno);
		return(-1);
	}

	bzero(&sin, sizeof(sin));
	sin.sin_family = AF_INET;
	/*
	 * only allow connections from the loopback.
	 * this is a poor-man's iptables.
	*/
	sin.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
	sin.sin_port = htons(port);

	/*
	 * bind the endpoint to 'port'
	 */
	if (bind(s, (struct sockaddr *)&sin, sizeof(sin)) == -1) {
		fprintf(stderr,
			"connection_mgmt:bind:errno (0x%x)\n", errno);
		close(s);
		return(-1);
	}

	/*
	 * tell the socket to listen for 1 connection
	 */
	if (listen(s, 1) == -1) {
		fprintf(stderr,
			"connection_mgmt:listen:errno (0x%x)\n", errno);
		close(s);
		return(-1);
	}

	while (1) {
		/*
		 * accept the connection
		 */
		if ((client = accept(s, NULL, NULL)) == -1) {
			fprintf(stderr,
				"connection_mgmt:accept:errno (0x%x)\n", errno);
			close(s);
			return(-1);
		}

		if (negotiate_telnet_options(client) == -1) {
			fprintf(stderr,
				"connection_mgmt:negotiate_telnet_options\n");
		} else {
			while (detour(client) == 0)
				;
		}

		close(client);
	}

	close(s);
	return(0);
}

int
main(int argc, char **argv)
{
	/*
	 * get the port number
	 */
	const char	*usage_command = (const char *)basename(argv[0]);
	int			c;
	short			port = DEFAULT_PORT;

	opterr = 0;
	while ((c = getopt(argc, argv, "p:h")) != EOF) {
		switch (c) {
		case 'p':	/* port number				*/
			port = atoi(optarg);
			break;

		case 'h':	/* help 				*/
			help(stdout, usage_command);
			exit(0);
		default:	/* usage 				*/
			usage(stderr, usage_command);
			exit(-1);
		}
	}

	argc -= optind;
	if ( argc != 0 ) {
		usage(stderr, usage_command);
		exit(-1);
	}

	while (1) {
		connection_mgmt(port);

		/*
		 * connection_mgmt returns only on a error, so sleep in hopes
		 * the retry will be successful
		 */
		sleep(1);
	}
}
