///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Sep  8 2010)
// http://www.wxformbuilder.org/
//
// PLEASE DO "NOT" EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#ifndef __noname__
#define __noname__

#include <wx/string.h>
#include <wx/bitmap.h>
#include <wx/image.h>
#include <wx/icon.h>
#include <wx/menu.h>
#include <wx/gdicmn.h>
#include <wx/font.h>
#include <wx/colour.h>
#include <wx/settings.h>
#include <wx/aui/auibook.h>
#include <wx/listctrl.h>
#include <wx/sizer.h>
#include <wx/frame.h>
#include <wx/stattext.h>
#include <wx/choice.h>
#include <wx/toolbar.h>

///////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////
/// Class MyFrame1
///////////////////////////////////////////////////////////////////////////////
class MyFrame1 : public wxFrame 
{
	private:
	
	protected:
		wxMenuBar* m_menubar1;
		wxMenu* file;
		wxMenu* New;
		wxMenu* view;
		wxAuiNotebook* OverheadNotebook;
		wxListCtrl* m_listCtrl5;
	
	public:
		
		MyFrame1( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxEmptyString, const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 646,367 ), long style = wxDEFAULT_FRAME_STYLE|wxTAB_TRAVERSAL );
		~MyFrame1();
	
};

///////////////////////////////////////////////////////////////////////////////
/// Class MyToolBar1
///////////////////////////////////////////////////////////////////////////////
class MyToolBar1 : public wxToolBar 
{
	private:
	
	protected:
		wxStaticText* ComposeNew;
		wxChoice* MessageType;
	
	public:
		
		MyToolBar1( wxWindow* parent, wxWindowID id = wxID_ANY, const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = 0 );
		~MyToolBar1();
	
};

#endif //__noname__
