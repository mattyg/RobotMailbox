import wx
import wx.html
from library import simplejson

class EvmailView:
	def __init__(self,controller):
		'''
		Initialize view of Evmail Messages
		'''
		self.controller = controller

	def generateMessageSizer(self,panel,message,froms,tos=None):
		boldfont = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
		sizerlist = []
		#item, proportion=0, flag=0, border=0, userData=None

		# add Subject
		label = wx.StaticText(panel,wx.ID_ANY,label='Subject:')
		label.SetFont(boldfont)
		sizerlist.append((label,0,wx.RIGHT,10))
		stext = wx.StaticText(panel, wx.ID_ANY, label=str(message['subject']))
		sizerlist.append((stext,0,wx.RIGHT,10))

		# add Froms
		label = wx.StaticText(panel,wx.ID_ANY,label='From:')
		label.SetFont(boldfont)
		
		sizerlist.append((label,0,wx.RIGHT,10))
		etext = wx.StaticText(panel,wx.ID_ANY,label=froms)
		sizerlist.append((etext,0,wx.RIGHT,10))

		# add Tos
		if tos is not None:
			label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label='To:')
			label.SetFont(boldfont)
		
			sizerlist.append((label,0,wx.RIGHT,10))
			etext = wx.StaticText(panel,wx.ID_ANY,label=tos)
			sizerlist.append((etext,0,wx.RIGHT,10))
	
		# add Date/time
		label = wx.StaticText(panel,wx.ID_ANY,label='Date:')
		label.SetFont(boldfont)
		sizerlist.append((label,0,wx.RIGHT,10))
		statictext = wx.StaticText(panel,wx.ID_ANY,label=message['date'])
		sizerlist.append((statictext,0,wx.RIGHT,10))

		# add content
		if message['template'] is None:
			# add Content
			label = wx.StaticText(panel,wx.ID_ANY,label='Body:')
			label.SetFont(boldfont)
		
			sizerlist.append((label,0,wx.RIGHT,10)) 
			#text = wx.html.HtmlWindow(self.ViewMessagePanel)
			text = wx.StaticText(panel,label=message['body'])
			#text.LoadPage(message['body'])
			sizerlist.append((text,0,wx.RIGHT,10))
		elif message['evmail'] != '':
			# add Content
			evmail = simplejson.loads(message['evmail'])
			for each in evmail['show']:
				label = wx.StaticText(panel,wx.ID_ANY,label=each+':')
				label.SetFont(boldfont)
		
				sizerlist.append((label,0,wx.RIGHT,10))
				etext = wx.StaticText(panel,wx.ID_ANY,label=evmail['show'][each])
				sizerlist.append((etext,0,wx.RIGHT,10))
		return sizerlist

	def generateMessageView(self,notebook):
		''' initiate generateMessageView
		@param notebook: notebook to add message tab to
		@type notebook: wx.Notebook
		'''
		self.notebook = notebook

		self.ViewMessagePanel = wx.lib.scrolledpanel.ScrolledPanel( notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.ViewMessagePanel.SetupScrolling()
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		return self.ViewMessagePanel,self.vbox

	def generateMessageViewPart(self,panel,vbox,message,froms,tos):
		'''
		Generate Evmail Message view panel
		@param panel:  the panel to add to
		@type panel: wx.Panel
		@param message: the message from database
		@type message: List
		@param froms: list of persons who sent the email
		@type froms: List
		@param tos: list of persons who recieved the email
		@type tos: List
		'''
		self.vbox = vbox
		boldfont = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		if message['template'] is not None and message['template'] != '':
			messagedata = simplejson.loads(message['evmail'])
			choiceids = self.controller.controller.getTemplatesetController().model.getResponseTemplates(message['template'])
			if len(choiceids) > 0:			
				responsechoice = wx.Choice(panel,choices=[])
				for each in choiceids:
					setname,templatename = self.controller.controller.getTemplatesetController().model.getTemplateName(each)
					responsechoice.Append(templatename,(message['id'],setname))
				panel.Bind(wx.EVT_CHOICE,self.responseMessage)
				hbox.Add(responsechoice,flag=wx.RIGHT,border=10)
				self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		else:
			templatesetctrl = self.controller.controller.getTemplatesetController()
			choiceids = templatesetctrl.model.getResponseTemplates(templatesetctrl.model.hasTemplate('discussion','message'))
			if len(choiceids) > 0:
				responsechoice = wx.Choice(panel,choices=[])
				for each in choiceids:
					setname,templatename = templatesetctrl.model.getTemplateName(each)
					responsechoice.Append(templatename,(message['id'],setname))
				panel.Bind(wx.EVT_CHOICE,self.responseMessage)
				hbox.Add(responsechoice,flag=wx.RIGHT,border=10)
				self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		
		

		# add message type
		if message['template'] is not None and message['template'] != '':
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			label = wx.StaticText(panel,wx.ID_ANY,label='Type:')
			label.SetFont(boldfont)
			hbox.Add(label,flag=wx.RIGHT, border=10)
			stext = wx.StaticText(panel, wx.ID_ANY, label=str(message['template']))
			hbox.Add(stext,flag=wx.RIGHT,border=10)
			self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		# add Subject
		label = wx.StaticText(panel,wx.ID_ANY,label='Subject:')
		label.SetFont(boldfont)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		hbox.Add(wx.StaticText(panel, wx.ID_ANY, label=message['subject']), flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))

		# add Froms
		label = wx.StaticText(panel,wx.ID_ANY,label='From:')
		label.SetFont(boldfont)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		for each in froms:
			hbox.Add(wx.StaticText(panel,wx.ID_ANY,label=each['email']),flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))

		# add Tos
		label = wx.StaticText(panel,wx.ID_ANY,label='To:')
		label.SetFont(boldfont)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		for each in tos:
			hbox.Add(wx.StaticText(panel,wx.ID_ANY,label=each['email']),flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))
	
		# add Date/time
		label = wx.StaticText(panel,wx.ID_ANY,label='Date:')
		label.SetFont(boldfont)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		hbox.Add(wx.StaticText(panel,wx.ID_ANY,label=message['date']),flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))

		# add content
		if message['templateset'] == '':
			# add Content
			label = wx.StaticText(panel,wx.ID_ANY,label='Body:')
			label.SetFont(boldfont)
		
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			hbox.Add(label,flag=wx.RIGHT,border=10)
			#text = wx.html.HtmlWindow(self.ViewMessagePanel)
			text = wx.StaticText(panel,label=message['body'])
			#text.LoadPage(message['body'])
			hbox.Add(text,flag=wx.RIGHT,border=10)
			self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
			self.vbox.Add((-1,10))
		elif message['evmail'] != '':
			# add Content
			evmail = simplejson.loads(message['evmail'])
			for each in evmail['show']:
				label = wx.StaticText(panel,wx.ID_ANY,label=each+':')
				label.SetFont(boldfont)
		
				hbox = wx.BoxSizer(wx.HORIZONTAL)
				hbox.Add(label,flag=wx.RIGHT,border=10)
				hbox.Add(wx.StaticText(panel,wx.ID_ANY,label=evmail['show'][each]),flag=wx.RIGHT,border=10)
				self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
				self.vbox.Add((-1,10))
		vbox = self.vbox
		return vbox
		
	def responseMessage(self,event):
		'''
		Create response message bound to 'responsd' click
		'''
		messageid,setname = event.GetClientData()
		msg = self.controller.model.getMessageData(messageid)
		name = event.GetString()
		templateid = self.controller.controller.getTemplatesetController().model.hasTemplate(setname,name)
		self.controller.controller.getTemplatesetController().generateFormView(self.notebook,templateid,messageid,msg)
