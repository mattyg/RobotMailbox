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
	statustext = ''
	''' Text of the initial statusbar'''
	def __init__(self,controller,xrcpath):
		"""
		@param controller: the Controller that this View notifies and updates from.
		@type controller: L{Controller}
		@param xrcpath: the path to XRC template File
		@type xrcpath: String
		"""
		self.xrc = xrcpath
		self.controller = controller
		self.templatesetcontroller = self.controller.getTemplatesetController()
		self.evmailcontroller = self.controller.getEvmailController()
		self.app = wx.App(False)
		wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 646,367 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )	
		self.statusbar = None

	def start(self):
		self.loadDefault(self.xrc)
		self.populateMessages()
		self.app.MainLoop()	


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

		self.NewMessagesPanel = wx.Panel( self.OverheadNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		NewMesagesSizer = wx.BoxSizer( wx.VERTICAL )
		self.NewMessagesListCtrl = wx.ListCtrl( self.NewMessagesPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		NewMesagesSizer.Add( self.NewMessagesListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.NewMessagesPanel.SetSizer( NewMesagesSizer )
		self.NewMessagesPanel.Layout()
		NewMesagesSizer.Fit( self.NewMessagesPanel )
		self.OverheadNotebook.AddPage( self.NewMessagesPanel, u"New Messages", False )


		self.OverheadBoxSizer = wx.BoxSizer( wx.VERTICAL )
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText(self.statustext)
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
		reloadbutton = wx.MenuItem(self.File,wx.ID_ANY,"Update Inbox", wx.EmptyString,wx.ITEM_NORMAL)
		self.Bind(wx.EVT_MENU,self.updateMessages,id=reloadbutton.GetId())
		self.File.AppendItem(reloadbutton)
		
		reloadallbutton = wx.MenuItem(self.File,wx.ID_ANY,"Reload Inbox",wx.EmptyString,wx.ITEM_NORMAL)
		self.Bind(wx.EVT_MENU,self.reloadAllEmails,id=reloadallbutton.GetId())
		self.File.AppendItem(reloadallbutton)

		# add menu templates
		templatesets = self.templatesetcontroller.model.getAllTemplatesets()

		for each in templatesets:
			print "TEMPLATESET -",each
			# get all DEFAULT OUTGOING templates in templateset
			rows = self.templatesetcontroller.model.getDefaultTemplates(each.name,each.version)
			rcount = len(rows)
			if rcount> 1:
				tmenu = wx.Menu()
				self.New.AppendSubMenu(tmenu, each.name+' '+each.version)
			else:
				tmenu = self.New
			for template in rows:
				tplate = wx.MenuItem(tmenu, wx.ID_ANY, each['name']+'/'+template['name'], wx.EmptyString, wx.ITEM_NORMAL)
				tmenu.AppendItem(tplate)
				# bind events
				self.templatedata[tplate.GetId()] = template.id
				self.Bind(wx.EVT_MENU, self.newMessage,id=tplate.GetId())
				#self.Bind(wx.EVT_MENU, binds.newMessage,id=self.Templates[each.name+'/'+template.name].GetId())

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

	def populateMessages(self):
		'''
		1. get new imap messages
		2. get all active messages
		3. re-populate L{self.NewMessagesListCtrl} with messages
		@returns: the number of messages
		@rtype: Integer
		'''
		# 3. New messages to populate ListCtrl
		num_items = self.NewMessagesListCtrl.GetItemCount()
		emailcontroller = self.controller.getEmailController()
		if emailcontroller.offline is False:
			emailcontroller.addNewEmails()
		activesets = emailcontroller.model.getActiveEmails()
		for each in activesets:
			if each['templateset'] is not None and each['template'] != '':
				res = self.templatesetcontroller.model.getTemplateName(each['template'])
				if res is not None:
					tsname,tname = res[0],res[1]
				else:
					tsname='email'
			else:
				tsname = 'email'
			self.NewMessagesListCtrl.InsertStringItem(num_items, str(tsname))
			self.NewMessagesListCtrl.SetStringItem(num_items,1,each['subject'])
			personemail,personname = emailcontroller.model.getFromPerson(each['id'])
			self.NewMessagesListCtrl.SetStringItem(num_items,2,personemail+' '+personname)
			self.NewMessagesListCtrl.SetStringItem(num_items,3,each['date'])
			self.NewMessagesListCtrl.SetItemData(long(0),long(each['id']))
			self.NewMessagesListCtrl.GetItem(num_items,1).SetWidth(20000)
		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.viewMessage)

		self.SetSizer( self.OverheadBoxSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		self.Show()
		return len(activesets)

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
		count = self.populateMessages()
		self.SetStatusText(str(count)+" new messages added")

	def newMessage(self,event):
		'''
		Bind callback function from wx.MenuItem New > template message click
		'''
		evid = event.GetId()
		templateid = self.templatedata[evid]
		self.statusbar.SetStatusText(self.templatesetcontroller.generateFormView(self.OverheadNotebook, templateid))
	
	def SetStatusText(self,text):
		'''
		Set text of the frame statusbar
		@param text: Text to set StatusBar
		@type text: String
		'''
		if self.statusbar is not None:
			self.statusbar.SetStatusText(text)
		else:
			self.statustext = text
	def reloadAllEmails(self,event):
		''' Bind event to reload all emails from menu item'''
		self.controller.getEmailController().model.reloadAllEmails()
if __name__ == "__main__":
	View()
