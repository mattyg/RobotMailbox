from library.db.dal import DAL,Field
from pysqlite2.dbapi2 import OperationalError

class Model:
	controller = None
	''' controller of parent core model'''
	db = None
	def __init__(self,controller,dbpath):
		"""
		Initialize class for all Models
		@param controller: The parent core Controller
		@type controller: L{Controller}	
		@param dbpath: path to database
		@type dbpath: String
		"""
		self.controller = controller
		self.db = DAL(dbpath)
		self._defineSchema()

	def _defineSchema(self):
		'''
		Define database tables: person, attachment, email
		@requires: dal.py of the web2py library
		'''
		self.db.define_table('person',Field('id'), Field('email','string',unique=True), Field('name','string'),migrate=False,fake_migrate=True)
		self.db.define_table('attachment',Field('id'),Field('name','string'),Field('message'),migrate=False,fake_migrate=True)
		self.db.define_table('message',Field('id'), Field('templateset','string'), Field('template','string'), Field('status','integer',default=0), Field('subject','string'), Field('body','text'), Field('date','string'), Field('replyto',self.db.person),Field('evmail','text'), Field('attachments', self.db.attachment), Field('messageid','string',unique=True),migrate=False,fake_migrate=True)
		self.db.define_table('messageset',Field('id'),Field('messageid','string',unique=True),Field('messagesetid','string'),Field('status','integer',default=0),migrate=False,fake_migrate=True)

		# To & From persons
		self.db.define_table('message_to_person', Field('message',self.db.message), Field('person',self.db.person),migrate=False,fake_migrate=True)
		self.db.define_table('message_from_person', Field('message',self.db.message), Field('person',self.db.person),migrate=False,fake_migrate=True)


		# TEMPLATE tables
		self.db.define_table('template', Field('name','string'), Field("towho","string",default="",comment="{sender|recievers}"), Field("use","string",comment="{default|option}"), Field('templateset','integer'),migrate=False,fake_migrate=True)
		self.db.define_table('templateset', Field('name','string'), Field('version','string'), Field('path','string'), Field('templates',self.db.template),migrate=False,fake_migrate=True) 
		self.db.define_table('template_response', Field('id'), Field('template','integer'), Field('responsetemplate','integer'), Field('templateset','integer'),migrate=False,fake_migrate=True)
		# there should be unique_key=['name','version'] BUT multi-column unique keys are not possible in dal.py 
