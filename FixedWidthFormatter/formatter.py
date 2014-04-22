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
        lines = textwrap.wrap(self.content, self.numCols - self.indent)
        fmtted = ""

        # dont use tabs -- they arent always rendered how we want in
        # a browser text field
        for line in lines:
            fmtted = fmtted + (" " * int(self.indent))
            fmtted = fmtted + line + "\n"
        
        return fmtted
    
    # not used in this plugin, but it can be used in other contexts. TODO: make
    # use of the format method instead of the duplicate code below              
    def printLine(self, file, cols):
        assert(file.closed == False)
        lines = textwrap.wrap(self.content, cols - self.indent)
        
        # a line that was originally a new line or only blank space will have
        # been broken up into zero lines by the textwrap module. Therefore, 
        # a single newline must be printed
        if len(lines) == 0:
            file.write("\n")
            return
            
        for _line in lines:
            file.write(" " * int(self.indent))
            file.write(_line + "\n")

  
# Extends TextCommand so that run() receives a View to modify.  
class WrcFormatCommand(sublime_plugin.TextCommand):  
    def run(self, edit):
        # TODO: change to parameter!
        numCols = 88
        listOfLines = self.getListOfLines()
        
        # necessary so we start inserting at the bottom of the file
        self.moveCursorToBottomOfRegion(edit)
        self.printWrcActionHeader(edit, numCols)
        self.printListOfLines(edit, listOfLines, numCols)
        self.printWrcActionFooter(edit)
        

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
        
    
    def printWrcActionHeader(self, edit, numCols):
        self.view.insert(edit, self.view.sel()[0].end(), "\n\n")
        self.view.insert(edit, self.view.sel()[0].end(), "[ Formatted to " + str(numCols) + " columns wide ]\n")
        self.view.insert(edit, self.view.sel()[0].end(), "\n")
   
    def printWrcActionFooter(self, edit):
        self.view.insert(edit, self.view.sel()[0].end(), "\n")
        self.view.insert(edit, self.view.sel()[0].end(), "[ End WRC formatting ]\n")

    def printListOfLines(self, edit, listOfLines, numCols):
        for l in listOfLines:
            lineObj = line(l, numCols)
            formattedLine = lineObj.format()
            self.view.insert(edit, self.view.sel()[0].end(), formattedLine)


