import wx
import wx.html
from library import simplejson

class EvmailView:
	def __init__(self,controller):
		'''
		Initialize view of Evmail Messages
		'''
		self.controller = controller

	def generateMessageView(self,notebook,message,froms,tos):
		'''
		Generate Evmail Message view panel
		@param notebook: the notebook to add the panel to
		@type notebook: wx.Notebook
		@param message: the message from database
		@type message: List
		@param froms: list of persons who sent the email
		@type froms: List
		@param tos: list of persons who recieved the email
		@type tos: List
		'''
		self.notebook = notebook
		boldfont = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)

		self.ViewMessagePanel = wx.lib.scrolledpanel.ScrolledPanel( notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.ViewMessagePanel.SetupScrolling()
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		if message['templateset'] == '':
			templatesetctrl = self.controller.controller.getTemplatesetController()
			choiceids = templatesetctrl.getResponseTemplates(templatesetctrl.model.hasTemplate('discussion','message'))
			responsechoice = wx.Choice(self.ViewMessagePanel,choices=[])
			for each in choiceids:
				setname,templatename = templatesetctrl.getTemplateName(each)
				responsechoice.Append(templatename,(None,setname))		

			self.ViewMessagePanel.Bind(wx.EVT_CHOICE,self.responseMessage)
			hbox.Add(responsechoice,flag=wx.RIGHT,border=10)
			self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		elif message['evmail'] != '':
			messagedata = simplejson.loads(message['evmail'])
			choiceids = self.controller.controller.getTemplatesetController().getResponseTemplates(message['template'])
			responsechoice = wx.Choice(self.ViewMessagePanel,choices=[])
			for each in choiceids:
				setname,templatename = self.controller.controller.getTemplatesetController().getTemplateName(each)
				responsechoice.Append(templatename,(messagedata,setname))

			self.ViewMessagePanel.Bind(wx.EVT_CHOICE,self.responseMessage)
			hbox.Add(responsechoice,flag=wx.RIGHT,border=10)
			self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		

		# add Subject
		label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label='Subject:')
		label.SetFont(boldfont)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		hbox.Add(wx.StaticText(self.ViewMessagePanel, wx.ID_ANY, label=message['subject']), flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))

		# add Froms
		label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label='From:')
		label.SetFont(boldfont)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		for each in froms:
			hbox.Add(wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label=each['email']),flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))

		# add Tos
		label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label='To:')
		label.SetFont(boldfont)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		for each in tos:
			hbox.Add(wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label=each['email']),flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))
	
		# add Date/time
		label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label='Date:')
		label.SetFont(boldfont)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(label,flag=wx.RIGHT,border=10)
		hbox.Add(wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label=message['date']),flag=wx.RIGHT,border=10)
		self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.vbox.Add((-1,10))

		# add content
		if message['templateset'] == '':
			# add Content
			label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label='Body:')
			label.SetFont(boldfont)
		
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			hbox.Add(label,flag=wx.RIGHT,border=10)
			#text = wx.html.HtmlWindow(self.ViewMessagePanel)
			text = wx.StaticText(self.ViewMessagePanel,label=message['body'])
			#text.LoadPage(message['body'])
			hbox.Add(text,flag=wx.RIGHT,border=10)
			self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
			self.vbox.Add((-1,10))
		elif message['evmail'] != '':
			# add Content
			evmail = simplejson.loads(message['evmail'])
			for each in evmail['show']:
				label = wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label=each+':')
				label.SetFont(boldfont)
		
				hbox = wx.BoxSizer(wx.HORIZONTAL)
				hbox.Add(label,flag=wx.RIGHT,border=10)
				hbox.Add(wx.StaticText(self.ViewMessagePanel,wx.ID_ANY,label=evmail['show'][each]),flag=wx.RIGHT,border=10)
				self.vbox.Add(hbox,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
				self.vbox.Add((-1,10))
		
		self.ViewMessagePanel.SetSizer(self.vbox)

		notebook.AddPage( self.ViewMessagePanel, message['subject'], False )
		pcount = notebook.GetPageCount()
		notebook.SetSelection(pcount-1)

	def responseMessage(self,event):
		'''
		Create response message bound to 'response' click
		'''
		messagedata,setname = event.GetClientData()
		name = event.GetString()
		self.controller.controller.getTemplatesetController().generateFormView(self.notebook,setname,name,None,messagedata)
