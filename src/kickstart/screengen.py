#! @PYTHON@
#
# $Id: screengen.py,v 1.25 2012/11/27 00:48:38 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: screengen.py,v $
# Revision 1.25  2012/11/27 00:48:38  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.24  2012/09/18 23:33:17  clem
# I need to make kickstart.cgi loadable as a module (I need that in the EC2 roll)
# then i fixed all the other classes in the pylib
#
# Revision 1.23  2012/05/06 05:48:44  phil
# Copyright Storm for Mamba
#
# Revision 1.22  2011/07/23 02:30:47  phil
# Viper Copyright
#
# Revision 1.21  2010/09/07 23:53:07  bruno
# star power for gb
#
# Revision 1.20  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.19  2009/01/08 01:20:58  bruno
# for anoop
#
# Revision 1.18  2009/01/08 00:41:36  mjk
# test when you need to
#
# Revision 1.17  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.16  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.15  2007/12/13 02:53:40  bruno
# can now build a bootable kernel CD and build a physical frontend with V
# on RHEL 5 update 1
#
# Revision 1.14  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.13  2006/09/11 22:47:16  mjk
# monkey face copyright
#
# Revision 1.12  2006/08/10 00:09:37  mjk
# 4.2 copyright
#
# Revision 1.11  2006/07/11 21:17:55  bruno
# screen cleanup
#
# Revision 1.10  2006/07/05 19:13:05  bruno
# use values from /tmp/site.xml for default values
#
# Revision 1.9  2006/06/05 17:57:37  bruno
# first steps towards 4.2 beta
#
# Revision 1.8  2006/03/22 18:32:41  bruno
# make screens more self contained
#
# Revision 1.7  2006/03/19 23:19:19  bruno
# screen validation is now done for every screen
#
# Revision 1.6  2006/03/19 21:19:40  bruno
# added a form validator -- it is a concatenation of all the screen validation
# functions and is run when the user hits the 'next' button
#
# Revision 1.5  2006/03/17 20:29:43  bruno
# can now handle including javascript 'code' for form validation
#
# Revision 1.4  2006/03/16 17:23:24  bruno
# screengen can now handle hidden variables and can now call javascript
# validation code
#
# Revision 1.3  2006/02/27 23:21:25  bruno
# support for the help frame
#
# Revision 1.2  2006/02/24 22:35:20  bruno
# added support for password fields and default values
#
# Revision 1.1  2006/02/24 21:32:09  bruno
# parse XML screen node files
#
#

import os
import sys
import string
import rocks.gen
import rocks.file
import rocks.gen
import rocks.app
from xml.dom                 import ext
from xml.dom.ext.reader.Sax2 import FromXmlStream
from xml.sax._exceptions     import SAXParseException
from rocks.util import KickstartError


class ScreenNodeFilter(rocks.gen.NodeFilter):
	def acceptNode(self, node):
		if node.nodeName == 'kickstart':
			return self.FILTER_ACCEPT
			
		if node.nodeName not in [ 
			'screen',
			'title',
			'variable',
			'code',
			]:
			return self.FILTER_SKIP

		if not self.isCorrectCond(node):
			return self.FILTER_SKIP

		return self.FILTER_ACCEPT

osGenerator = getattr(rocks.gen, 'Generator_%s' % os.uname()[0].lower())

