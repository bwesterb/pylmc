import objectfile

NEGATIVE = -1

class LMCException(Exception): pass
class Halt(LMCException): pass
class BadInstruction(LMCException): pass
class Overflow(LMCException): pass
class PCOverflow(Overflow): pass

class Register(object):
	def __init__(self, data):
		assert 0 <= data <= 999 or data == NEGATIVE
		self.data = data

	@property
	def instruction(self):
		if self.data == NEGATIVE:
			return None
		return self.data / 100

	@property
	def argument(self):
		if self.data == NEGATIVE:
			return None
		return self.data % 100

	@property
	def instruction_mnemonic(self):
		i, a = self.instruction, str(self.argument).zfill(2)
		if self.data == 000:
			return ("HLT", '')
		elif self.instruction is None:
			return ("NEG", '')
		elif self.instruction == 1:
			return ("ADD", a)
		elif self.instruction == 2:
			return ("SUB", a)
		elif self.instruction == 3:
			return ("STA", a)
		elif self.instruction == 5:
			return ("LDA", a)
		elif self.instruction == 6:
			return ("BRA", a)
		elif self.instruction == 7:
			return ("BRZ", a)
		elif self.instruction == 8:
			return ("BRP", a)
		elif self.data == 901:
			return ("INP", '')
		elif self.data == 902:
			return ("OUT", '')
		else:
			return ("DATA", '')

	def add(self, v):
		assert 0 <= v <= 999
		self.data += v
		if self.data > 999:
			raise Overflow
	
	def substract(self, v):
		assert 0 <= v <= 999
		self.data -= v
		if self.data < 0:
			self.data = -1

	def __str__(self):
		im, am = self.instruction_mnemonic
		return "%3s %3s%3s" % (str(self.data).zfill(3)
					if self.data >= 0 else '', im, am)

class Computer(object):
	def __init__(self, mem=None, acc=None, pc=None, inp=None, out=None,
			on_inp=None, on_out=None):
		if mem is None: mem = [0 for i in xrange(100)]
		if acc is None: acc = Register(0)
		if inp is None: inp = Register(0)
		if out is None: out = Register(0)
		if on_inp is None: on_inp = self.default_on_inp
		if on_out is None: on_out = self.default_on_out
		if pc is None:
			pc = 0
		self.mem = [Register(v) for v in mem]
		self.acc = acc
		self.inp = inp
		self.out = out
		self.on_out = on_out
		self.on_inp = on_inp
		self.pc = pc
	
	def default_on_inp(self):
		return int(raw_input("input> "))

	def default_on_out(self, v):
		print "Output: ", str(self.out)
	
	def _step_pc(self):
		self.pc += 1
		if self.pc > 99:
			raise PCOverflow
	
	def _jump_pc(self, a):
		assert 0 <= a <= 99
		self.pc = a
	
	def run(self):
		try:
			while True:
				print self
				self.step()
		except Halt:
			pass

	def step(self):
		reg = self.mem[self.pc]
		i, a = reg.instruction, reg.argument
		if reg.data == 000:		# HLT
			raise Halt
		elif i is None:
			raise BadInstruction
		elif i == 1:	# ADD
			self.acc.add(self.mem[a].data)
			self._step_pc()
		elif i == 2:	# SUB
			self.acc.substract(self.mem[a].data)
			self._step_pc()
		elif i == 3:	# STA
			self.mem[a].data = self.acc.data
			self._step_pc()
		elif i == 5:	# LDA
			self.acc.data = self.mem[a].data
			self._step_pc()
		elif i == 6:	# BRA
			self._jump_pc(a)
		elif i == 7:	# BRZ
			if self.acc.data == 0:
				self._jump_pc(a)
			else:
				self._step_pc()
		elif i == 8:	# BRP
			if self.acc.data == NEGATIVE:
				self._step_pc()
			else:
				self._jump_pc(a)
		elif reg.data == 901:		# INP
			self.inp.data = self.on_inp()
			self.acc.data = self.inp.data
			self._step_pc()
		elif reg.data == 902:		# OUT
			self.out.data = self.acc.data
			self.on_out(self.out.data)
			self._step_pc()
		else:
			raise BadInstruction
	
	def __str__(self):
		ret = ''
		for i in xrange(20):
			for j in xrange(5):
				flag = ''
				if i+20*j == self.pc:
					flag = '*'
				ret += "%1s%-15s" % (flag, self.mem[i+20*j])
			ret += '\n'
		ret += '             acc %-11s inp %-11s out %-15s' % (
				self.acc, self.inp, self.out)
		return ret

def main():
	import optparse
	usage = 'usage: %prog [options] objectfile'
	parser = optparse.OptionParser(usage=usage)
	(options, args) = parser.parse_args()
	if len(args) == 0:
		parser.print_help()
		return
	with open(args[0], 'r') as f:
		mem = objectfile.load(f)
	c = Computer(mem=mem)
	c.run()

if __name__ == '__main__':
	main()
