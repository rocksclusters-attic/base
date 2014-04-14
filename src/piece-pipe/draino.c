static char rcsid[] = "$Id: draino.c,v 1.14 2012/11/27 00:48:40 phil Exp $";
/* -----------------------------------------------------------------------
 *
 * file		$RCSfile: draino.c,v $
 * author(s)	Mason J. Katz
 * created	10/17/00 15:34:26	mjk
 *
 * -----------------------------------------------------------------------
 *
 * 
 *
 * -----------------------------------------------------------------------
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
 * $Log: draino.c,v $
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
 * Revision 1.16  2004/03/25 03:15:47  bruno
 * touch 'em all!
 *
 * update version numbers to 3.2.0 and update copyrights
 *
 * Revision 1.15  2003/08/15 22:34:46  mjk
 * 3.0.0 copyright
 *
 * Revision 1.14  2003/05/22 16:39:28  mjk
 * copyright
 *
 * Revision 1.13  2003/02/17 18:43:04  bruno
 * updated copyright to 2003
 *
 * Revision 1.12  2002/10/18 21:33:26  mjk
 * Rocks 2.3 Copyright
 *
 * Revision 1.11  2002/02/21 21:33:27  bruno
 * added new copyright
 *
 * Revision 1.10  2001/05/09 20:17:19  bruno
 * bumped copyright 2.1
 *
 * Revision 1.9  2001/04/10 14:16:31  bruno
 * updated copyright
 *
 * Revision 1.8  2001/02/14 20:16:34  mjk
 * Release 2.0 Copyright
 *
 * Revision 1.7  2000/11/02 05:09:34  mjk
 * Added Copyright
 *
 * Revision 1.6  2000/10/20 19:13:18  mjk
 * Lowered select timeout for draino
 * Bumped version number
 *
 * Revision 1.5  2000/10/20 17:04:25  mjk
 * Fixed mem leak bug
 * Added bufferram to freeram for mem utilization test
 *
 * Revision 1.4  2000/10/20 00:07:32  mjk
 * Cleaned usage() command
 * Fixed detach in spec file
 *
 * Revision 1.3  2000/10/19 23:12:21  mjk
 * Bumped version number
 * added detach.c
 * fixed bug in draino.c
 *
 * Revision 1.2  2000/10/19 20:04:46  mjk
 * Change pipe upward bounds to be a function of remaining RAM rather than
 * a fixed constant.
 *
 * Revision 1.1  2000/10/19 19:22:28  mjk
 * Cleanup on CSP
 * Added draino.c
 *
 */

#include <stdio.h>
#include <signal.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <assert.h>
#include <sys/time.h>
#ifdef __linux__
#include <libgen.h>
#include <linux/kernel.h>
#include <sys/sysinfo.h>
#endif

#define DEFAULT_MAX_MEMUSAGE	99

#ifndef max
#define max(a,b)	(a) > (b) ? (a) : (b)
#endif

typedef struct node {
	char		*pkt;
	size_t		len;
	struct node	*next;
} node_t;

typedef struct list {
	node_t		*head;
	node_t		*tail;
} list_t;


static void	help(FILE *fout, const char *name);
static void	usage(FILE *fout, const char *name);
static int	draino(int in, int out, int memusage);
static int	list_add(list_t *list, int fd, int memusage);
static node_t	*list_pop(list_t *list);
static int	mem_utilization(void);

static const char	*usage_name    = "Draino";
static const char	*usage_version = VERSION " ("__DATE__"  "__TIME__")";
static const char	*usage_text = "[-h] [-m percent]";
static const char	*usage_help =
"\t-h\thelp\n"
"\t-m\tpercent of memory to remain free\n"
;



