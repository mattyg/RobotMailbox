from app.core.model import Model
from pysqlite2.dbapi2 import IntegrityError
from email.message import Message
from email.utils import make_msgid
import os
import simplejson

class EvmailModel(Model):
	def __init__(self,controller,db):
		"""Initialize  EvmailModel
		@param controller: The parent EvmailController
		@type controller: L{Controller}	
		@param db: path to database
		@type db: String
		"""
		Model.__init__(self,controller,db)
		self.controller = self.controller
	def getMessagesInSet(self,messagesetid):
		'''
		Read message id's of a messageset
		@param messagesetid: id of the messageset
		@type messagesetid: Integer
		'''
		row = self.db(self.db.messageset.messagesetid==messagesetid).select()
		msgids = []
		for each in row:
			msgids.append(each['messageid'])
		return msgids

	def getMessage(self,messageid):
		'''
		Get a single message with messageid
		@param messageid: the id of the message to get to persons
		@type messageid: Integer
		@return: message with messageid
		@rtype: Dict
		'''
		row = self.db(self.db.message.id==messageid).select().first()
		return row

	def getMessagesetId(self,messageid):
		'''
		Get messageset id,name from messageid
		@param messageid: id of the message to get set of
		@type messageid: Integer
		'''
		messagerow = self.db(self.db.message.id==messageid).select().first()
		rows = self.db(self.db.messageset.messageid==messagerow['id']).select().first()
		if rows is not None:
			return rows['messagesetid']
		else:
			return None


	def getMessageFroms(self,messageid):
		'''
		Get all from persons of a message
		@param messageid: the id of the message to get to persons
		@type messageid: Integer
		@return: list of people who sent the message
		@rtype: List
		'''
		rows = self.db(self.db.message_from_person.message==messageid).select()
		froms = []
		for each in rows:
			froms.append(self.db(self.db.person.id==each['person']).select().first())
		return froms
	def getMessageReplyTo(self,messageid):
		'''
		Get name,email of reply to person
		@param messageid: id of message to get replyto 
		@type messageid: Integer
		'''
		row = self.db(self.db.message.id==messageid).select().first()
		if row is not None:
			rowp = self.db(self.db.person.id==row['replyto']).select().first()
			if rowp is not None:
				return rowp['name'],rowp['email']
			else:
				return None
		else:
			return None
	def getMessageTos(self,messageid):
		'''
		Get all to persons of a message
		@param messageid: the id of the message to get to persons
		@type messageid: Integer
		@return: list of people who recieved the message
		@rtype: List
		'''
		rows = self.db(self.db.message_to_person.message==messageid).select()
		tos = []
		for each in rows:
			tos.append(self.db(self.db.person.id==each['person']).select().first())
		return tos

	def generateMessageId(self):
		'''
		Generate hide data in response to another evmail message
		@param mid: message
		@type mid: Integer
		@return: response hide data
		@rtype: Dict
		'''
		return make_msgid()

	def generateNewHideData(self,setname,name,version):
		'''
		Generate hide data for a new evmail message
		@param setname: evmail templateset name
		@type setname: String
		@param name: evmail template name
		@type name: String
		@param version: evmail templateset version
		@type version:
		@return: response hide data
		@rtype: Dict
		'''
		data = self.controller.controller.getTemplatesetController().model.readTemplate(setname,name,version)

		data['hide']['messageid'] = make_msgid()
		data['hide']['messagesetid'] = data['hide']['messageid']
		print 'DHIDE',data['hide']
		print 'DHIDE',setname,name,version
		
		return data['hide']

	def getMessageData(self,messageid):
		row = self.db(self.db.message.id==messageid).select().first()
		if row['evmail'].strip() is not '':
			try:
				res = simplejson.loads(row['evmail'])
				return res
			except:
				return None
		else:
			data = {'hide':{},'show':{}}
			data['hide']['messageid'] = row['messageid']
			data['hide']['setname'] = 'discussion'
			data['hide']['name'] = 'message'
			data['hide']['version'] = self.controller.controller.getTemplatesetController().model.getNewestTemplatesetVersion('discussion')
			data['show']['subject'] = row['subject']
			data['show']['body'] = row['body']
			msrow = self.db(self.db.messageset.messageid==row['id']).select().first()
			if msrow is not None:
				data['hide']['messagesetid'] = msrow['messagesetid']
			return data	
