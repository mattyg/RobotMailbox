# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class OverheadFrame
###########################################################################

class OverheadFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 646,367 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.OverheadMenu = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.New = wx.Menu()
		self.Letter = wx.MenuItem( self.New, wx.ID_ANY, u"Letter", wx.EmptyString, wx.ITEM_NORMAL )
		self.New.AppendItem( self.Letter )
		
		self.file.AppendSubMenu( self.New, u"New" )
		
		self.OverheadMenu.Append( self.file, u"File" ) 
		
		self.view = wx.Menu()
		self.OverheadMenu.Append( self.view, u"View" ) 
		
		self.SetMenuBar( self.OverheadMenu )
		
		self.OverheadToolBar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.NewMessageText = wx.StaticText( self.OverheadToolBar, wx.ID_ANY, u"Compose New  ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.NewMessageText.Wrap( -1 )
		self.OverheadToolBar.AddControl( self.NewMessageText )
		NewMessageChoiceChoices = [ u"Letter" ]
		self.NewMessageChoice = wx.Choice( self.OverheadToolBar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, NewMessageChoiceChoices, 0 )
		self.NewMessageChoice.SetSelection( 0 )
		self.NewMessageChoice.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		self.OverheadToolBar.AddControl( self.NewMessageChoice )
		self.OverheadToolBar.Realize()
		
		OverheadBoxSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.OverheadNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.NewMessagesPanel = wx.Panel( self.OverheadNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		NewMesagesSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.NewMessagesListCtrl = wx.ListCtrl( self.NewMessagesPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST )
		NewMesagesSizer.Add( self.NewMessagesListCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.NewMessagesPanel.SetSizer( NewMesagesSizer )
		self.NewMessagesPanel.Layout()
		NewMesagesSizer.Fit( self.NewMessagesPanel )
		self.OverheadNotebook.AddPage( self.NewMessagesPanel, u"New Messages", False )
		
		OverheadBoxSizer.Add( self.OverheadNotebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( OverheadBoxSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

