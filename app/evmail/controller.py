from app.core import settings
from library import validictory
from library import simplejson
from tempfile import NamedTemporaryFile
from simplejson.decoder import JSONDecodeError
from validictory.validator import SchemaError
from app.evmail.model import EvmailModel
from app.evmail.view import EvmailView
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.utils import formatdate
import json

class EvmailError(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

class EvmailController:
	controller = None
	'''Parent core controller'''
	def __init__(self,controller):
		self.controller = controller
		self.templatesetcontroller = self.controller.getTemplatesetController()
		'''@ivar: templateset controller''' 
		self.model = EvmailModel(self,settings.DB_PATH)
		'''@ivar: Evmail Model'''
		self.view = EvmailView(self)
		'''@ivar: Evmail View'''

	def getEvmailTemplate(self,setname,name,version):
		'''
		Get schema data of particular template file within a particular template set.
		@param setname: Name of the templateset
		@type setname: string
		@param name: Name of the template
		@type name: string
		@param version: Version of the templateset
		@type version: string
		@returns: dict with template schema data
		'''
		
		try:
			templatefile = open(settings.TEMPLATESETS_PATH+setname+'/'+version+'/templates/'+name,'r')
		except IOError:
			raise IOError, "Template not found ("+tspath+'templates/'+name+")"
		
		try:
			templatedata = simplejson.load(templatefile)
		except JSONDecodeError, e:
			raise EvmailError("simplejson.load( "+tspath+'templates/'+name+" ) raised JSONDecodeError")

		return templatedata


	def processEvmail(self,evmail):
		'''
		Read meta information, determine proper templateset, download (or find) templateset, and validate to it
		and add it to the database
		@param evmail: Contents of evmail json file
		@type evmail: String
		'''
		setname,name,version,messagesetid = self.readEvmail(evmail)
		templateschema = self.getEvmailTemplate(setname,name,version)
		
		try:
			evmail = simplejson.loads(evmail)
		except:
			print "evmail JSON Decoding error: ",e
			raise EvmailError("simplejson.load( config.json ) raised JSONDecodeError")
		
		try:
			validictory.validate(evmail,templateschema)
		except SchemaError, e:
			print "config.json Schema validation error: ",e
			raise TemplatesetError("validictory.validate( config.json, config-schema.json) raised SchemaError")

		return setname,name,version,messagesetid
		

	def readEvmail(self,evmail):
		'''
		Read meta information from Evmail string
		@returns: tuple of (setname,name,version)
		@param evmail: Contents of evmail json file
		@type evmail: String
		'''
		try:
			evmaildata = simplejson.loads(evmail)
		except JSONDecodeError, e:
			print "evmail JSON Decoding error: ",e
			raise EvmailError("simplejson.loads( evmail ) raised JSONDecodeError")
			
		return str(evmaildata['hide']['setname']),str(evmaildata['hide']['name']),str(evmaildata['hide']['version']),str(evmaildata['hide']['messagesetid'])

		
	def validateEvmail(self,evmaildata,templateschema):
		'''
		Validate Evmail to schema in templateset
		@param evmaildata: data object of evmail json file
		@type evmaildata: Dict
		@param schemapath: path to the templateset template specific to this evmail message
		@type schemapath: String
		'''
		try:
			validictory.validate(evmaildata,templateschema)
			return True
		except SchemaError, e:
			raise Exception,e

	def generateMessage(self,template,data,subject,tos,fromemail):
		'''
		Generate  MimeMultipart message from message data
		@param data: evmail message data
		@type data: Dict
		@param subject: message subject
		@type subject: String
		@param tos: list of people to send the message to
		@type tos: List
		@param fromemail: email of sender
		@type fromemail: String
		@return: message
		@rtype: MIMEMultipart		
		'''
		message = MIMEMultipart()
		message['To'] = tos
		message['From'] = fromemail
		message['Date'] = formatdate(localtime=True)
		message['Subject'] = subject

		# validate message data from template
		res = self.validateEvmail(message,template) 
		if res is not True:
			raise Exception,res
		'''fail = False
		failtext = []
		for each in template['hide']:
			if template['hide'][each].__contains__('required'):
				if template['hide'][each]['required'] == True:
					if not data['hide'].__contains__(each):
						fail = True
						failtext.append(each+' is required')
					elif data['hide'][each] == '':
						fail = True
						failtext.append(each+' is required')
		for each in template['show']:
			if template['show'][each].__contains__('required'):
				if template['show'][each]['required'] == True:
					if not data['show'].__contains__(each):
						fail = True
						failtext.append(each+' is required')
					elif data['show'][each] == '':
						fail = True
						failtext.append(each+' is required')'''
					
		# generate text from data
		text = []
		for each in data['show']:
			text.append(each+": "+data['show'][each])
		text = "\n\n".join(text)
		message.attach(MIMEText(str(text)))

		# attach data file
		datastr = json.dumps(data)
		part = MIMEBase('application', "json")
		part.set_payload(datastr)
		part.add_header('Content-Disposition', 'attachment; filename="meta.json"')
		message.attach(part)

		return message

	def generateMessageView(self,notebook,messageid):
		'''
		Generate message view for message with messageid
		@param notebook: the wx.NoteBook to send along to generateMessageView
		@type notebook: wx.Notebook
		@param messageid: id of message to view
		@type messageid: Integer
		'''
		# get message data
		message = self.model.getMessage(messageid)
		froms = self.model.getMessageFroms(messageid)
		tos = self.model.getMessageTos(messageid)
		# generate message view
		self.view.generateMessageView(notebook,message,froms,tos)

	def generateResponseHideData(self,responseto=None):
		return self.model.generateResponseHideData(responseto)
