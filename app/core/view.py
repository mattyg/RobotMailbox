import wx
import wx.aui
import wx.lib.scrolledpanel
from wx import xrc

class View(wx.Frame):
	'''Base class for every View: it sends events to controller & recieves updates from controller'''
	controller = None
	'''The Controller that this View notifies and updates from.'''
	xrc = None
	"""The XRC xml resource File containing this view's default setup"""
	def __init__(self,controller,xrcpath):
		"""
		@param controller: the Controller that this View notifies and updates from.
		@type controller: L{Controller}
		@param xrcpath: the path to XRC template File
		@type xrcpath: String
		"""
		self.controller = controller
		self.templatesetcontroller = self.controller.getTemplatesetController()
		self.evmailcontroller = self.controller.getEvmailController()
		app = wx.App(False)
		wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 646,367 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.loadDefault(xrcpath)
		app.MainLoop()		

	def loadDefault(self,xrcpath):
		'''
		Load default view setup
		@param xrcpath: path to an .xrc file if one is being used
		@type xrcpath: String
		'''
		self.xrc = xrc.XmlResource(xrcpath)
		self.OverheadFrame = self.xrc.LoadFrame(None, 'OverheadFrame')
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		# create Notebook
		self.OverheadNotebook = wx.aui.AuiNotebook( self )
		self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.closePage, self.OverheadNotebook)

		self.NewMessagesPanel = wx.Panel( self.OverheadNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		NewMesagesSizer = wx.BoxSizer( wx.VERTICAL )
		self.NewMessagesListCtrl = wx.ListCtrl( self.NewMessagesPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		NewMesagesSizer.Add( self.NewMessagesListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.NewMessagesPanel.SetSizer( NewMesagesSizer )
		self.NewMessagesPanel.Layout()
		NewMesagesSizer.Fit( self.NewMessagesPanel )
		self.OverheadNotebook.AddPage( self.NewMessagesPanel, u"New Messages", False )


		self.OverheadBoxSizer = wx.BoxSizer( wx.VERTICAL )
		self.statusbar = wx.StatusBar(self.OverheadFrame)
		self.statusbar.SetFields(['what','huh','whats teh deal'])
		subbox2 = wx.BoxSizer(wx.HORIZONTAL)
		subbox2.Add(self.statusbar,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		self.OverheadBoxSizer.Add( self.OverheadNotebook, 1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=0 )
		self.OverheadBoxSizer.Add(subbox2, flag=wx.EXPAND|wx.RIGHT, border=2)

		# create Menu
		self.OverheadMenu = wx.MenuBar( 0 )
		self.File = wx.Menu()
		self.New = wx.Menu()
		self.Templates = {}
		self.Templatesets = {}
		self.templatedata = {}

		# add menu reload item
		reloadbutton = wx.MenuItem(self.New,wx.ID_ANY,"Update Inbox", wx.EmptyString,wx.ITEM_NORMAL)
		self.Bind(wx.EVT_MENU,self.updateMessages,id=reloadbutton.GetId())
		self.File.AppendItem(reloadbutton)

		# add menu templates
		templatesets = self.templatesetcontroller.getAllTemplatesets()

		for each in templatesets:
			print "TEMPLATESET -",each
			# get all DEFAULT OUTGOING templates in templateset
			rows = self.templatesetcontroller.getDefaultTemplates(each.name,each.version)
			rcount = len(rows)
			if rcount> 1:
				self.Templatesets[each.name] = wx.Menu()
				self.New.AppendSubMenu(self.Templatesets[each.name], each.name)
				for template in rows:
					self.Templates[each['name']+'/'+template['name']] = wx.MenuItem(self.Templatesets[each.name], wx.ID_ANY, each['name']+'/'+template['name'], wx.EmptyString, wx.ITEM_NORMAL)
					self.Templatesets[each.name].AppendItem(self.Templates[each.name+'/'+template.name])
					# bind events
					self.templatedata[self.Templates[each.name+'/'+template.name].GetId()] = (each['name'],template['name'])
					self.Bind(wx.EVT_MENU, self.newMessage,id=self.Templates[each.name+'/'+template.name].GetId())
					#self.Bind(wx.EVT_MENU, binds.newMessage,id=self.Templates[each.name+'/'+template.name].GetId())
			elif rcount == 1:
				for template in rows:
					tkey = str(each.name)+'/'+str(template.name)	
					setname = each.name
					templatename = template.name
					self.Templates[tkey] = wx.MenuItem(self.New,wx.ID_ANY,each.name+'/'+template.name,wx.EmptyString,wx.ITEM_NORMAL)
					self.New.AppendItem(self.Templates[tkey])

					# bind events
					self.templatedata[self.Templates[each.name+'/'+template.name].GetId()] = (each['name'],template['name'])
					self.Bind(wx.EVT_MENU,self.newMessage, id=self.Templates[tkey].GetId())
					#self.Bind(wx.EVT_MENU, Binds.Menu.New.Message,id=self.Templates[each.name+'/'+template.name].GetId())

		self.File.AppendSubMenu( self.New, u"New" )		
		self.OverheadMenu.Append( self.File, u"File" ) 
		
		self.view = wx.Menu()
		self.OverheadMenu.Append( self.view, u"View" ) 
		
		self.SetMenuBar( self.OverheadMenu )
		
		
		
		# 2. columns for NewMessagesListCtrl
		self.NewMessagesListCtrl.InsertColumn(0,"Type")
		self.NewMessagesListCtrl.InsertColumn(1,"Subject")
		self.NewMessagesListCtrl.InsertColumn(3,"Date & Time")
		self.NewMessagesListCtrl.InsertColumn(2,"From")
		self.NewMessagesListCtrl.SetColumnWidth(0, 50)
		self.NewMessagesListCtrl.SetColumnWidth(1, 500)
		self.NewMessagesListCtrl.SetColumnWidth(2, 300)
		self.NewMessagesListCtrl.SetColumnWidth(3, 500)
		self.populateMessages()

	def populateMessages(self):
		'''
		1. get new imap messages
		2. get all active messages
		3. re-populate L{self.NewMessagesListCtrl} with messages
		'''
		# 3. New messages to populate ListCtrl
		num_items = self.NewMessagesListCtrl.GetItemCount()
		emailcontroller = self.controller.getEmailController()
		emailcontroller.addNewEmails()
		activemessages = emailcontroller.getActiveEmails()
		for each in activemessages:
			if len(each['templateset'].strip()) > 0:
				print "getTemplateName",each['template']
				tsname,tname = self.templatesetcontroller.getTemplateName(each['template'])
			else:
				tsname = 'email'
			self.NewMessagesListCtrl.InsertStringItem(num_items, str(tsname))
			self.NewMessagesListCtrl.SetStringItem(num_items,1,each['subject'])
			personemail,personname = emailcontroller.getFromPerson(each['id'])
			self.NewMessagesListCtrl.SetStringItem(num_items,2,personemail+' '+personname)
			self.NewMessagesListCtrl.SetStringItem(num_items,3,each['date'])
			self.NewMessagesListCtrl.SetItemData(long(0),long(each['id']))
			
		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.viewMessage)

		self.SetSizer( self.OverheadBoxSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		self.Show()

	def closePage(self, event):
		'''
		Close the page on gtk where it FAILS
		??
		'''
		page = self.nb.GetPage(self.nb.GetSelection())
	
	def viewMessage(self,event):
		'''
		Bind callback function from wx.ListItem click. 
		'''
		item = event.GetItem()
		messageid = int(item.GetData())
		self.evmailcontroller.generateMessageView(self.OverheadNotebook, messageid)

	def updateMessages(self,event):
		'''
		Bind callback function from wx.MenuItem "Update Messages" click
		'''
		self.NewMessagesListCtrl.DeleteAllItems()
		self.populateMessages()

	def newMessage(self,event):
		'''
		Bind callback function from wx.MenuItem New > template message click
		'''
		evid = event.GetId()
		print self.templatedata[evid]
		setname = self.templatedata[evid][0]
		name = self.templatedata[evid][1]

		statustext = self.templatesetcontroller.generateFormView(self.OverheadNotebook, setname,name,None)
		#self.statusbar =
