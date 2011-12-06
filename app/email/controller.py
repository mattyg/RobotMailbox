from library.imapclient.imapclient import IMAPClient
from app.email.model import EmailModel
from app.core import settings
import email
import os
import smtplib
import time

class EmailController:
	'''
	Email controller
	@todo: 	create mark message as read function
	'''
	client = None
	''' IMAP client library'''
	model = None
	''' Email model'''
	offline = True
	''' Is IMAP connected '''
	def __init__(self,controller,host,port,user,passw,ssl=True):
		'''
		Initialize EmailController -- works with imap
		@param controller: parent core L{Controller}
		@type controller: L{Controller}
		@param host: IMAP host address
		@type host: String
		@param port: IMAP port
		@type port: L{int} 
		@param user: IMAP username
		@type user: String
		@param passw: IMAP password
		@type passw: String
		@param ssl: Use IMAP through SSL?
		@type ssl: Boolean
		'''
		self.controller = controller
		self.host = host
		self.port = port
		self.user = user
		self.passw = passw
		self.ssl = ssl
		try:
			self.client = IMAPClient(host,port,True,ssl)
			self.client.login(user,passw)	
			self.offline = False
		except:
			print "Couldn't connect to IMAP server: ",host,port,user,passw,"ssl=",ssl
			self.offline = True
		self.model = EmailModel(self,settings.DB_PATH)	
	
	def sendMessage(self,send_from,send_to,mimemessage):
		'''
		Send a message through smtp
		@param send_from: email of sender
		@type send_from: String
		@param send_to: email of reciever
		@type send_to: String
		@param mimemessage: messagedata
		@param mimemessage: MIMEMessage
		'''
		smtp = smtplib.SMTP_SSL(settings.SMTP_HOST,settings.SMTP_PORT)
		smtp.login(settings.IMAP_USER,settings.IMAP_PASS)
		try:
			smtp.sendmail(send_from, send_to, mimemessage.as_string())
			#return True
		except smtplib.SMTPException, e:
			raise Exception('SMTP to '+settings.SMTP_HOST+':'+settings.SMTP_PORT+' failed.')
			#return False
		'''try:
			self.emailmodel.updateStatus(
		except Exception, e:
			print e'''
		smtp.close()
		

	def addNewEmails(self):
		'''
		Add UNSEEN emails in IMAP to DB
		'''
		self.client.select_folder("INBOX")
		uids = self.client.search("UNSEEN")
		for uid in uids:
			msg = self.client.fetch([uid],['RFC822'])
			message = email.message_from_string(msg[uid]['RFC822'])
			mid = self._addMessage(message)
			

	def _addMessage(self,message):
		'''
		analyze email message & add to database
		@param message: the email message data
		@type message: Message
		@return: new message id
		@rtype: L{int}
		'''
		messageid = message.get('Message-ID')
		subject = message.get('Subject')
		body = ''
		date = message.get('Date')
		metajson = ''
		attachments = []
		replyto = message.get('Reply-to')
		if message.get('From') is not None:
			fromp = message.get('From').split('\n')
		else: 
			fromp = []
		if message.get('To') is not None:
			to  = message.get('To').split('\n')
		else:
			to = []
	
		if message.is_multipart():
			payload = message.get_payload()
			for part in payload:
				if part.is_multipart():
					payload2 = part.get_payload()
					for part2 in payload2:
						maintype = part2.get_content_maintype()
						subtype = part2.get_content_subtype()
						if maintype == "application" and subtype == "json":
							filen = part2.get_filename()
							metajson =  str(part2.get_payload(decode=True))
						elif maintype != "text":
							filen = part2.get_filename()
							if filen is not None:
								fpath = self._saveFile(part2.get_payload(decode=True),'text','attachments/',filen)
								attachments.append(fpath)
							else:
								print "odd message: ",maintype,subtype	
						else:
							body += part2.get_payload()
				else:
					maintype = part.get_content_maintype()
					subtype = part.get_content_subtype()
					if maintype == "application" and subtype == "json":
						filen = part.get_filename()
						metajson = str(part.get_payload(decode=True))
					elif maintype != "text":
						filen = part.get_filename()
						if filen is not None:
							fpath = self._saveFile(part.get_payload(decode=True),'text','attachments/',filen)
							attachments.append(fpath)
						else:
							print "odd message: ",maintype,subtype	
					else:
						body += part.get_payload()
			
		else:
			body = str(message.get_payload())
		if metajson != '':
			evmailcontroller = self.controller.getEvmailController()
			setname,name,version,messagesetid = evmailcontroller.processEvmail(metajson)
			self.templatesetmodel = self.controller.getTemplatesetController().model
			tsid = self.templatesetmodel.hasTemplateset(setname,version)
			tid = self.templatesetmodel.hasTemplate(setname,name,version)
		else:
			tsid = ''
			tid = ''
			messagesetid = messageid
		datet = email.utils.parsedate(date)
		date = time.strftime('%Y-%m-%d %H:%M:%S ',datet)
		mid = self.model.addMessage(tsid,tid,subject,body,date,to,fromp,replyto,messageid,messagesetid,metajson,attachments)
		return mid
		#for uid in uids:
		#	self.client.fetch(uid,['UID','BODY','TO','SUBJECT','FROM'])

	def _saveFile(self,payload,loadtype='text',prefix="",filename=""):
		'''
		Save a file attachment
		@param payload: mime payload
		@param loadtype: payload type (text or binary)
		@type loadtype: String
		@param prefix: File prefix
		@type prefix: String
		@param filename: original filename
		@type filename: String
		@return: filepath within files directory,
		@rtype: String
		'''
		if filename is not None and filename.find('.') != -1:
			filesplit = filename.rpartition('.')
			ftype = "."+filesplit[2]
			path = settings.FILES_PATH+filesplit[0]
		else:
			ftype = ""
			path = settings.FILES_PATH+filename

		counter = ""
		delim = ''
		while os.path.isfile(path+delim+str(counter)+ftype):
			if counter == "":
				counter = 1
			else:
				counter += 1
			delim = '-'
		print path+delim+str(counter)+ftype
		if loadtype == 'binary':
			openstr = 'wb'
		else:
			openstr = 'w'
		fp = open(path+delim+str(counter)+ftype,openstr)			
		fp.write(payload)
		fp.close()
		return str(counter)+ftype

	def isoffline(self,count=0):
		if count == 3 and self.offline is True:
			return True
		elif self.offline is False:
			return False
		else:
			self.__init__(self.controller,self.host,self.port,self.user,self.passw,self.ssl)
			return self.isoffline(count+1)

if __name__ == "__main__":
	emailcontroller()
