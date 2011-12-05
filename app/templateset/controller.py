from app.templateset.model import TemplatesetModel
from app.templateset.view import TemplatesetView
from app.email.controller import EmailController
from app.core import settings
from library import validictory
from library import simplejson
from simplejson.decoder import JSONDecodeError
from validictory.validator import SchemaError

class TemplatesetError(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

class TemplatesetController:
	def __init__(self,controller):
		'''
		initialize TemplatesetController
		'''
		self.controller = controller
		self.emailcontroller = self.controller.getEmailController()
		self.model = TemplatesetModel(self,settings.DB_PATH,settings.TEMPLATESETS_REPO,settings.TEMPLATESETS_PATH)

	def getTemplatesetPath(self,setname,version):
		'''
		Return the path of templateset named setname of version
		@param setname: name of templateset to get path of
		@type setname: wx.Notebook
		@param version: version of templateset
		@type version: wx.Notebook
		@return: templateset path
		@rtype: wx.Notebook
		'''
		tspath = self.model.getTemplatesetPath(setname,str(version))
		if tspath is not None:
			return tspath
		else:
			templatesetpath = self.model.dlTemplateset(name,version)
			self.model.addTemplateset(name,version,templatesetpath)
			return templatesetpath

	def validateTemplateset(self,templatesetdir):
		'''
		validate ALL files of a template set: config.json & all templates
		@param templatesetdir: name of the templateset directory containing config.json file for the templateset
		@type templatesetdir: string
		'''
		configschemafile = open(settings.CONFIG_SCHEMA_PATH,'r')
		configschema = simplejson.load(configschemafile)
		try:
			configfile = open(settings.TEMPLATESETS_PATH+templatesetdir+'/config.json','r')
		except IOError:
			raise IOError,"Templateset directory has no config.json."

		try:
			configdata = simplejson.load(configfile)
		except JSONDecodeError, e:
			print "config.json JSON Decoding error: ",e
			raise TemplatesetError("simplejson.load( config.json ) raised JSONDecodeError")
		
		try:
			validictory.validate(configdata,configschema)
		except SchemaError, e:
			print "config.json Schema validation error: ",e
			raise TemplatesetError("validictory.validate( config.json, config-schema.json) raised SchemaError")
		

		templateschecked = []
		for each in configdata['files']:
			str(configdata['setname'])+"/"+str(each['file'])
			try:
				self.validateTemplate(settings.TEMPLATESETS_PATH+templatesetdir+"/"+each['name'])
				templateschecked.append(each['file'])
				for et in each['responses']:
					if et['file'] not in templateschecked:
						print et['file']
						self.validateTemplate(settings.TEMPLATESETS_PATH+templatesetdir+"/"+et['file'])
			except IOError, e:
				print "Template",str(configdata['setname'])+"/"+str(each['file'])," was not found with error: ",e

			except JSONDecodeError, e:
				print e
			except SchemaError, e:
				print "Template",str(configdata['setname'])+"/"+str(each['file']),"Schema validation error: ",e
				raise TemplatesetError("validictory.validate( config.json, config-schema.json) raised SchemaError") 

	def validateTemplate(self,templatepath):
		'''
		validate a single template
		@returns: tuple of setname/name,version
		@param templatepath: path to the template
		@type templatepath: string
		'''
		# Open & Load template-schema file
		templateschemafile = open(settings.TEMPLATE_SCHEMA_PATH,'r')
		templateschema = simplejson.load(templateschemafile)

		# Open & load template file
		try:
			templatefile = open(templatepath,'r')
		except IOError, e:
			raise IOError, e

		try:
			templatedata = simplejson.load(templatefile)
		except simplejson.JSONDecodeError, e:
			raise simplejson.JSONDecodeError, e

		# Validate template file
		try:
			validictory.validate(templatedata,templateschema)	
		except SchemaError, error:
			raise SchemaError, error
		
		tname = str(templatedata['setname'])+"/"+str(templatedata['name'])
		return tname,templatedata['version']

	def generateFormView(self,panel,setname,name=None,version=None,response=None):
		'''
		Read template and generate a form view from it
		@param panel: wx parent to generate form on
		@param setname: name of templateset
		@type setname: wx.Notebook
		@param name: name of template
		@type name: wx.Notebook
		'''
		template = self.model.readTemplate(setname,name,version)
		templatesetview = TemplatesetView(self,panel)
		templatesetview.generateFormView(panel,template,settings.IMAP_EMAIL,response)

	def reloadTemplatesets(self):
		self.model.reloadAll()

	def getAllTemplatesets(self):
		return self.model.getAll()

	def getDefaultTemplates(self,name,version):
		return self.model.getDefaultTemplates(name,version)

	def getResponseTemplates(self,templateid):
		return self.model.getResponseTemplates(templateid)

	def getTemplateName(self,templateid):
		return self.model.getTemplateName(templateid)

