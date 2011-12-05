
Message Template
----------------

Each structured message type, or *template*, is defined in a JSON file, structured with the JSON schema media type as outline in draft-zyp-json-schema-03 (1). 


Template Sets
--------------

Template sets are a container for all the message templates that share a common purpose for communication. 

Each template set is a directory, containing the following files:
*	a json schema file entitled *config.json* conataining information about the template set and the roles of individual templates
*	a json schema file for every template
*	a json schema file entitle *auto.json* containing information about default and optional automated actions by RobotMailbox or another compatible evMail client


__Examples__
To describe event messages using a template set, the directory structure might look like:
`events/
	auto.json
	config.json
	invite.json
	rsvp.json
	requestnewdate.json
`


config.json
------------

config.json outlines the roles of each template in the template set.

The following root attributes are **required:**

**name** - The template set name
**version** - Template set version

**files** - An array of dicts, each dict representing one template in the set,
*	The following attributes for each dict within files are **required**
	* 	**name** - URI to each template file
	*	
	



The following root attributes are **optional:**

**description** - description of the template set


Citations:
(1) http://tools.ietf.org/html/draft-zyp-json-schema-03