int
main(int argc, char *argv[])
{
	const char	*usage_command	= (const char *)basename(argv[0]);
	int		memusage	= DEFAULT_MAX_MEMUSAGE;
	int		c;

	opterr = 0;
	while ( (c=getopt(argc,argv,"h")) != EOF ) {
		switch ( c ) {
		case 'm':	/* mem upward bounds percent 		*/
			memusage = atoi(optarg);
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
	argv += optind;

 	return draino(STDIN_FILENO, STDOUT_FILENO, memusage);
} /* main */


static int
draino(int in, int out, int memusage)
{
	int		done		= 0;
	int		retval		= 0;
	node_t		*node		= NULL;
	char		*head;
	char		*tail;
	fd_set		rset;
	int		n;
	struct timeval	tv;
	int		flags;
	list_t		list;
	int		len;

	list.head = list.tail = NULL;

				/* Set output to nonblocking */
	if ( (flags = fcntl(out, F_GETFL, 0)) < 0 ) {
		perror("F_GETFL");
		return -1;
	}
	if ( (fcntl(out, F_SETFL, flags | O_NONBLOCK)) ) {
		perror("F_SETFL");
		return -1;
	}
	
	while ( !done || node ) {
		FD_ZERO(&rset);
		FD_SET(in, &rset);
		tv.tv_sec  = 0;
		tv.tv_usec = done ? 0 : 50000;

		n = select(in+1, &rset, NULL, NULL, &tv);

		if ( FD_ISSET(in, &rset) ) {
			if ( !list_add(&list, in, memusage) ) {
				done = 1;
			}
		}
		if ( !node ) {
			node = list_pop(&list);
			if ( node ) {
				head = node->pkt;
				tail = node->pkt + node->len;
			}
		}
		if ( node ) {
			len = write(out, head, tail - head);
			if ( len > 0 ) {
				head += len;
				if ( head >= tail ) {
					if ( node->pkt ) {
						free(node->pkt);
					}
					free(node);
					node = NULL;
				}
			}
		}
	}

				/* The sender is done, so now we can
                                   block on writes again */
	if ( (flags = fcntl(out, F_GETFL, 0)) < 0 ) {
		perror("F_GETFL");
		return -1;
	}
	if ( (fcntl(out, F_SETFL, flags & (~O_NONBLOCK))) ) {
		perror("F_SETFL");
		return -1;
	}
	
				/* Push out rest of the list */
	while ( (node = list_pop(&list)) ) {
		if ( write(out, node->pkt, node->len)  < 0 ) {
			perror("write");
		}
		if ( node->pkt ) {
			free(node->pkt);
		}
		free(node);
	}
	

	return retval;
} /* draino */


static int
list_add(list_t *list, int fd, int memusage)
{
	node_t	*node;
	char	buf[1024];
	int	len;

	assert(list);
	len = read(fd, buf, sizeof buf);

				/* If we read data and we still have
                                   the desired amount of RAM still
                                   available copy the data into the
                                   tail of the list */
	if ( len > 0 ) {
		if ( mem_utilization() < memusage ) {
			node = calloc(1, sizeof *node);
			assert(node);
			node->pkt = calloc(1, len);
			assert(node->pkt);

			memcpy(node->pkt, buf, len);
			node->len = len;

			if ( list->tail ) {
				list->tail->next = node;
				list->tail       = node;
			} else {
				list->tail = node;
				list->head = node;
			}
		}
	}

	else if ( len < 0 ) {
		perror("read");
	}

	return len;
} /* list_add */

static node_t *
list_pop(list_t *list)
{
	node_t	*node = NULL;

	assert(list);
	if ( list->head ) {
		node = list->head;
		list->head = node->next;
		if ( node == list->tail ) {
			list->head = NULL;
			list->tail = NULL;
		}
	}
	
	return node;
} /* list_pop */


static int
mem_utilization(void)
{
	struct sysinfo	info;
	float		percent = 0;

	if ( sysinfo(&info) < 0 ) {
		perror("sysinfo");
	} else {
		percent = 1 - ((float)(info.freeram+info.bufferram) /
			       info.totalram);
	}
	return percent * 100;
} /* mem_utilization */


static void
help(FILE *fout, const char *name)
{
	usage(fout, name);
	fprintf(fout, "%s", usage_help);
} /* help */
  

static void
usage(FILE *fout, const char *name)
{
	fprintf(fout,"%s - version %s\nUsage: %s %s\n",
		usage_name, usage_version, name, usage_text);
} /* usage */


