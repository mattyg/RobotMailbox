""" Store global SETTINGS variables """


BASE_PATH = "/home/matt/Brandeis/Email2.0/RobotMailbox/"
'''root path to application. Include trailing slash.'''


XRC_PATH = BASE_PATH+"storage/wxformbuilder/noname.xrc"
'''path to .xrc file with default wx interface''' 

SMTP_HOST = "smtp.gmail.com"
'''# SMTP host address'''

SMTP_PORT = 465
'''SMTP Host port'''

IMAP_HOST = "imap.gmail.com"
'''IMAP host address'''

IMAP_PORT = 993
'''IMAP host port (default is 143)'''

IMAP_EMAIL = "thisismyuser@gmail.com"
IMAP_USER = "ThisIsMyUser"
IMAP_PASS = "ThisIsMyPassword"
'''IMAP user name'''

FILES_PATH = BASE_PATH+'storage/attachments/'
'''path to files directory (where attachements are stored)'''

TEMPLATESETS_PATH = BASE_PATH+'storage/templatesets/'
'''path to templatesets directory (where templatesets are stored)'''


DB_PATH = 'sqlite://'+BASE_PATH+'storage/db/storage.db'
'''
path to database, can be any of the following:
	SQLite 	sqlite://storage.db
	MySQL 	mysql://username:password@localhost/test
	PostgreSQL	postgres://username:password@localhost/test
	MSSQL 	mssql://username:password@localhost/test
	FireBird 	firebird://username:password@localhost/test
	Oracle 	oracle://username/password@test
	DB2 	db2://username:password@test
	Ingres 	ingres://username:password@localhost/test
	Informix 	informix://username:password@test
	Google App Engine/SQL	google:sql
	Google App Engine/NoSQL	google:datastore
'''

BASE_SCHEMA_PATH = BASE_PATH+'storage/schema/'
''' Base json schema path '''
CONFIG_SCHEMA_PATH = BASE_SCHEMA_PATH+'config-schema.json'
''' Base templateset config schema path '''
MESSAGE_SCHEMA_PATH = BASE_SCHEMA_PATH+'message-schema.json'
''' Base templateset message schema path '''
TEMPLATE_SCHEMA_PATH = BASE_SCHEMA_PATH+'template-schema.json'
''' Base templatset template schema path'''

TEMPLATESETS_REPO = 'http://gabrenya.com/mattneeds/templatesets/'
'''templatesets online repository URI'''