class Generator(osGenerator):

	def __init__(self):
		rocks.gen.Generator.__init__(self)	
		self.screens = []

	
	##
	## Parsing Section
	##
	
	def parse(self, file):
		doc  = FromXmlStream(file)

		filter = ScreenNodeFilter({})
		iter = doc.createTreeWalker(doc, filter.SHOW_ELEMENT,
			filter, 0)
		node = iter.nextNode()

		while node:
			if node.nodeName == 'screen':
				self.screens.append({})
				child = iter.firstChild()
				while child:
					self.handle_screenChild(child)
					child = iter.nextSibling()
			node = iter.nextNode()
			
	# <screen>
	
	def handle_screenChild(self, node):
		try:
			eval('self.handle_screen_%s(node)' % node.nodeName)
		except:
			pass

	# <screen>
	#	<title>
	# </screen>
	def handle_screen_title(self, node):
		self.screens[-1]['title'] = '%s' % (self.getChildText(node))
		return


	# <screen>
	#	<variable>
	# </screen>
	def handle_variableChild(self, node):
		try:
			eval('self.handle_variable_%s(node)' % node.nodeName)
		except:
			pass
		return


	def handle_screen_variable(self, node):
		if not self.screens[-1].has_key('variables'):
			self.screens[-1]['variables'] = [{}]
		else:
			self.screens[-1]['variables'].append({})

		for child in node.childNodes:
			self.handle_variableChild(child)

		return


	# <screen>
	#	<variable>
	#		<label>
	# </screen>
	def handle_variable_label(self, node):
		self.screens[-1]['variables'][-1]['label'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<name>
	# </screen>
	def handle_variable_name(self, node):
		self.screens[-1]['variables'][-1]['name'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<type>
	# </screen>
	def handle_variable_type(self, node):
		self.screens[-1]['variables'][-1]['type'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<size>
	# </screen>
	def handle_variable_size(self, node):
		self.screens[-1]['variables'][-1]['size'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<default>
	# </screen>
	def handle_variable_default(self, node):
		self.screens[-1]['variables'][-1]['default'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<value>
	# </screen>
	def handle_variable_value(self, node):
		self.screens[-1]['variables'][-1]['value'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<validate>
	# </screen>
	def handle_variable_validate(self, node):
		self.screens[-1]['variables'][-1]['validate'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<help>
	# </screen>
	def handle_variable_help(self, node):
		self.screens[-1]['variables'][-1]['help'] = \
			'%s' % (self.getChildText(node))
		return

	# <screen>
	#	<variable>
	#		<option>
	# </screen>
	def handle_variable_option(self, node):
		if not self.screens[-1]['variables'][-1].has_key('option'):
			self.screens[-1]['variables'][-1]['option'] = []

		self.screens[-1]['variables'][-1]['option'].append(
			'%s' % (self.getChildText(node)))
		return

	# <screen>
	#	<code>
	# </screen>
	def handle_screen_code(self, node):
		if not self.screens[-1].has_key('code'):
			self.screens[-1]['code'] = ''

		self.screens[-1]['code'] += '%s' % (self.getChildText(node))
		return

	# <screen>
	#	<code>
	#		<include>
	# </screen>
	def handle_screen_include(self, node):
		self.screens[-1]['code'] = '%s' % (self.getChildText(node))
		return

	# <*>
	#	<*> - tags that can go inside any other tags
	# </*>
	def getChildText(self, node):
		text = ''
		for child in node.childNodes:
			if child.nodeType == child.TEXT_NODE:
				text += child.nodeValue
			elif child.nodeType == child.ELEMENT_NODE:
				text += eval('self.handle_screen_%s(child)' \
					% (child.nodeName))
		return text

	
	##
	## Generator Section
	##
	def generateScreen(self, screen, i):
		if self.screens[i].has_key('code'):
			print self.screens[i]['code']
			print ""

		print "function screen%d()" % (i)
		print "{"

		print "\tvar\td_title = " + \
			"top.workarea.document.createElement('div');"
		print "\tvar\td_vars = " + \
			"top.workarea.document.createElement('div');"
		print "\tvar\td_help = " + \
			"top.help.document.createElement('div');"
		print "\tvar\td_buttons = " + \
			"top.workarea.document.createElement('div');"
		print "\tvar\thelptext;"

		print ""

		#
		# output the screen title
		#
		print "\td_title.id = 'screen-title';"
		print "\td_title.appendChild(top.addTitleText" + \
			"('%s'));" % (self.screens[i]['title'])
		print "\ttop.screen_title[%d] = d_title;" % (i)

		print ""

		#
		# output the screen variables
		#
		print "\td_vars.id = 'screen-variables';"
		for variable in self.screens[i]['variables']:
			if not variable.has_key('type'):
				inputtype = 'text'
			else:
				if variable['type'] == 'password':
					inputtype = 'password'
				elif variable['type'] == 'hidden':
					inputtype = 'hidden'
				elif variable['type'] == 'radio':
					inputtype = 'radio'
				elif variable['type'] == 'menu':
					inputtype = 'menu'
				else:
					inputtype = 'text'

			if not variable.has_key('size'):
				size = 20
			else:
				size = variable['size']

			if variable.has_key('value') \
						and variable['value'] != '':
				value = variable['value']
			elif variable.has_key('default'):
				value = variable['default']
			else:
				value = ''

			if not variable.has_key('validate'):
				validate = 'null'
			else:
				validate = 'top.screens.%s' % \
					(variable['validate'])

			if inputtype == 'menu':
				print "\tvar options = new Array();"
				if variable.has_key('option'):
					j = 0
					for option in variable['option']:
						o = "\toptions[%d] = " % (j)
						o += "'%s';" % (option)
						print o
						j = j +1

				print "\td_vars.appendChild(top.addToMenu(" + \
					"'%s'" % (variable['label']) + \
					", '%s'" % (variable['name']) + \
					", '%s'" % (size) + \
					", %s" % (validate) + \
					", options" + \
					", '%s'));" % (value)
			else:
				print "\td_vars.appendChild(top.addToForm(" + \
					"'%s'" % (inputtype) + \
					", '%s'" % (variable['label']) + \
					", '%s'" % (variable['name']) + \
					", '%s'" % (size) + \
					", '%s'" % (value) + \
					", %s));" % (validate)
		print "\ttop.screen_variables[%d] = d_vars;" % (i)

		print ""

		#
		# output the screen help
		#
		print "\td_help.id = 'screen-help';"
		for variable in self.screens[i]['variables']:
			if not variable.has_key('help'):
				continue
			else:
				help = variable['help']

			print "\td_help.appendChild(top.addToHelp(" + \
				"'%s:'" % (variable['label']) + \
				", '%s'));" % (help)
		print "\ttop.screen_help[%s] = d_help;" % (i)

		#
		# output the screen buttons
		#
		print ""
		print "\td_buttons.id = 'screen-buttons';"
		print "\td_buttons.appendChild(" + \
			"top.addButton('Back', top.prevScreen));"
		print "\td_buttons.appendChild(" + \
			"top.addButton('Next', " + \
				"validate_screen%d));" % (i)
		print "\ttop.screen_buttons[%s] = d_buttons;" % (i)

		#
		# end the 'function screen[0-9]*' function
		#
		print "}"

		#
		# now output the form validation code. this is just a
		# concatenation of all the variable validators
		#
		validatefunctions = []
		for variable in self.screens[i]['variables']:
			if variable.has_key('validate'):
				functioncall = variable['validate'] + '(e)'
				validatefunctions.append(functioncall)

		#
		# register the screen form validation function with
		# the parent screen
		#
		if validatefunctions == []:
			validatefunctions = [ 'true' ]

		#
		# now print out the screen validation code
		#
		print ""
		print "function validate_screen%d(e)" % (i)
		print "{"
		print "\tvar retval = true;"
		print ""
		print "\tif ((" + \
			string.join(validatefunctions, ' && ') + ")) {"
		print "\t\ttop.savevalues();"
		print "\t\ttop.nextScreen();"
		print "\t} else {"
		print "\t\tretval = false;"
		print "\t}"
		print ""
		print "\treturn(retval);"
		print "}"
		print ""

		return


	def generate(self):
		print '<html>'
		print '<head>'

		print '<script language="JavaScript">'

		i = 0;
		for screen in self.screens:
			self.generateScreen(screen, i)
			i = i + 1

		print ''

		print 'function initScreens()'
		print '{'
		i = 0;
		for screen in self.screens:
			#
			# call the screen functions to initialize them
			#
			print '\tself.screen%d();' % (i)
			i = i + 1
		print '}'

		print '</script>'
		print '</head>'
		print '</html>'

		return


class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)

		self.usage_name = 'Installation Screen Generator'
		self.usage_version = '@VERSION@'
		self.sections = []

		self.os = os.uname()[0].lower()
		self.generator = Generator()		
		self.generator.setArch(self.getArch())
		self.generator.setOS(self.os)

		self.getopt.s.extend([('a:', 'architecture')])
		self.getopt.l.extend([('arch=', 'architecture')])


	def usageTail(self):
		return ' [file]'


	def parseArg(self, c):
		if rocks.app.Application.parseArg(self, c):
			return 1
		elif c[0] in ('-a', '--arch'):
			self.generator.setArch(c[1])
		else:
			return 0
		return 1


	def run(self):
        	if self.args:
			file = self.args[0]
		else:
			file = sys.stdin
		
		self.generator.parse(file)
		self.generator.generate()

		return


if __name__ == "__main__":
	app = App(sys.argv)
	app.parseArgs()
	app.run()

