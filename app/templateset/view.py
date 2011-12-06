import wx
import wx.lib.masked
import json


class TemplatesetViewForm:
	def __init__(self,controller,notebook,template,fromemail,response=None):
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
		self.response = response
		self.controller = controller
		self.template = template
		self.show = {}
		self.hide = {}
		self.fromemail = fromemail
		self.todata = []
		self.notebook = notebook
		self.panel = wx.lib.scrolledpanel.ScrolledPanel( notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel.SetupScrolling()

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.generateFormLabel(self.panel,hbox2,"To")
		self.to = wx.TextCtrl(self.panel, wx.ID_ANY,size=(600,100),style=wx.TE_MULTILINE)
		hbox2.Add(self.to)
		self.vbox.Add(hbox2,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))
		self.subject = ''
		print template
		self.generateElements(template['show'])
		self.generateEndButton()

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
				if each.__contains__('mapsto'):
					if each['mapsto'] == 'subject':
						self.subject = each
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
							hbox = self.generateFormElement(self.panel,hbox,name,each['type'],'date')
							hbox = self.generateFormElement(self.panel,hbox,name,each['type'],'time')
						else:
							hbox = self.generateFormElement(self.panel,hbox,name,itemsdata[each]['type'],format)
				else:
					hbox = self.generateFormLabel(self.panel,hbox,name)
			elif isinstance(itemsdata[each],str):
				self.required = True
			self.vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
			self.vbox.Add((-1,10))
		


	def generateElements(self,itemsdata):
		'''
		Genearte form elements in an array data structure
		@param itemsdata: Items data of elements in array
		@type itemsdata: List
		'''
		for each in itemsdata:
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			if isinstance(itemsdata[each],dict):
				if itemsdata[each].__contains__('mapsto'):
					if itemsdata[each]['mapsto'] == 'subject':
						self.subject = each
				if itemsdata[each].__contains__('type'):
					# add widget based on type & format
					if itemsdata[each]['type'] == 'object':
						if itemsdata[each].__contains__('properties'):
							self.generateElements(itemsdata[each]['properties'])
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
							hbox = self.generateFormElement(self.panel,hbox,each,itemsdata[each]['type'],'date')
							hbox = self.generateFormElement(self.panel,hbox,each,itemsdata[each]['type'],'time')
						else:
							hbox = self.generateFormElement(self.panel,hbox,each,itemsdata[each]['type'],format)
				else:
					hbox = self.generateFormLabel(self.panel,hbox,each)
			elif isinstance(itemsdata[each],str):
				self.required = True
			print hbox
			self.vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
			self.vbox.Add((-1,10))

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

	def readHideData(self,response=None):
		'''
		read hide data
		@param response: response data
		@type response: Dict
		'''
		if response is None:
			self.hide = self.controller.controller.getEvmailController().model.generateNewHideData(self.template['hide']['setname'],self.template['hide']['name'],self.template['hide']['version'])
		else:
			self.hide = self.controller.controller.getEvmailController().model.generateResponseHideData(response)

	def readData(self):
		'''
		Read the information populating the form widgets
		@return: the form data
		@rtype: Dict
		'''
		data = {}
		data['show'] = {}
		for each in self.show:
			if isinstance(self.show[each],wx.DatePickerCtrl):
				value = self.show[each].GetValue()
			elif isinstance(self.show[each],wx.TextCtrl):
				pos = self.show[each].GetLastPosition()
				value = self.show[each].GetString(0,pos)
				data['show'][each] = value
			elif isinstance(self.show[each],wx.lib.masked.TimeCtrl):
				value = self.show[each].GetValue(as_wxDateTime=True)
				data['show'][each] = value
			elif isinstance(self.show[each],wx.ColourPickerCtrl):
				value = self.show[each].GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
				data['show'][each] = value

		# generate / retrieve hide data
		self.readHideData(self.response)
		data['hide'] = self.hide		
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
		return data


	def onSendButton(self,event):
		'''
		Bind response to sending message
		'''
		# get data to send		
		data = self.readData()
		# generate message
		print data
		message = self.controller.controller.getEvmailController().generateMessage(data,self.subject,self.todata,self.fromemail)
		# add to database
		'''datastr = json.dumps(data)
		self.controller.getEmailController().addMessage(data['hide']['setname']+'/'+data['hide']['name'],subject,text,message['Date'],tos,fromemail,fromemail,message['Message-ID'],datastr,0)'''
		# send message
		try:
			self.controller.controller.getEmailController().sendMessage(self.fromemail,self.todata,message)
			# CLOSE TAB
			print "controller",self.controller
			print "parent controller",self.controller.controller
			print "parent controller view",self.controller.controller.view
			self.controller.controller.SetStatusText("Message sent to "+str(self.todata))
			selected = self.notebook.GetSelection()
			self.notebook.DeletePage(selected)
			return "Message Sent."
		except Exception, e:
			self.controller.controller.SetStatusText("Message sent to "+str(self.todata))
			return "Message sending failed."



	def generateFormElement(self,panel,boxsizer,name,ttype,format=None):
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
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
				elif format == 'time':
					item = wx.lib.masked.TimeCtrl(panel, wx.ID_ANY)
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
				elif format == 'color':
					item = wx.ColourPickerCtrl(panel, wx.ID_ANY)
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
				elif format == 'phone':
					item = wx.TextCtrl(panel, wx.ID_ANY,size=(200,30))
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10)
				elif format == 'short':
					item = wx.TextCtrl(panel, wx.ID_ANY,size=(200,30))
					self.show[name] = item
					boxsizer.Add(item,flag=wx.RIGHT,border=10) 
		
			else:
				item = wx.TextCtrl(panel, wx.ID_ANY,size=(600,400),style=wx.TE_MULTILINE)
				self.show[name] = item
				boxsizer.Add(item,flag=wx.RIGHT,border=10)
		return boxsizer

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
	def generateFormView(self,parent,template,fromemail,response=None):
		fv = TemplatesetViewForm(self.controller,parent,template,fromemail,response)
		self.formviews.append(fv)
