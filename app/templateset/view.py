import wx
import wx.lib.masked
import json
from library.db.dal import Row
import datetime
import time
from library.ordereddict import ordereddict

class TemplatesetViewForm:
	def __init__(self,controller,notebook,template,fromemail,responseid=None,responsedata=None):
		'''
		@param controller: the parent TemplatesetController
		@type controller: TemplatesetController
		@param notebook: the notebook you are putting the templateset form on
		@type notebook: wx.NoteBook
		@param template: The template data to make a form of
		@type template: Dict
		@param fromemail: email that the message is from
		@type fromemail: String
		@param response: the message data you are responding to
		@type response: Dict
		'''
		self.responsedata = responsedata
		self.controller = controller
		self.template = template
		self.show = {}
		self.hide = {}
		self.responsedataid = responseid
		self.valuemap = {}
		self.itemmap = {}
		self.fromemail = self.controller.controller.settings.IMAP_EMAIL
		if self.responsedataid is not None:
			self.evmailmodel = self.controller.controller.getEvmailController().model
			self.templaterow = self.controller.controller.getTemplatesetController().model.getTemplate(template['hide']['setname'],template['hide']['name'],template['hide']['version'])
			if self.templaterow['towho'] == 'sender' or self.templaterow['towho'] == 'all':
				self.todata = self.evmailmodel.getMessageReplyTo(responseid)
				if self.todata is not None:
					if isinstance(self.todata,tuple):
						if self.todata[1] is None or self.todata[1] == '':
							self.todata = self.evmailmodel.getMessageFroms(responseid)
				else:
					self.todata = self.evmailmodel.getMessageFroms(responseid)
				print type(self.todata)
				if str(type(self.todata)).find('list') != -1:
					tostr = ''
					for each in self.todata:
						tostr += each['name']+' '+each['email']+', '
					self.todata = tostr
				else:
					print self.todata
					self.todata = self.todata[0]+' '+self.todata[1]+', '

				print self.todata
			if self.templaterow['towho'] == 'all':
				oldtos = self.evmailmodel.getMessageTos(responseid)
				if str(type(oldtos)).find('list') != -1:
					tostr = ''
					for each in oldtos:
						if each['email'] != self.fromemail.strip():
							tostr += each['name']+' '+each['email']+', '
					oldtos = tostr
				else:
					oldtos = oldtos[0]+' '+oldtos[1]+', '
				self.todata += oldtos
			self.valuemap['to'] = self.todata
		else:
			self.templaterow = None
			self.valuemap['to'] = ''
		self.notebook = notebook
		self.panel = wx.lib.scrolledpanel.ScrolledPanel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel.SetupScrolling()

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.generateFormLabel(self.panel,hbox2,"To")
		self.to = wx.TextCtrl(self.panel, wx.ID_ANY,size=(600,100),style=wx.TE_MULTILINE)
		self.to.AppendText(str(self.valuemap['to']))
		self.itemmap['to'] = self.to
		hbox2.Add(self.to)
		self.vbox.Add(hbox2,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))
		self.vbox = self.generateElements(template['show'])
		self.generateEndButton()
		if self.responsedataid is not None:
			lister = self.controller.controller.getEvmailController().view.generateMessageSizer(self.panel,self.evmailmodel.getMessage(responseid),self.fromemail)			
			self.vbox.AddMany(lister)

	def generateAElements(self,itemsdata,name):
		'''
		Genearte form elements in an array data structure
		@param itemsdata: Items data of elements in array
		@type itemsdata: List
		@param name: name of array
		@type name: String
		'''
		hboxtop = wx.BoxSizer(wx.HORIZONTAL)
		hboxtop = self.generateFormLabel(self.panel,hboxtop,name)
		addarraybutton = wx.Button(self.panel,label="Remove this "+name)
		hboxtop.Add(addarraybutton, flag=wx.RIGHT,border=10)
		addarraybutton.Bind(wx.EVT_BUTTON,self.onDelArray,id=addarraybutton.GetId())
		self.vbox.Add(hboxtop,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		
		for each in itemsdata:
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			if isinstance(each,dict):
				if each.__contains__('responsemapsto'):
					mapsto = each['responsemapsto']
				else:
					mapsto = None
				if itemsdata[each].__contains__('editable'):
					editable = itemsdata[each]['editable']
				else:
					editable = True
				if each.__contains__('type'):
					# add widget based on type & format
					if each['type'] == 'object':
						if each.__contains__('properties'):
							self.generateElements(each['properties'])
					elif each['type'] == 'array':
						pass
							# generate + button
							#addarraybutton = wx.Button(self.panel,label="+")
							#hbox.Add(addarraybutton, flag=wx.RIGHT,border=10)
							#addarraybutton.Bind(wx.EVT_BUTTON,self.onAddArray,id=addarraybutton.GetId())
					else:
						if each.__contains__('format'):
							format = each['format']
						else:
								format = None
						if format == 'date-time':
							hbox = self.generateFormElement(self.panel,hbox,name,each['type'],'date',mapsto)
							hbox = self.generateFormElement(self.panel,hbox,name,each['type'],'time',mapsto)
						else:
							hbox = self.generateFormElement(self.panel,hbox,name,itemsdata[each]['type'],format,mapsto)
				else:
					hbox = self.generateFormLabel(self.panel,hbox,name)
			elif isinstance(itemsdata[each],str):
				self.required = True
			self.vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
			self.vbox.Add((-1,10))
		


	def generateElements(self,itemsdata,parentresponsemapsto=[]):
		'''
		Genearte form elements in an array data structure
		@param itemsdata: Items data of elements in array
		@type itemsdata: List
		'''
		for each in itemsdata:
			mapsto = []
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			if isinstance(itemsdata[each],dict):
				if itemsdata[each].__contains__('responsemapsto'):
					mapsto.append(itemsdata[each]['responsemapsto'])
				else:
					mapsto = parentresponsemapsto
					mapsto.append(each)
				if itemsdata[each].__contains__('editable'):
					editable = itemsdata[each]['editable']
				else:
					editable = True
				if itemsdata[each].__contains__('type'):
					# add widget based on type & format
					if itemsdata[each]['type'] == 'object':
						if itemsdata[each].__contains__('properties'):
							self.generateElements(itemsdata[each]['properties'],mapsto)
						else:
							raise Exception, "Malformed json: object has no properties (templateset/view/generateElements"
					elif itemsdata[each]['type'] == 'array':
						if itemsdata[each].__contains__('items'):
							self.generateAElements(itemsdata[each]['items'],each)
							self.addArray = wx.Button(self.panel,label="Add another "+each)
							hbox.Add(self.addArray, flag=wx.RIGHT,border=10)
							self.addArray.Bind(wx.EVT_BUTTON,self.onAddArray,id=self.addArray.GetId())
					else:
						if itemsdata[each].__contains__('format'):
							format = itemsdata[each]['format']
						else:
								format = None
						if format == 'date-time':
							hbox,item = self.generateFormElement(self.panel,hbox,each,itemsdata[each]['type'],'date',mapsto,editable)
							hbox,item = self.generateFormElement(self.panel,hbox,each,itemsdata[each]['type'],'time',mapsto,editable)
						else:
							hbox,item = self.generateFormElement(self.panel,hbox,each,itemsdata[each]['type'],format,mapsto,editable)
				else:
					hbox = self.generateFormLabel(self.panel,hbox,each)
				if itemsdata[each].__contains__('mapsto'):
					preval = itemsdata[each]['mapsto'].find('[')
					postval = itemsdata[each]['mapsto'].find(']')
					if preval < postval:
						pre = itemsdata[each]['mapsto'][:preval]
						post = itemsdata[each]['mapsto'][postval+1:]
						it = itemsdata[each]['mapsto'][preval+1:postval]
						self.itemmap[it] = (pre,item,post)
					else:
						self.itemmap[itemsdata[each]['mapsto']] = item
			elif isinstance(itemsdata[each],str):
				self.required = True
			print hbox
			self.vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
			self.vbox.Add((-1,10))
		return self.vbox

	def generateEndButton(self):
		'''
		Generate end button for closing array of items
		'''
		sendbutton = wx.Button(self.panel,label="Send")
		sendbutton.Bind(wx.EVT_BUTTON,self.onSendButton,id=sendbutton.GetId())
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(sendbutton,flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.panel.SetSizer(self.vbox)
		
		self.notebook.AddPage( self.panel,"New "+self.template['hide']['setname']+'-'+self.template['hide']['name'], False )
		pcount = self.notebook.GetPageCount()
		self.notebook.SetSelection(pcount-1)

	def readData(self):
		'''
		Read the information populating the form widgets
		@return: the form data
		@rtype: Dict
		'''
		data = {}
		data['show'] = {}
		data['hide'] = {}
		for each in self.show:
			value = ''
			if isinstance(self.show[each],wx.DatePickerCtrl):
				value = self.show[each].GetValue()
				value = value.FormatDate()
			elif isinstance(self.show[each],wx.TextCtrl):
				pos = self.show[each].GetLastPosition()
				value = self.show[each].GetString(0,pos)
			elif isinstance(self.show[each],wx.lib.masked.TimeCtrl):
				value = self.show[each].GetValue(as_wxDateTime=True)
			elif isinstance(self.show[each],wx.ColourPickerCtrl):
				value = self.show[each].GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
			elif isinstance(self.show[each],wx.CheckBox):
				value = str(self.show[each].GetValue())
			data['show'][each] = value

		# generate / retrieve hide data
		if self.responsedata is not None:
			print 'RESPONSEDATA',self.responsedata
			data['hide']['setname'] = self.template['hide']['setname']
			data['hide']['name'] = self.template['hide']['name']			
			data['hide']['version'] = self.template['hide']['version']
			data['hide']['messageid'] = self.controller.controller.getEvmailController().model.generateMessageId()
			data['hide']['messagesetid'] = self.responsedata['hide']['messagesetid']
		else:
			print 'TEMPLATEDATA',self.template
			data['hide']['setname'] = self.template['hide']['setname']
			data['hide']['name'] = self.template['hide']['name']
			data['hide']['version'] = self.template['hide']['version']
			data['hide']['messageid'] = self.controller.controller.getEvmailController().model.generateMessageId()
			data['hide']['messagesetid'] = data['hide']['messageid']
		# get to data		
		pos = self.to.GetLastPosition()
		tostring = self.to.GetString(0,pos)
		'''tostring.split(' ')
		tos = []
		for each in tostring:
			neach = each.strip()
			neach = neach.replace(',','')
			tos.append(neach)'''
		self.todata = tostring
		print 
		return data


	def onSendButton(self,event):
		'''
		Bind response to sending message
		'''
		# get data to send		
		data = self.readData()
		# generate message
		subject = self.itemmap['subject']
		substr = ''
		if str(type(subject)).find('tuple') != -1:
			substr += str(subject[0])
			substr += str(subject[1].GetValue())
			substr += str(subject[2])
			subject = str(substr)
		else:
			subject = str(subject.GetValue())
		to = str(self.itemmap['to'].GetValue())
		fromp = self.fromemail
		try:
			print 'SENDING MESSAGE: ',data
			message = self.controller.controller.getEvmailController().generateMessage(self.template,data,subject,to,fromp)
		except Exception, e:
			self.controller.controller.view.SetStatusText(str(e))
			return "Message genertion failed."	
		# add to database
		'''datastr = json.dumps(data)
		self.controller.getEmailController().addMessage(data['hide']['setname']+'/'+data['hide']['name'],subject,text,message['Date'],tos,fromemail,fromemail,message['Message-ID'],datastr,0)'''
		# send message
	
		emailcontroller = self.controller.controller.getEmailController()
		if emailcontroller.isoffline() == False:
			emailcontroller.sendMessage(self.fromemail,self.todata,message)
			# CLOSE TAB
			print "controller",self.controller
			print "parent controller",self.controller.controller
			print "parent controller view",self.controller.controller.view
			selected = self.notebook.GetSelection()
			self.notebook.DeletePage(selected)
			self.controller.controller.SetStatusText("Message sent to "+str(self.todata))
			return "Message Sent."
		else:
			self.controller.controller.SetStatusText("Message sending failed. Check IMAP settings in app/core/settings.py")
		



	def generateFormElement(self,panel,boxsizer,name,ttype,format=None,responsemapsto=[],editable=True):
		'''
		Generate a single form element
		@param panel: panel to put the widget on
		@type panel: wx.Panel
		@param boxsizer: BoxSizer to put widget on
		@type boxsizer: wx.BoxSizer
		@param name: name of form element
		@type name: String
		@param format: format of form element if any
		@type format: String
		'''
		#add label
		boxsizer = self.generateFormLabel(panel,boxsizer,name)
		# add form element
		if ttype == 'boolean':
			item = wx.CheckBox(panel,wx.ID_ANY)
			self.show[name] = item
			boxsizer.Add(item,flag=wx.RIGHT,border=10)
		elif ttype == 'string' or ttype == 'number' or ttype == 'integer':
			if format is not None:
				if format == 'date':
					item = wx.DatePickerCtrl(panel, wx.ID_ANY)
					# set date
					if len(responsemapsto) > 0 and self.responsedata is not None:
						rdata = self.responsedata['show']
						for rmap in responsemapsto:
							rdata = rdata[rmap]
						time_format = "%m/%d/%Y"
						dt = wx.DateTime()
						rdata = rdata.split('/')
						dt.Set(int(rdata[0]),int(rdata[1]),int(rdata[2]))
						item.SetValue(dt)
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
				elif format == 'time':
					item = wx.lib.masked.TimeCtrl(panel, wx.ID_ANY)
					if len(responsemapsto) > 0 and self.responsedata is not None:
						rdata = self.responsedata['show']
						print rdata
						print 'RD',responsemapsto
						for rmap in responsemapsto:
							rdata = rdata[rmap]
						item.ChangeValue(rdata)
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
					#set time
				elif format == 'color':
					item = wx.ColourPickerCtrl(panel, wx.ID_ANY)
					if len(responsemapsto) > 0 and self.responsedata is not None:
						rdata = self.responsedata['show']
						for rmap in responsemapsto:
							rdata = rdata[rmap]
						item.SetFromName(rdata)
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
				else:
					if format == 'phone':
						item = wx.TextCtrl(panel, wx.ID_ANY,size=(200,30))
					elif format == 'short':
						item = wx.TextCtrl(panel, wx.ID_ANY,size=(800,30))
					if len(responsemapsto) > 0 and self.responsedata is not None:
						rdata = self.responsedata['show']
						for rmap in responsemapsto:
							rdata = rdata[rmap]
						item.AppendText(rdata)
					boxsizer.Add(item,flag=wx.RIGHT,border=10) 
					self.show[name] = item
			else:
				item = wx.TextCtrl(panel, wx.ID_ANY,size=(800,400),style=wx.TE_MULTILINE)
				self.show[name] = item
				boxsizer.Add(item,flag=wx.RIGHT,border=10)
				if len(responsemapsto) > 0 and self.responsedata is not None:
					rdata = self.responsedata['show']
					for rmap in responsemapsto:
						rdata = rdata[rmap]
					item.AppendText(rdata)
			item.Enable(editable)
		return boxsizer,item

	def generateFormLabel(self,panel,boxsizer,label):
		'''	
		Generate the label for a form item
		@param panel: the panel to draw the widget on
		@type panel: wx.Panel
		@param boxsizer: the boxsizer to add the label to
		@type boxsizer: wx.BoxSizer
		@param label: the label for the form element
		@type label: String
		@return: the boxsizer
		@rtype: wx.BoxSizer
		'''
		# add form label
		label = wx.StaticText(panel, wx.ID_ANY, label=label)
		boxsizer.Add(label,flag=wx.RIGHT, border=10)
		return boxsizer

	def validateForm(self):
		pass
	def onAddArray(self,event):
		print event

	def onDelArray(self,event):
		print event
		#for each in self.aitems[0]:
		#	self.

class TemplatesetView(wx.Frame):
	def __init__(self,controller,parent):
		'''
		Initialize TemplatesetView class -- links and creates TemplateFormViews
		'''
		wx.Frame.__init__( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 646,367 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.controller = controller
		self.loadDefault(parent)
		self.formviews = []
		self.required = []

	def loadDefault(self,parent):
		pass
	def generateFormView(self,parent,template,fromemail,responseid=None,responsedata=None):
		fv = TemplatesetViewForm(self.controller,parent,template,fromemail,responseid,responsedata)
		self.formviews.append(fv)
