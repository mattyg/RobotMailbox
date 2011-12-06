from app.core.model import Model
from pysqlite2.dbapi2 import IntegrityError
import urllib
import os
import tarfile
from app.core import settings
from library import simplejson
import ordereddict
class TemplatesetModelError:
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)


class TemplatesetModel(Model):
	def __init__(self,controller,db,templatesetsrepo,templatesetspath):
		'''
oll		Create TemplatesetModel
		@param controller: parent Templateset controller
		@type controller: L{TemplatesetController}
		@param db: path to database
		@type db: String
		@param templatesetsrepo: Online path to repo of templatesets
		@type templatesetsrepo: String
		@param templatesetspath: Local path to directory of templatesets
		@type templatesetspath: String
		'''
		Model.__init__(self,controller,db)
		self.templatesetsrepo = templatesetsrepo
		self.templatesetspath = templatesetspath

	def getNewestTemplatesetVersion(self,name):
		'''
		get the highest version of the templateset name
		@param name: name of templateset
		@type name: String
		@return: version of newest templateset
		@rtype: String
		'''
		rows = self.db(self.db.templateset.name==name).select().first()
		version = rows.version
		return version
	
	def hasTemplateset(self,name,version=None):
		''' 
		return value of template-set id if it exists, false if it doesnt
		@param name: template set name
		@type name: String
		@param version: template set version
		@type version: String
		'''
		if version is None:
			version = self.getNewestTemplatesetVersion(name)
		
		rows = self.db((self.db.templateset.name==name) & (self.db.templateset.version==version)).select().first()
		if rows is None:
			return False
		else:
			return rows['id']

	def hasTemplate(self,setname,name,version=None):
		''' 
		Checks if template with setname & name exists
		@param name: template set name
		@type name: string
		@param version: template set version
		@type version: string	
		@return: id of template from db
		@rtype: Integer
		'''
		if version is None:
			version = self.getNewestTemplatesetVersion(setname)
		
		ts = self.db((self.db.templateset.name==setname) & (self.db.templateset.version==version)).select().first()
		print 'HASTEMPLATE',ts.id
		if ts is not None:		
			rows = self.db((self.db.template.name==name) & (self.db.template.templateset==ts.id)).select().first()
			if rows is not None:
				return rows.id
			else:
				return False
		else:
			return False

	def getResponseTemplates(self,templateid):
		'''
		Get all available responses from the template with templateid. 
		@param templateid: id of the template in db
		@type templateid: Integer
		@return: list of response template ids
		@rtype: List
		'''
		rows = self.db(self.db.template_response.template==templateid).select()
		templateids = []
		for each in rows:
			templateids.append(each['responsetemplate'])
		return templateids

	def getDefaultTemplates(self,setname,version):
		'''
		get default new-message templates
		@param setname: name of the template set
		@type: string
		@param version: version of tempate set
		@type: string
		'''
		rows = self.db((self.db.templateset.name==setname) & (self.db.templateset.version==version)).select().first()
		tsid = rows.id
		rows = self.db((self.db.template_response.template==0) & (self.db.template_response.templateset==tsid)).select()
		templaterows = []
		for each in rows:
			rows = self.db(self.db.template.id==each.responsetemplate).select()
			templaterows.extend(rows)
		return templaterows

	def addTemplateset(self,name,version):
		'''
		add a (already downloaded) template set to the database.
		@param name: the Templateset name
		@type name: String
		@param version: the Templateset version
		@type version: String
		'''
		if self.hasTemplateset(name,version) is False:
			tsid = self.db.templateset.insert(name=name,version=version)
			#try:
			configf = open(settings.TEMPLATESETS_PATH+name+'/'+version+'/config.json')
			print settings.TEMPLATESETS_PATH+name+'/'+version+'/config.json'
			config = simplejson.load(configf)
			for each in config['files']:
				efile = open(settings.TEMPLATESETS_PATH+name+'/'+version+'/templates/'+each['name'],'r')
				print name+'/'+each['name']
				template = simplejson.load(efile)
				tid = self.db.template.insert(name=each['name'],templateset=tsid)
				self.db.template_response.insert(template=0,responsetemplate=tid,templateset=tsid)
				if each.__contains__('responses'):
					for res in each['responses']:
						print name+'/'+res['name']
						resid = self.hasTemplate(name,res['name'],version)
						if resid == False:
							resid = self.db.template.insert(name=res['name'],templateset=tsid)
						self.db.template_response.insert(template=tid,templateset=tsid,responsetemplate=resid)
						
			#except IOError:
			#	raise IOError, "Config file not found"	
			self.db.commit()

	def dlTemplateset(self,name,version):
		'''
		Download a template set from the internet. Call self.addTemplateset to add to DB
		@param name: name of the templateset
		@type name: String
		@param version: version of the templateset
		@type version: String
		'''
		try:
			os.mkdir(self.templatesetspath+name)
		except:
			# Already has a version of template
			pass
		try: 
			os.mkdir(self.templatesetspath+name+'/'+version)
		except OSError:
			#raise OSError, "Template Set "+str(name)+" "+str(version)+" already exists"
			pass

		urllib.urlretrieve(self.templatesetsrepo+name+'/'+version,self.templatesetspath+name+'/'+version+'/temp.tar')
		tf = tarfile.open(self.templatesetspath+name+'/'+version+'/temp.tar')
		tf.extractall(self.templatesetspath+name+'/'+version+'/')
		tf.close()
		os.remove(self.templatesetspath+name+'/'+version+'/temp.tar')
		return self.templatesetspath+name+'/'+version+'/'

	def reloadAll(self):
		self.db(self.db.templateset).delete()
		templatesets = os.listdir(settings.TEMPLATESETS_PATH)
		for each in templatesets:
			templatesetsver = os.listdir(settings.TEMPLATESETS_PATH+each+'/')
			for ver in templatesetsver:
				try:
					configfile = open(settings.TEMPLATESETS_PATH+each+'/'+ver+'/config.json','r')
					try:
						config = simplejson.load(configfile)
						self.addTemplateset(config['setname'],config['version'],each+'/'+ver+'/config.json')
					except:
						print "Bad Templateset",each,ver,"config.json file"
						raise TemplatesetModelError("simplejson.load( config.json ) raised JSONDecodeError")
	
				except:
					print "Templateset",each,"does not have a 'config.json' file"

	def getAllTemplatesets(self):
		'''
		get all templatesets in the database
		@return: templateset rows
		@rtype: List
		'''
		rows = self.db(self.db.templateset).select()
		return rows

	def readTemplate(self,setname,name,version=None):
		'''
		read a template and return it in data form
		'''
		if version is None:
			version = self.getNewestTemplatesetVersion(setname)
		
		try:
			tfile = open(settings.TEMPLATESETS_PATH+setname+'/'+version+'/templates/'+name)
			#try:
			tdata = simplejson.load(tfile,object_pairs_hook=ordereddict.OrderedDict)
			print "TEMPLATE READ",tdata
			return tdata
			#except:
			print "Template file "+settings.TEMPLATESETS_PATH+setname+'/'+version+'/templates/'+name+' is not properly formed JSON'
		except IOError:
			raise IOError
		return None

	
	def getTemplatesetPath(self,name,version):
		'''
		Get path of templateset with name=name & version = version)
		@param name: templateset name
		@type name: String
		@type version: String
		@return: string of template path
		@rtype: String
		'''
		return name+'/'+version+'/'
	
	
 
	def getTemplateName(self,templateid):
		'''
		Get setname,name of template from id
		@param templateid: id of template
		@type templateid: Integer
		@return: tuple of templateset name, template name
		@rtype: Tuple
		'''
		print "tid",templateid
		t = self.db(self.db.template.id==templateid).select().first()
		if t is not None:
			ts = self.db(self.db.templateset.id==t['templateset']).select().first()
			t = t['name']
			if ts is not None:
				ts = ts['name']
				return ts,t

