# $Id: __init__.py,v 1.6 2012/11/27 00:48:30 phil Exp $

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

# $Log: __init__.py,v $
# Revision 1.6  2012/11/27 00:48:30  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/07/31 23:20:10  phil
# Generate a cluster-wide ssh [rsa,dsa] keys and put them in
# the secure attributes database. These are different from frontend's host keys.
# Place these on nodes with rocks sync host sec_attr (new sec_attr plugins).
# Add list global sec_attr command
#
# Revision 1.4  2012/05/06 05:48:36  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2012/02/15 21:23:58  clem
# moving from import sha to import hashlib
#
# Revision 1.2  2011/07/23 02:30:40  phil
# Viper Copyright
#
# Revision 1.1  2011/06/03 02:34:40  anoop
# Added code for secure_attributes
#

import os
import sys
import rocks.commands
import crypt
import rocks.password
import getpass
import random
import string

class Command(rocks.commands.set.command):
	"""
	Set a secure attribute to the database.
	The user also has the option of not supplying the
	value on the command line. The command will prompt
	the user to enter the secure attribute value, and
	will not echo this value on screen.

	If the user chooses to enter the value for the secure
	attribute by prompt, then the value entered must be in
	an unencrypted form.
	
	<arg type='string' name='attr'>
	Name of the attribute
	</arg>

	<param type='string' name='value'>
	Value of the attribute. If value is a file, read the value from the file
	</param>
	
	<param type='boolean' name='crypted'>
	Is "value" already crypted or not
	</param>

	<param type='string' name='enc'>
	Encryption scheme to use to crypt the value. Currently
	supported values are "sha", "crypt", "portable".
	</param>

	<example cmd='set sec_attr db_pw
	value=DatabasePassword crypted=false enc=sha'>
	Sets a secure attribute called db_pw to the crypted
	value of "DatabasePassword" using the sha1 encoding schema.
	</example>

	<example cmd='set sec_attr db_pw
	value=77e6674e6d71f898d5fc79424117c86731ca7498 crypted=true'>
	Same as above
	</example>
	"""
	def run(self, params, args):
		
		(args, attr) = self.fillPositionalArgs(('attr'))
		# Get params
		(attr, value, crypted, enc) = self.fillParams([('attr', attr),
						('value', None),
						('crypted','n'), ('enc', None)])

		if attr is None:
			self.abort('missing attribute name')

		# Check if value is supposed to be crypted
		crypted = self.str2bool(crypted)
		
		
		if enc == None:
			rows = self.db.execute('select enc from sec_global_attributes ' +\
				'where attr="%s"' % attr)
			if not rows:
				enc = "sha"
			else:
				(enc, ) = self.db.fetchone()

		self.enc = rocks.password.Enc()
		if hasattr(self.enc, 'enc_%s' % enc):
			f = getattr(self.enc, 'enc_%s' % enc)
		else:
			self.abort('Encryption method %s not supported' % enc)

		#
		# see if the value is a file name
		#
		if value is not None and os.path.exists(value):
			file = open(value, 'r')
			value = file.read()
			file.close()

		if value is None:
			if crypted == 1:
				sys.stderr.write('Ignoring crypted argument\n')
			crypted = 0
			value = getpass.getpass('  Enter %s: ' % attr)
			c_value = getpass.getpass('Confirm %s: ' % attr)
			if c_value != value:
				self.abort('Values don\'t match')
			


		if crypted == 0:
			enc_value = f(value)
		else:
			enc_value = value

		rows = self.db.execute('select * from sec_global_attributes ' + \
			'where attr="%s"' % attr)
		if rows:
			self.db.execute('update sec_global_attributes ' +\
				'set value="%s", enc="%s" where attr="%s"' \
				% (enc_value, enc, attr))
		else:	
			self.db.execute('insert into sec_global_attributes ' +\
				'values ("%s", "%s", "%s")' \
				% (attr, enc_value, enc))
