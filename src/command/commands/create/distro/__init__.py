# $Id: __init__.py,v 1.2 2008/05/22 21:02:06 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: __init__.py,v $
# Revision 1.2  2008/05/22 21:02:06  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.1  2008/05/10 01:49:28  bruno
# first draft of rocks-dist replacement
#
#

import os
import os.path
import rocks
import rocks.commands
import rocks.dist
import rocks.build

class Command(rocks.commands.create.command):
	"""
	Create a Rocks distribution. This distribution is used to install
	Rocks nodes.

	<param type='string' name='arch'>
	The architecture of the distribution. The default is the native
	architecture of the machine.
	</param>

	<param type='string' name='version'>
	The version of the distribution. The default is the native
	version of the machine.
	</param>

	<param type='string' name='rolls'>
	A list of rolls that should be included in the distribution. This
	must be a list separated by spaces of the form: rollname,version.
	For example: rolls="CentOS,5.0 kernel,5.0". The default is to
	include all the enabled rolls for the native architecture. To
	get a list of enabled rolls, execute: "rocks list roll".
	</param>

	<param type='string' name='root'>
	The path prefix location of the rolls. The default is:
	/export/rocks/install.
	</param>

	<param type='string' name='dist'>
	The directory name of the distribution. The default is: "rocks-dist".
	</param>

	<example cmd='create distro'>
	Create a distribution in the current directory.
	</example>
	"""

	def makeTorrents(self, dist):    	
		import time

		print 'making "torrent" files for RPMS'

		#
		# mark each torrent file with the current time
		#
		timestamp = time.time()

		for dir in [ dist.getBasePath(), dist.getRPMSPath() ]:
			self.command('create.torrent', [ dir,
				'timestamp=%d' % (timestamp) ])

		return


	def getRolls(self, arch):
		rolls = []

		self.db.execute("""select name,version,arch,enabled from
			rolls where site=0 and OS="linux" """)

		for name,version,arch,enabled in self.db.fetchall():
			if enabled == 'yes' and arch == arch:
				rolls.append([name, version])

		return rolls


	def commandDist(self, dist, rolls):    	
		builder = rocks.build.DistributionBuilder(dist)

		builder.setRolls(rolls)
		builder.setSiteProfiles(1)
		builder.build()

		return builder


	def run(self, params, args):
		#
		# args = arch
		#
		(arch, version, rolls, root, dist) = self.fillParams(
			[ ('arch', self.arch),
			('version', rocks.version),
			('rolls', []),
			('root', '/export/rocks/install'),
			('dist', 'rocks-dist') ])

		lockFile = '/var/lock/rocks-dist'
		os.system('touch %s' % (lockFile))

		if self.db:
			rolls = self.getRolls(arch)

		mirror = rocks.dist.Mirror()
		mirror.setHost('rolls')
		mirror.setPath(root)
		mirror.setRoot(root)
		mirror.setArch(arch)

		mirrors = []
		mirrors.append(mirror)

		distro = rocks.dist.Distribution(mirrors, rocks.version)
		distro.setRoot(os.getcwd())
		distro.setDist(dist)
		distro.setLocal('/usr/src/redhat')
		distro.setContrib(os.path.join(mirror.getRootPath(), 'contrib',
			rocks.version))

		builder = self.commandDist(distro, rolls)
		base = distro.getBasePath()
		try:
			self.makeTorrents(distro)
		except:
			pass

		#
		# make sure everyone can traverse the the rolls directories
		#
		mirrors = distro.getMirrors()
		fullmirror = mirrors[0].getRollsPath()
		os.system('find %s -type d ' % (fullmirror) + \
			'-exec chmod -R 0755 {} \;')

		try:
			os.unlink(lockFile)
		except:
			pass
