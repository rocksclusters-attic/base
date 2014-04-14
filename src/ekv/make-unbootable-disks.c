/*
 * $Id: make-unbootable-disks.c,v 1.14 2012/11/27 00:48:35 phil Exp $
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
 * $Log: make-unbootable-disks.c,v $
 * Revision 1.14  2012/11/27 00:48:35  phil
 * Copyright Storm for Emerald Boa
 *
 * Revision 1.13  2012/05/06 05:48:40  phil
 * Copyright Storm for Mamba
 *
 * Revision 1.12  2011/07/23 02:30:44  phil
 * Viper Copyright
 *
 * Revision 1.11  2010/09/07 23:53:05  bruno
 * star power for gb
 *
 * Revision 1.10  2009/05/01 19:07:05  mjk
 * chimi con queso
 *
 * Revision 1.9  2008/10/18 00:55:59  mjk
 * copyright 5.1
 *
 * Revision 1.8  2008/03/06 23:41:41  mjk
 * copyright storm on
 *
 * Revision 1.7  2007/06/23 04:03:22  mjk
 * mars hill copyright
 *
 * Revision 1.6  2006/09/11 22:47:09  mjk
 * monkey face copyright
 *
 * Revision 1.5  2006/08/10 00:09:31  mjk
 * 4.2 copyright
 *
 * Revision 1.4  2005/10/12 18:08:38  mjk
 * final copyright for 4.1
 *
 * Revision 1.3  2005/09/16 01:02:18  mjk
 * updated copyright
 *
 * Revision 1.2  2005/05/24 21:21:53  mjk
 * update copyright, release is not any closer
 *
 * Revision 1.1  2005/03/01 02:02:47  mjk
 * moved from core to base
 *
 * Revision 1.2  2005/02/14 21:56:45  bruno
 * check to see if device node file exists. if it does, remove it first then
 * try to create it
 *
 * Revision 1.1  2004/09/03 23:21:19  bruno
 * new
 *
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <syslog.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <getopt.h>
#include <linux/fs.h>
#include <fcntl.h>
#include <sys/stat.h>

/*
 * make sure all disks are unbootable
 */
static void
unbootable(char *device, int major, int minor)
{
	mode_t		mode;
	struct stat	statbuf;
	int		fd;
	char		devicepath[128];
	char		buf[2];

	sprintf(devicepath, "/tmp/rocks-%s", device);

	if (stat(devicepath, &statbuf) == 0) {
		/*
		 * the device name file exists, let's remove it before
		 * the call to mknod (mknod fails if the the device name
		 * already exists)
		 */
		unlink(devicepath);
	}

	mode = S_IFBLK | S_IRUSR | S_IWUSR;

	if (mknod(devicepath, mode, makedev(major, minor)) < 0) {
		perror("unbootable:mknod failed");
		return;
	}

	if ((fd = open(devicepath, O_WRONLY)) < 0) {
		perror("unbootable:open failed");
		unlink(devicepath);
		return;
	}

	lseek(fd, 510, SEEK_SET);

	buf[0] = 0x00;
	buf[1] = 0x00;

	if (write(fd, buf, sizeof(buf)) < 0) {
		perror("unbootable:write failed");
	}

	/*
	 * now tell the kernel to re-read the partition table
	 */
	if (ioctl(fd, BLKRRPART) != 0) {
		perror("unbootable:ioctl failed");
	}

	close(fd);
	unlink(devicepath);
	return;
}

int
main()
{
	unsigned int	part_size;
	int		fd;
	int		major, minor, blocks;
	int		bytesread;
	char		done;
	char		*buf;
	char		*dev;
	char		*diskdevice;
	char		*line;
	char		*ptr;

	part_size = 2048;
	done = 0;
	while (!done) {
		if ((buf = (char *)malloc(part_size)) == NULL) {
			perror("main:malloc failed");
			return(-1);
		}

		if ((fd = open("/proc/partitions", O_RDONLY)) < 0) {
			perror("main:open failed for /proc/partitions");
			return(-1);
		}

		bytesread = read(fd, buf, part_size);
		if (bytesread < 0) {
			perror("main:read failed for /proc/partitions");
			return(-1);
		}

		if (bytesread < part_size) {
			done = 1;
		} else {
			free(buf);
			part_size = part_size * 2;
		}

		close(fd);
	}

	diskdevice = NULL;

	/*
	 * eat the first two lines
	 *
	 * there is a two line header on the output of
	 * /proc/partitions -- toss those lines, then do
	 * the work
	 */
	ptr = buf;
	line = strsep(&ptr, "\n");
	line = strsep(&ptr, "\n");
	
	while ((line = strsep(&ptr, "\n")) != NULL) {
		if (strcmp(line, "") != 0) {
			major = atoi(strtok(line, " "));
			minor = atoi(strtok(NULL, " "));
			blocks = atoi(strtok(NULL, " "));
			dev = strtok(NULL, " ");

			if (diskdevice == NULL) {
				diskdevice = strdup(dev);
				unbootable(diskdevice, major, minor);
			} else {
				if (strncmp(dev, diskdevice,
						strlen(diskdevice)) != 0) {

					free(diskdevice);
					diskdevice = strdup(dev);
					unbootable(diskdevice, major, minor);
				}
			}
		}
	}

	if (diskdevice != NULL) {
		free(diskdevice);
	}

	free(buf);

	return(0);
}
