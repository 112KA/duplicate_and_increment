# coding:utf-8
import sublime, sublime_plugin, re

class DuplicateAndIncrementCommand(sublime_plugin.TextCommand):

	def func(self, m):
		n=int(m.group())
		return str(n+1)

	def increment(self, region):
		string = self.view.substr(region)
		return re.sub(r'(\d+)', self.func, string)

	def increment_line(self, edit, line, regions):
		#duplicate
		string = self.view.substr(line)
		self.view.insert(edit, line.begin(), string + '\n')

		offset = len(line) + 1
		line = sublime.Region(line.a+offset, line.b+offset)

		for i in range(len(regions)):
			regions[i] = sublime.Region(regions[i].a+offset, regions[i].b+offset)

		if len(regions)==1 and regions[0].empty():
			string = self.increment(line)
			self.view.replace(edit, line, string)
		else:
			for region in regions:
				if not region.empty():
					string = self.increment(region)
					self.view.replace(edit, region, string)

		return offset

	def run(self, edit):

		regions = []
		offset = 0
		for region in self.view.sel():
			if len(regions) == 0:
				line = self.view.line(region)
				regions.append(region)
			else:
				if not line.contains(region):
					offset = self.increment_line(edit, line, regions)
					regions = []

				region = sublime.Region(region.a+offset,region.b+offset)
				line = self.view.line(region)
				regions.append(region)

		self.increment_line(edit, line, regions)