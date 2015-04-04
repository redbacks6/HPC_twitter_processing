
def main():
	example = Example()
	print example.printtext()


class Example():

	def __init__(self):
		
		self.text = 'Hello World'

	def printtext(self):
		return self.text


if __name__ == '__main__':
	main()