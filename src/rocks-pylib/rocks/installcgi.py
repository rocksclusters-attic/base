#! /opt/rocks/bin/python
#
# $Id: installcgi.py,v 1.19 2012/11/27 00:48:40 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: installcgi.py,v $
# Revision 1.19  2012/11/27 00:48:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.18  2012/05/06 05:48:47  phil
# Copyright Storm for Mamba
#
# Revision 1.17  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.16  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.15  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.14  2009/03/04 01:32:13  bruno
# attributes work for frontend installs
#
# Revision 1.13  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.12  2008/05/30 22:15:16  bruno
# can now install a frontend off CD with the distro moved to
# /export/rocks/install
#
# Revision 1.11  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.10  2008/03/24 20:58:44  bruno
# more apache vs. lighttpd directory listing parsing
#
# Revision 1.9  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.8  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.7  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.6  2006/11/29 23:12:40  bruno
# prototype support for lights out frontend installs
#
#

import os
import os.path
import string
import shutil
import rocks.file
import rocks.util

class InstallCGI:

	def __init__(self, rootdir=None):
		if rootdir == None:
			cmd = '/opt/rocks/bin/rocks report distro'
			for line in os.popen(cmd).readlines():
				distrodir = line[:-1]
			self.rootdir = distrodir
		else:
			self.rootdir = rootdir

		cmd = '/opt/rocks/bin/rocks report version'
		for line in os.popen(cmd).readlines():
			self.version = line[:-1]

		self.arch = rocks.util.getNativeArch()

		return


	def createPopt(self, dir=None):
		if dir == None:
			dir = self.rootdir

		if not os.path.exists(dir):
			os.system('mkdir -p %s' % (dir))

		filename = os.path.join(dir, '.popt')

		if not os.path.exists(filename):
			file = open(filename, 'w')
			file.write("rpm alias --dbpath --define '_dbpath !#:+'")
			file.write("\n")
			file.close()

		return


	def getSiteDotAttrs(self):
		#
		# look in the newly built distro for site.attrs
		#
		site_attrs = os.path.join(self.rootdir, 'rocks-dist', self.arch,
			'build', 'nodes', 'site.attrs')

		if os.path.exists(site_attrs):
			shutil.copy(site_attrs, '/tmp/site.attrs')

		return


	def createSkeletonSiteAttrs(self):
		self.getSiteDotAttrs()
		if os.path.exists('/tmp/site.attrs'):
			return

		file = open('/tmp/site.attrs', 'w')

		#
		# set the language
		#
		cmdline = open('/proc/cmdline', 'r')
		args = string.split(cmdline.readline())
		cmdline.close()

		#
		# the default language
		#
		lang = 'en_US'
		langsupport = 'en_US'

		for arg in args:
			if arg.count('lang='):
				a = string.split(arg, '=')
				if len(a) > 1 and a[1] == 'ko':
					lang = 'ko_KR'
					langsupport = string.join([
						'ko_KR.UTF-8',
						'ko_KR',
						'ko',
						'en_US.UTF-8',
						'en_US'
						])

		file.write('Kickstart_Lang:%s\n' % lang)
		file.write('Kickstart_Langsupport:%s\n' % langsupport)

		file.close()

		return


	def getKickstartFiles(self, roll):
		#
		# for every selected roll, find the roll-{name}-kickstart*rpm
		# file
		#
		cwd = os.getcwd()

		self.createPopt(self.rootdir)

		contribdir = os.path.join(self.rootdir, 'contrib', self.version,
			self.arch, 'RPMS')

		os.system('mkdir -p %s' % (contribdir))
		os.chdir(contribdir)

		(rollname, rollver, rollarch, rollurl, diskid) = roll
		url = rollurl + '%s/%s/%s/' % (rollname, rollver, rollarch)
		url += 'RedHat/RPMS/'

		if os.path.exists('/tmp/updates/rocks/bin/wget'):
			wget = '/tmp/updates/rocks/bin/wget'
		else:
			wget = '/usr/bin/wget'

		cmd = '%s -O - -nv %s 2> /dev/null' % (wget, url)

		for line in os.popen(cmd).readlines():
			a = string.split(line, '"')

			if a[0] == '<a href=':
				#
				# apache style listing
				#
				filename = a[1]
			elif len(a) > 2 and a[2] == '><a href=':
				#
				# lighttpd style listing
				#
				filename = a[3]
			else:
				continue

			l = filename.split('-')

			if l[0] != 'roll':
				continue
			try:
				k = l.index('kickstart')
				rollname = '-'.join(l[1:k])
			except ValueError:
				continue

			#
			# if we're here, we know we have a
			# roll-<rollname>-kickstart*rpm file, so download
			# the RPM
			#
			roll_kickstart_rpm = url + filename
			getcmd = '%s --quiet %s' % (wget, roll_kickstart_rpm)
			os.system(getcmd)

		os.chdir(cwd)
		return


	def rebuildDistro(self, rollslist):
		cwd = os.getcwd()
		os.chdir(self.rootdir)

		#
		# get a list of the rolls
		#
		rolls = []
		for r in rollslist:
			(rollname, rollversion, rollarch, rollurl, diskid) = r
			rolls.append('%s,%s' % (rollname, rollversion))

		#
		# build the distro
		#
		pythonpath = os.environ['PYTHONPATH']
		os.environ['PYTHONPATH'] = ''

		cmd = 'HOME=%s ' % (self.rootdir)
		cmd += '/opt/rocks/bin/rocks create distro '
		if len(rolls) > 0:
			cmd += 'rolls="%s" ' % ' '.join(rolls)
		cmd += 'root=%s ' % (self.rootdir)
		os.system('echo %s > /tmp/rocks-create-distro.debug' % cmd)
		os.system(cmd + ' >> /tmp/rocks-create-distro.debug 2>&1')

		os.environ['PYTHONPATH'] = pythonpath

		os.chdir(cwd)

		return

