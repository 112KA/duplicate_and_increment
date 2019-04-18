# coding:utf-8
import sublime, sublime_plugin, re, inspect

# Asks the user to input the number of times they want to duplicate the content
class DuplicateAndIncrementInputCommand(sublime_plugin.TextCommand):

	def run(self, edit):		
		# Gather Input
		window = self.view.window()
		window.show_input_panel("Number of duplications:", "1", lambda x: self.view.run_command('duplicate_and_increment', {"num_duplications": x}), None, None)

# Duplicates and increments the selected content
class DuplicateAndIncrementCommand(sublime_plugin.TextCommand):
	# Generator that returns a string with any digits inside incremented by 1
	def increment(self, string, num_duplications):
		i = 0
		while i < num_duplications:
			string = re.sub(r'(\d+)', self.func, string)
			yield string
			i = i + 1

	# Takes a Regex capture group, parses as an int and returns that int plus 
	# one as a string.
	def func(self, m):
		n = int(m.group())
		return str(n + 1)

	def run(self, edit, **kwargs):
		num_duplications = int(kwargs.get('num_duplications', 1))
    
		# Collect each region, selecting by the line level
		regions = []
		for region in self.view.sel():
			if not region.empty():
				regions.append(self.view.full_line(region))
		
		# Duplicate each region in turn
		for i in range(len(regions)):
			# Text in the region
			region = regions[i]
			string = self.view.substr(region)
			
			# We'll build a string to append after the region
			# Using a generator incase number of duplications is really high
			replace_string = '\n'.join(s for s in self.increment(string, num_duplications))
				
			# Append to the previous region
			self.view.insert(edit, region.end(), replace_string);
