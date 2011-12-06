from app.core import settings
from app.core.view import View
from app.core.model import Model
from app.email.controller import EmailController
from app.evmail.controller import EvmailController
from app.email.controller import EmailController
from app.templateset.controller import TemplatesetController

class Controller:
	'''
	Core controller class
	'''
	emailcontroller = None
	'''Child Email Controller'''
	templatesetcontroller = None
	''' Child Templateset Controller'''
	evmailcontroller = None
	''' Child evmail Controller'''
	view = None
	''' core View'''
	def __init__(self):
		'''
		Initialize core Controller -- links all controllers, models & views together
		'''
		print "views"
		self.emailcontroller = EmailController(self,settings.IMAP_HOST,settings.IMAP_PORT,settings.IMAP_USER,settings.IMAP_PASS,ssl=True)
		self.templatesetcontroller = TemplatesetController(self)
		self.evmailcontroller = EvmailController(self)
		self.templatesetcontroller.model.reloadAll()
		self.view = View(self,settings.XRC_PATH)
		self.view.start()
		self.view.SetStatusText('Welcome to RobotMailbox')

	
	def getTemplatesetController(self):
		'''
		@return: core instance of TemplatesetController
		@rtype: L{TemplatesetController}
		'''
		return self.templatesetcontroller

	def getEmailController(self):
		'''
		@return: core instance of EmailController
		@rtype: L{EmailController}
		'''		
		return self.emailcontroller

	def getEvmailController(self):
		'''
		@return: core instance of EvmailController
		@rtype: L{EvmailController}
		'''
		return self.evmailcontroller

	def SetStatusText(self,text):
		'''
		forward setting status text function to model
		@param text: new status text
		@type text: String
		'''
		self.view.statusbar.SetStatusText(text)

if __name__ == "__main__":
	Controller()
