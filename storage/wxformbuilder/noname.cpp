///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Sep  8 2010)
// http://www.wxformbuilder.org/
//
// PLEASE DO "NOT" EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "noname.h"

///////////////////////////////////////////////////////////////////////////

MyFrame1::MyFrame1( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );
	
	m_menubar1 = new wxMenuBar( 0 );
	file = new wxMenu();
	New = new wxMenu();
	wxMenuItem* Letter;
	Letter = new wxMenuItem( New, wxID_ANY, wxString( wxT("Letter") ) , wxEmptyString, wxITEM_NORMAL );
	New->Append( Letter );
	
	file->Append( -1, wxT("New"), New );
	
	m_menubar1->Append( file, wxT("File") ); 
	
	view = new wxMenu();
	m_menubar1->Append( view, wxT("View") ); 
	
	this->SetMenuBar( m_menubar1 );
	
	wxFlexGridSizer* fgSizer1;
	fgSizer1 = new wxFlexGridSizer( 2, 2, 0, 0 );
	fgSizer1->SetFlexibleDirection( wxBOTH );
	fgSizer1->SetNonFlexibleGrowMode( wxFLEX_GROWMODE_SPECIFIED );
	
	OverheadNotebook = new wxAuiNotebook( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxAUI_NB_DEFAULT_STYLE|wxAUI_NB_TAB_MOVE );
	
	fgSizer1->Add( OverheadNotebook, 1, wxALL|wxALIGN_CENTER_HORIZONTAL|wxEXPAND, 5 );
	
	m_listCtrl5 = new wxListCtrl( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxLC_ICON );
	fgSizer1->Add( m_listCtrl5, 0, wxALL, 5 );
	
	this->SetSizer( fgSizer1 );
	this->Layout();
	
	this->Centre( wxBOTH );
}

MyFrame1::~MyFrame1()
{
}

MyToolBar1::MyToolBar1( wxWindow* parent, wxWindowID id, const wxPoint& pos, const wxSize& size, long style ) : wxToolBar( parent, id, pos, size, style )
{
	ComposeNew = new wxStaticText( this, wxID_ANY, wxT("Compose New  "), wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT );
	ComposeNew->Wrap( -1 );
	AddControl( ComposeNew ); 
	wxString MessageTypeChoices[] = { wxT("Letter") };
	int MessageTypeNChoices = sizeof( MessageTypeChoices ) / sizeof( wxString );
	MessageType = new wxChoice( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, MessageTypeNChoices, MessageTypeChoices, 0 );
	MessageType->SetSelection( 0 );
	MessageType->SetFont( wxFont( wxNORMAL_FONT->GetPointSize(), 70, 90, 90, false, wxEmptyString ) );
	AddControl( MessageType );
	
	Realize();
}

MyToolBar1::~MyToolBar1()
{
}
