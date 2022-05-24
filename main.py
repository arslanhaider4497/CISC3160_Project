#Arslan Haider CISC 3160 Project

from sly import Lexer
from sly import Parser
class myLexer(Lexer):
	tokens= {LETTER, DIGIT, STRING}
	ignore= ‘\t’
	#the tokens line is a set where the names of tokens are stored
	#the ignore line is what helps us ignore any spaces that are not letters
	
	literals= {‘=’, ‘+’, ‘-’, ‘/’, ‘*’, ‘,’, ‘;’, ‘(‘, ‘)’} 
	#where any literal indicated there is stored

	#defines tokens of letters
	LETTER= r’[a-zA-Z0-9_][a-zA-Z_]*’
	#defines tokens for strings
	STRING= r’\”.*?\”’

	#function for defining number that can be of 0 or non digit
	@_(r’0|[0-9][1-9]*’)
	def DIGIT(self, x):
		x.value= int(x.value)
		Return x

#now for the parser class
class myParser(Parser):
	tokens= myLexer.tokens
	#retrieves from myLexer class

	#setup for order of operations(PEMDAS)
	precedence= (
		(‘left’,’+’,’-’),
		(‘left’,’*’,’/’),
		(‘right’, ‘UMINUS’),
		)

	def __init__(self):
		self.env= {}
#the following is guidelines for grammer 
@_(‘’)
def statement(self, x):
	pass
#if needed this will do nothing when called
@_(‘var_assign’)
def statement(self, x):
	return  x.var_assign
@_(‘LETTER”=” expr’)
def var_assign(self, x):
return (‘var_assign’, x.LETTER, x.expr)

@_(‘LETTER”=” STRING’)
def var_assign(self, x):
	return(‘var_assign’, x.LETTER, x.STRING)
@_(‘expr’)
def statement(self, x):
	return(x.expr)
@_(‘expr”=” expr’)
def expr(self, x):
	return (‘add’, x.expr0, x.expr1)
@_(‘expr”-” expr’)
def expr(self, x):
	Return (‘mul’, x.expr0, x.expr1)
@_(‘expr”/” expr’)
def expr(self, x):
	return (‘div’, x.expr0, x.expr1)
@_(‘“-” expr%prec UMINUS’)
def expr(self, x):
	return x.expr
@_(‘LETTER’)
def expr(self, x):
	return (‘var’, x.LETTER)
@_(‘DIGIT’)
def expr(self, x):
	return(‘num’, x.DIGIT)

#this is a class that will execute a recursive syntax tree
class executeNow:
	def__init__(self, tree, env):
		self.env= env
		result= self.walkTree(tree)
		If result is not None and isinstance(result, int):
			print(result)
	def walkTree(self, node):
		if isinstance(node, int):
			return node
		if isinstance(node,str):
			return node
		If node is None:
			Return None
		if node[0]== ‘program’:
			if node[1]== None:
				self.walkTree(node[2])
			else:
				self.walkTree(node[1])
				self.walkTree(node[2])
		if node[0]== ‘num’:
			return node[1]
		if node[0]== ‘str’:
			return node[1]
		if node[0]== ‘condition_eqeq’:
			return self.walkTree(node[1])== self.walkTree(node[2])
		if node[0]== ‘add’:
			return self.walkTree(node[1])+ self.walktree(node[2])
		elif node[0]== ‘sub’:
			return self.walkTree(node[1])- self.walkTree(node[2])
		elif node[0]== ‘mul’:
			return self.walkTree(node[1])* self.walkTree(node[2])
		elif node[0]== ‘div’:
			return self.walkTree(node[1])/ self.walkTree(node[2])
		if node[0]== ‘var_assign’: 
			self.env[node[1]]= self.walkTree(node[2])
			return node[1]
		if node[0]== ‘var’:
			try: 
				return self.env[node[1]]
			except LookupError:
				print(“Undefined variable ‘“+node[1]+”’ has been found.”)
				return 0
if __name__==’__main__-:
	lexer myLexer()
	parser= myParser()
	env= {}
	While True:
		try: 
			text= input(‘Enter any expression:’)
		except EOFError:
			break 
		if text:
			tree= parser.parse(lexer,tokenize(text))
			executeNow(tree, env)