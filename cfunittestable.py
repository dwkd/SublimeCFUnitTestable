import sublime, sublime_plugin
import math
import re


class cfunittestableCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		#write general stats
		f = self.view
		returnMessage = "\nCFUnitTestable \n\nGeneral Stats:\n==========================================================================================================================\n"
		returnMessage += "File: "+str(f.file_name())+"\nSize: ~"+str(f.size()/1024)+"Kb ("+str(f.size())+" bytes)\n"
		all = self.view.find_all("[\s\S]*")
		self.view.add_regions("AllContent", all, "source", sublime.HIDDEN)
		g = self.view.get_regions("AllContent")
		for allregion in g:
			h = len(self.view.substr(allregion))
		
		#get all functions
		allMethods = self.view.find_all("<cffunction[\s\S]*?<\/cffunction>", sublime.IGNORECASE)

		PublicMethodIndexes = []
		PrivateMethodIndexes = []
		RemoteMethodIndexes = []
		PackageMethodIndexes = []

		#loop through functions and find all private and remote functions
		for idx,method in enumerate(allMethods):
			methodLineByLine = self.view.split_by_newlines(method)
			re_accessPublic = re.compile("access\s*\=\s*[\"\'](public)[\"\']", re.IGNORECASE)
			re_accessRemote = re.compile("access\s*\=\s*[\"\'](remote)[\"\']", re.IGNORECASE)
			re_accessPrivate = re.compile("access\s*\=\s*[\"\'](private)[\"\']", re.IGNORECASE)
			re_accessPackage = re.compile("access\s*\=\s*[\"\'](package)[\"\']", re.IGNORECASE)

			for line in methodLineByLine:
				foundAccessPublic = re_accessPublic.search(self.view.substr(line))
				if foundAccessPublic:
					PublicMethodIndexes.append(idx)					
			
			for line in methodLineByLine:
				foundAccessRemote = re_accessRemote.search(self.view.substr(line))
				if foundAccessRemote:
					RemoteMethodIndexes.append(idx)					

			for line in methodLineByLine:
				foundAccessPrivate = re_accessPrivate.search(self.view.substr(line))
				if foundAccessPrivate:
					PrivateMethodIndexes.append(idx)
			
			for line in methodLineByLine:
				foundAccessPackage = re_accessPackage.search(self.view.substr(line))
				if foundAccessPackage:
					PackageMethodIndexes.append(idx)


		returnMessage += "Methods:\n\t" + str(len(PublicMethodIndexes)) + " Public\n\t" + str(len(PrivateMethodIndexes)) + " Private\n\t" + str(len(RemoteMethodIndexes)) + " Remote\n\t" + str(len(PackageMethodIndexes)) + " Package"
		returnMessage += "\nPublic Methods:"
		returnMessage += "\n==========================================================================================================================\n"
		
		#retreive all method names
		methodNames = []
		for method in allMethods:
			methodLineByLine = self.view.split_by_newlines(method)
			re_LookFor_MethodName = re.compile("name\s*\=\s*[\"\']", re.IGNORECASE)
			for line in methodLineByLine:
				if re_LookFor_MethodName.search(self.view.substr(line)):
					for splittedItem in self.view.substr(line).split():
						if re_LookFor_MethodName.search(splittedItem):
							partialName = re.sub("^[^\"]*?\"","",str(splittedItem))
							methodNames.append(re.sub("(\"|>)","",str(partialName)))
					break

		#check for dependencies 
		for idx,method in enumerate(allMethods):
			dependencies = []
			QueryDependencies = []
			methodName = ""
			methodLineByLine = self.view.split_by_newlines(method)
			re_LookFor_MethodName = re.compile("name\s*\=\s*[\"\']", re.IGNORECASE)
			re_LookFor_CreateObject = re.compile("CreateObject", re.IGNORECASE)
			re_LookFor_Functions = re.compile("(?<!response)(?<!result)\.[A-Za-z\d_]+\(", re.IGNORECASE)
			get_allQueryDependencies = self.view.find_all("<cfquery[\s\S]*?<\/cfquery>", sublime.IGNORECASE)

			for line in methodLineByLine:

				#get the method name
				if not len(methodName) and re_LookFor_MethodName.search(self.view.substr(line)):
					for splittedItem in self.view.substr(line).split():
						if re_LookFor_MethodName.search(splittedItem):
							methodName = re.sub(">","",str(splittedItem))
							break		

				#get method access
				if not len(methodName) and re_LookFor_MethodName.search(self.view.substr(line)):
					for splittedItem in self.view.substr(line).split():
						if re_LookFor_MethodName.search(splittedItem):
							methodName = re.sub(">","",str(splittedItem))
							break				

				#look for object dependencies
				if re_LookFor_CreateObject.search(self.view.substr(line)):
					(row, col) = self.view.rowcol(line.begin())
					dependencies.append("Object dependency found on line " +str(row+1))

				#look for function dependencies
				if re_LookFor_Functions.search(self.view.substr(line)):
					(row, col) = self.view.rowcol(line.begin())
					dependencies.append("Function dependency found on line " +str(row+1)) # + ": " + re.sub("^[\t ]*?","\t",self.view.substr(line)))
				
				#look for function dependencies
				for pubMethodName in methodNames:
					re_LookFor_MethodCall = re.compile("(?<![a-zA-Z_\d])" +pubMethodName +"\(")
					if re_LookFor_MethodCall.search(self.view.substr(line)):
						(row, col) = self.view.rowcol(line.begin())
						dependencies.append("Function dependency found on line " +str(row+1)) # + ": " + re.sub("^[\t ]*?","\t",self.view.substr(line)))

				#look for query dependencies
				for i,queryDependency in enumerate(get_allQueryDependencies):
					if queryDependency.intersects(line):
						(row, col) = self.view.rowcol(line.begin())
						dependencies.append("Query dependency found on line " +str(row+1))# + ": " + re.sub("^[\t ]*?","\t",self.view.substr(line)))
						QueryDependencies.append("Query dependency found on line " +str(row+1))# + ": " + re.sub("^[\t ]*?","\t",self.view.substr(line)))	
						del get_allQueryDependencies[i]
						break
				
			#output method name and dependencies
			functionHeader = ""
			if idx in PackageMethodIndexes:
				functionHeader = "\n[BAD] Method: " + methodName + " - This method can not be unit tested because it is confined to a package (access=\"package\")\n"
			elif len(QueryDependencies):
				functionHeader = "\n[BAD] Method: " + methodName + " - This method can not be unit tested until the query dependencies are moved to DAOs\Gateways\n"
			else:
				functionHeader += "\n[OK] Method: " + methodName + " - This method can be unit tested\n"
			returnMessage += functionHeader
			for k in range(1,len(functionHeader)):
				returnMessage +="-"
			returnMessage += "\n"
			if idx in PrivateMethodIndexes:
				returnMessage += "(!HINT - This is a private method. Use \"makePublic\" to test it.)\n"
			if len(dependencies):
				returnMessage += "Dependencies found. Please mock the following:"
				for dependency in dependencies:
					returnMessage += "\n\t" + dependency
				returnMessage += "\n"
			returnMessage += "\n"
			

		#send to new file
		w = self.view.window()
		w.run_command("new_file")
		v = w.active_view()
		v.insert(edit,0,returnMessage)

		