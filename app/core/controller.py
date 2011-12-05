from app.core import settings
from app.core.view import View
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
		self.emailcontroller = EmailController(self,settings.IMAP_HOST,settings.IMAP_PORT,settings.IMAP_USER,settings.IMAP_PASS,ssl=True)
		self.templatesetcontroller = TemplatesetController(self)
		self.evmailcontroller = EvmailController(self)
		#self.emailcontroller.model.reloadAllEmails()
		view = View(self,settings.XRC_PATH)
	
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


if __name__ == "__main__":
	Controller()
