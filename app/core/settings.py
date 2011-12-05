""" Store global SETTINGS variables """


# root path to application. Include trailing slash.
BASE_PATH = "/home/matt/Brandeis/Email2.0/robotmailbox/"

# path to .xrc file with default wx interface
XRC_PATH = BASE_PATH+"storage/wxformbuilder/noname.xrc"

# SMTP host address
SMTP_HOST = "smtp.gmail.com"
# SMTP Host port
SMTP_PORT = 465

# IMAP host address
IMAP_HOST = "imap.gmail.com"

# IMAP host port (default is 143)
IMAP_PORT = 993

# IMAP user name
IMAP_EMAIL = "matt.gabrenya@gmail.com"
IMAP_USER = "matt.gabrenya"
IMAP_PASS = "fuckSchool"

# path to files directory (where attachements are stored)
FILES_PATH = BASE_PATH+'storage/attachments/'

# path to templatesets directory (where templatesets are stored)
TEMPLATESETS_PATH = BASE_PATH+'storage/templatesets/'


# path to database, can be any of the following:
'''     SQLite 	sqlite://storage.db
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
DB_PATH = 'sqlite://'+BASE_PATH+'storage/db/storage.db'


# Base json schema paths
BASE_SCHEMA_PATH = BASE_PATH+'storage/schema/'
CONFIG_SCHEMA_PATH = BASE_SCHEMA_PATH+'config-schema.json'
MESSAGE_SCHEMA_PATH = BASE_SCHEMA_PATH+'message-schema.json'
TEMPLATE_SCHEMA_PATH = BASE_SCHEMA_PATH+'template-schema.json'

# templatesets online repository URI
TEMPLATESETS_REPO = 'http://gabrenya.com/mattneeds/templatesets/'

