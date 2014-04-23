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

        # dont use tabs -- they arent always rendered how we want in
        # a browser text field
        for line in lines:
            fmtted = fmtted + (" " * int(self.indent))
            fmtted = fmtted + line + "\n"
        
        return fmtted

  
# Extends TextCommand so that run() receives a View to modify.  
class FixedWidthCommand(sublime_plugin.TextCommand):  
    def run(self, edit, numCols = 80):
        if (type(numCols) != int):
            numCols = int(numCols)
        listOfLines = self.getListOfLines()
        
        # necessary so we start inserting at the bottom of the file
        self.moveCursorToBottomOfRegion(edit)
        self.printHeader(edit, numCols)
        self.printListOfLines(edit, listOfLines, numCols)
        self.printFooter(edit)
        

    def getListOfLines(self):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        return content.split('\n')

    def moveCursorToBottomOfRegion(self, edit):
        screenful = self.view.visible_region()

        # calculate last row / col of the visible region
        row = self.view.rowcol(screenful.b)[0]
        col = self.view.rowcol(screenful.b)[1]
        target = self.view.text_point(row, 1000000)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))

        self.view.insert(edit, self.view.sel()[0].end(), "\n")
        
    
    def printHeader(self, edit, numCols):
        self.view.insert(edit, self.view.sel()[0].end(), "\n\n")
        self.view.insert(edit, self.view.sel()[0].end(), "[ Formatted to " + str(numCols) + " columns wide ]\n")
        self.view.insert(edit, self.view.sel()[0].end(), "\n")
   
    def printFooter(self, edit):
        self.view.insert(edit, self.view.sel()[0].end(), "\n")
        self.view.insert(edit, self.view.sel()[0].end(), "[ End formatting ]\n")

    def printListOfLines(self, edit, listOfLines, numCols):
        for l in listOfLines:
            lineObj = line(l, numCols)
            formattedLine = lineObj.format()
            self.view.insert(edit, self.view.sel()[0].end(), formattedLine)



