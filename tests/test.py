from app.email.controller import EmailController as emailcontroller
import app.core.settings
from pprint import pprint
from app.templateset.controller import TemplatesetController as templatecontroller

import sys
sys.path.append("")

#controller = emailcontroller(settings.IMAP_HOST,settings.IMAP_PORT,settings.IMAP_USER,settings.IMAP_PASS)

#print controller.reloadAllEmails()

#controller.reloadAllEmails()

controller = templatecontroller()
controller.validateTemplateset('discussion')

