import sublime, sublime_plugin, textwrap

# a simple object that keeps track of line content and its indentation
class line:
    def __init__(self, content, numCols):
        assert(type(content) == str or type(content) == unicode)
        assert(type(numCols) == int)

        self.numCols = numCols
        # get rid of any new-line or space characters at start/end of line
        self.content = content.rstrip().lstrip()
        
        num_indent_chars = len(content) - len(content.lstrip())
        self.indent = 0
        if (self.content == ""):
            return
        assert(num_indent_chars >= 0)
        
        # 1 tab == 4 spaces
        for i in range(num_indent_chars):
            if content[i] == " ":
                self.indent = self.indent + 1
            elif content[i] == "\t":
                self.indent = self.indent + 4
            else:
                assert(0)
    
    def format(self):
        if (self.content == ""):
            return "\n"
        lines = textwrap.wrap(self.content, self.numCols - self.indent - 1)
        fmtted = ""

        # don't use tabs -- they aren't always rendered how we want in
        # various text fields
        for line in lines:
            fmtted = fmtted + (" " * int(self.indent))
            fmtted = fmtted + line + "\n"
        
        return fmtted

  
# Extends TextCommand so that run() receives a View to modify.  
class FixedWidthCommand(sublime_plugin.TextCommand):  
    def run(self, edit, numCols = 80):
        if (type(numCols) != int):
            numCols = int(numCols)
        
        # here, each region is a selected area of text
        for region in self.view.sel():
            if not region.empty():  
                listOfLines = self.getListOfLines(region)
                newRegionString = self.getReplacementString(listOfLines, numCols)
                self.view.replace(edit, region, newRegionString)

        
    def getReplacementString(self, listOfLines, numCols):
        newRegionString = ""
        for l in listOfLines:
            lineObj = line(l, numCols)
            formattedLine = lineObj.format()
            newRegionString = newRegionString + formattedLine

        # the line formatter appends a new line to the end of each line, which
        # should be removed from the end of each region. Otherwise, an extra
        # newline will be printed after each selected region
        if (newRegionString[-1] == '\n'):
            newRegionString = newRegionString[0:-1]
        return newRegionString

    def getListOfLines(self, region):
        content = self.view.substr(region)
        return content.split('\n')


