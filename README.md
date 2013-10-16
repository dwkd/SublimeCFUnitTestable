What
============
CFUnitTestable is a small Sublime plugin that can be used to analyze Coldfusion Components.
This tool quickly determines which methods can be unit tested, what dependencies need to be mocked, and provides a resolution for methods that can not be unit tested.

To get familiar with unit testing, mocking and dependencies in Coldfusion, visit http://mxunit.org/


Installing
============
1. Download the project from github. (Press the Download Zip button.)
2. Open the downloaded zip file.
3. Select and copy the folder SublimeCFUnitTestable-master....
4. Open Sublime Text Editor
5. Under the Preferences menu, press Browse Packages....
6. Paste the folder SublimeCFUnitTestable-master... to the Packages directory.
7. Restart Sublime

Updating
========
1. Open Sublime and hit CTRL+`(tilde) to show the console.
2. Copy and paste the code below in the console input and hit ENTER
<br>!WARNING - the code below implies that your folder for this tool is named 'SublimeCFUnitTestable-master' and the py file is called 'cfunittestable.py'. Please modify this code accordingly if that's not the case.

<i>
	import urllib2,os; CFUnitTestable_dirName='SublimeCFUnitTestable-master'; CFUnitTestable_fileName='cfunittestable.py'; ipp=sublime.packages_path(); os.makedirs(os.path.join(ipp,CFUnitTestable_dirName)) if not os.path.exists(os.path.join(ipp,CFUnitTestable_dirName)) else None; urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(os.path.join(ipp,CFUnitTestable_dirName,CFUnitTestable_fileName),'wb').write(urllib2.urlopen('https://raw.github.com/dwkd/SublimeCFUnitTestable/master/cfunittestable.py').read());	
</i>

How to use
============
Simply open the CFC to be inspected and press the following key combination:<br/>
Windows: CTRL + ALT + U<br/>
Linux: CTRL + ALT + U<br/>
Mac: SUPER + ALT + U<br/>

License
=======
Copyright 2012 Alex Trican. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Alex Trican "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL Alex Trican OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
