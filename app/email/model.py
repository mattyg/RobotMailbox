from app.core.model import Model
from pysqlite2.dbapi2 import IntegrityError
import email

'''
db.define_table('person', Field('email','string'), Field('name','string'))
db.define_table('attachment', Field('name','string',uploadfolder=settings.BASE_PATH+'files/'))
db.define_table('message', Field('subject','string'), Field('body','text'), Field('date','text'), Field('from', db.person), Field('to',db.person), Field('cc',db.person), Field('bcc',db.person), Field('metajson','upload',uploadfield=True), Field('attachments', db.attachment))


db.define_table('template', Field('file','upload',uploadfield=True), Field("to","string",default=None,comment="{sender|recievers}"), Field("use","string",comment="{default|option}"), Field("responses", 'reference template'))
db.define_table('templateset', Field('name','string'), Field('version','string'), Field('templates', db.template))
'''

class EmailModel(Model):
	def __init__(self,controller,db):
		"""Initialize class for all EmailModels
		@param controller: The parent EmailController
		@type controller: L{Controller}	
		@param db: path to database
		@type db: String
		"""
		Model.__init__(self,controller,db)
		self.controller = controller
		
	
	def addPerson(self,email,name=""):
		'''
		Add person (name & email) to db
		@param email: person's email
		@type email: String
		@param name: persons name
		@type name: String
		@return:  new person id
		'''
		try:
			personid = self.db.person.insert(email=email,name=name)
		except IntegrityError:
			# "Person already exists in database", get their id			
			s = self.db(self.db.person.email==email).select()
			return s[0].id
		else:
			self.db.commit()
			return personid


	def addToPerson(self,messageid,personid):
		'''
		Add messageid, personid tuple to message_to_person table
		@param messageid: id of the message
		@type messageid: Integer
		@param personid: id of the person
		@type personid: Integer
		@return message_to_person.id
		'''
		try:
			mtpid = self.db.message_to_person.insert(message=messageid,person=personid)
		except IntegrityError:
			print "To Person already exists in database",mtpid
		else:	
			self.db.commit()
			return mtpid

	def addFromPerson(self,messageid,personid):
		'''
		Add messageid, personid tuple to message_from_person table
		@param messageid: id of the message
		@type messageid: Integer
		@param personid: id of the person
		@type personid: Integer
		@return message_to_person.id
		'''
		try:
			mtpid = self.db.message_from_person.insert(message=messageid,person=personid)
		except IntegrityError:
			print "From Person already exists in DB"
		else:
			self.db.commit()
			return mtpid

	def getFromPerson(self,messageid):
		'''
		Read who a message with messageid is sent fom
		@param messageid: id of the message
		@type messageid: Integer
		@return: tuple of email, name or blank if messageid not found ('','')
		@rtype: Tuple
		'''
		pid = self.db(self.db.message_from_person.message==messageid).select()
		for e in pid:
			person = self.db(self.db.person.id==e['person']).select()
			for e2 in person:
				return e2['email'],e2['name']	
		return "",""
			

	def addAttachment(self,messageid,name):
		'''
		Add an attachment file info to the database
		@param messageid: id of the message
		@type messageid: Integer
		@param name: short file path of the attachment 
		@type name: String
		'''
		try:
			aid = self.db.attachment.insert(message=messageid,name=name)
		except IntegrityError:
			print "Attachment alread exists in database"
		else:
			self.db.commit()
			return aid

	def addMessage(self,settype,template,subject,body,date,to,fromp,replyto,messageid,messagesetid,metajson="",attachments=[]):
		'''
		Add a new message to the database
		@param settype: templateset id 
		@type settype: Integer
		@param template: template id
		@type template: Integer
		@param subject: Subject of the message
		@type subject: String
		@param body: Body of the message
		@type body: String
		@param date: date string of when message was sent
		@type date: String
		@param to: list of people message was sent to
		@type to: list of strings
		@param fromp: list of people message is from
		@type fromp: list of strings
		@param replyto: replyto person
		@type replyto: String
		@param messageid: Message-Id header of the message
		@type messageid: String
		@param messagesetid: message set id of message
		@type messagesetid: String
		@param metajson: evmail string
		@type metajson: String
		@param attachments: list of files attached
		@type attachments: List
		@return: id of the new message
		@rtype: Integer
		'''
		print "---> Adding new message to:",to, "from:",fromp, "attachments:",attachments
		subject = subject.replace('\n','')
		try:
			rid = self.addPerson(replyto)
			mid = self.db.message.insert(templateset=settype,template=template,subject=subject,body=body,date=date,replyto=rid, evmail=metajson,messageid=messageid)
			msid = self.db.messageset.insert(messageid=mid,messagesetid=messagesetid)
			for each in to:
				pid = self.addPerson(each)
				self.addToPerson(mid,pid)
			for each in fromp:
				pid = self.addPerson(each)
				self.addFromPerson(mid,pid)
			for each in attachments:
				self.addAttachment(mid,each)
		except IntegrityError:
			print "Message already exists in database"
		else:
			self.db.commit()
			return messageid

	def deleteAllMessages(self):
		'''
		Delete all messages in the database
		'''
		self.db(self.db.message).delete()
		self.db(self.db.message_to_person).delete()
		self.db(self.db.message_from_person).delete()
		self.db(self.db.attachment).delete()
		self.db.commit()
	
	def getActiveEmails(self):
		'''
		Retrieve all active messages (status 1 or 2) in the database
		@return: list of message rows
		@rtype: List
		'''	
		query = "SELECT DATE(date) as dt,* FROM message INNER JOIN (SELECT DISTINCT messagesetid AS msid,messageid as msgid FROM messageset WHERE (status = 0 OR status = 1)) AS doop ON id=msgid ORDER BY dt ASC"
		#activemessages = self.db((self.db.message.status==0) | (self.db.message.status==1)).select()
		#activemessagesets = self.db(self.db.messageset).select(self.db.messageset.messageid,distinct=self.db.messageset.messagesetid)
		activemessages = self.db.executesql(query,as_dict=True)		
		print self.db._lastsql
		print activemessages
		'''items = []
		for each in activemessages:
			item.append(self.db(self.db.message.messagesetid==each[0]).select().first()'''
		
		return activemessages
	
	def reloadAllEmails(self):
		'''
		Delete all and re-add emails in the database
		'''
		# 1. Remove all messages from database
		self.deleteAllMessages()

		self.controller.client.select_folder("INBOX")
		uids = self.controller.client.search()
		for uid in uids:
			#try:
			messagestring = self.controller.client.fetch([uid],['RFC822'])
			message = email.message_from_string(messagestring[uid]['RFC822'])
			self.controller._addMessage(message)		
			#except ValueError:
			#	print "Value Error"


