# $Id: __init__.py,v 1.12 2008/03/06 23:41:35 mjk Exp $
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
# Revision 1.12  2008/03/06 23:41:35  mjk
# copyright storm on
#
# Revision 1.11  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.10  2007/06/23 03:54:51  mjk
# - first pass at consistency
# - still needs some docstrings
# - argument processors take SQL wildcards
# - add cannot run twice (must use set)
# - dump does sets not just adds
#
# Revision 1.9  2007/06/19 16:42:40  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.8  2007/06/18 22:34:41  phil
# Rewrote add host interface to use set commands
# Fixed error in subnet
# Xrefs in ip
#
# Revision 1.7  2007/06/11 19:26:58  mjk
# - apache counts as root
# - alphabetized some help flags
# - rocks dump error on arguments
#
# Revision 1.6  2007/06/09 00:24:45  anoop
# Moving away from device names.
# Also adding interfaces should make sure that device names
# are checked before subnets. This should change in the future
# but absolutely vital now for things to stay stable
#
# Revision 1.5  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.4  2007/05/30 22:08:32  bruno
# added help
#
# Revision 1.3  2007/05/30 20:14:25  anoop
# Modified the "rocks add host interface" script rather heavily
# to know about and use the subnets table in the database. Trying
# to move towards device independance. Currently in Beta. Still needs
# heavy testing
#
# Revision 1.2  2007/05/10 20:37:00  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.1  2007/04/18 22:03:44  bruno
# commands to add/remove host interfaces is now:
#
#     rocks add host interface
#     rocks remove host interface
#
# Revision 1.2  2007/04/18 22:00:11  bruno
# remove interfaces from the new rocks command line
#
# Revision 1.1  2007/04/18 21:43:43  bruno
# converted add-extra-nic to command line
#
#


import os
import stat
import time
import sys
import string
import rocks.commands


class Command(rocks.commands.HostArgumentProcessor, rocks.commands.add.command):
	"""
	Adds an interface to a host and sets the associated values 

	<arg type='string' name='host'>
	Host name of machine
	</arg>
	
	<arg type='string' name='iface'>
	The interface name on the host (e.g., 'eth0', 'eth1')
	</arg>
	
	<param type='string' name='iface'>
	Can be used in place of the iface argument.
	</param>

	<param type='string' name='ip'>
	The IP address to assign to the interface (e.g., '192.168.1.254')
	</param>

	<param type='string' name='subnet'>
	The name of the subnet to assign to the interface (e.g., 'private')
	</param>
	
	<param type='string' name='gateway'>
	The gateway to assign to the interface (e.g., '192.168.1.1')
	</param>
	
	<param type='string' name='name'>
	The name to assign to the interface
	</param>
	
	<param type='string' name='mac'>
	The MAC address of the interface (e.g., '00:11:22:33:44:55')
	</param>
	
	<param type='string' name='module'>
	The device driver name (or module) of the interface (e.g., 'e1000')
	</param>

	<example cmd='add host interface compute-0-0 eth1 ip=192.168.1.2 subnet=private gateway=192.168.1.1 name=fast-0-0'>
	</example>
	
	<example cmd='add host interface compute-0-0 iface=eth1 ip=192.168.1.2 subnet=private gateway=192.168.1.1 name=fast-0-0'>
	same as above
	</example>

	<related>set host interface gateway</related>
	<related>set host interface iface</related>
	<related>set host interface ip</related>
	<related>set host interface mac</related>
	<related>set host interface module</related>
	<related>set host interface name</related>
	<related>set host interface subnet</related>
	"""

	def run(self, params, args):

		(args, iface) = self.fillPositionalArgs(('iface',))
		hosts = self.getHostnames(args)
		
		if not iface:
			self.abort('missing iface')

		if len(hosts) != 1:	
			self.abort('must supply one host')
		host = hosts[0]

		rows = self.db.execute("""select * from networks,nodes where 
			nodes.name='%s' and networks.device='%s' and
			networks.node=nodes.id""" % (host, iface))
		if rows:
			self.abort('interface "%s" exists' % iface)

		# Add the interface and then call the set commands for
		# all the provided parameters
		
		self.db.execute("""insert into networks(node,device)
			values ((select id from nodes where name='%s'), '%s')"""
			% (host, iface)) 

		for key in ['gateway', 'ip', 'mac', 'module', 'name', 'subnet']:
			if params.has_key(key):
				self.command('set.host.interface.%s' % key,
					(host, iface, params[key]))
