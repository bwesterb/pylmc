import objectfile

class LMCAssemblerException(Exception): pass
class SyntaxError(LMCAssemblerException): pass
class LabelNotFound(LMCAssemblerException): pass
class DuplicateLabel(LMCAssemblerException): pass
class UnknownInstruction(LMCAssemblerException): pass

class LMCAssembler(object):
	def __init__(self):
		self.instr = []
	def parse_line(self, l):
		l = l[:-1].strip()
		l = l.split('#')[0]
		if not l:
			return None
		bits = [bit.strip().lower() for bit in l.split() if bit.strip()]
		if len(bits) == 0:
			return None
		if len(bits) > 3:
			raise SyntaxError
		if len(bits) == 1:
			return (None, self.mnemonic_to_code(bits[0]), None)
		elif len(bits) == 2:
			try:
				return (bits[0], self.mnemonic_to_code(bits[1]),
						None)
			except UnknownInstruction:
				return (None, self.mnemonic_to_code(bits[0]),
						bits[1])
		else: # len(bits) == 3
			return (bits[0], self.mnemonic_to_code(bits[1]),
					bits[2])

	def mnemonic_to_code(self, v):
		if v == 'hlt':
			return 0
		elif v == 'inp':
			return 901
		elif v == 'out':
			return 902
		elif v == 'add':
			return 100
		elif v == 'sub':
			return 200
		elif v == 'sta':
			return 300
		elif v == 'lda':
			return 500
		elif v == 'bra':
			return 600
		elif v == 'brz':
			return 700
		elif v == 'brp':
			return 800
		elif v == 'dat':
			return 000
		else:
			raise UnknownInstruction

	def parse_file(self, f):
		for l in f.readlines():
			parsed = self.parse_line(l)
			if parsed is None:
				continue
			self.instr.append(parsed)

	def resolve_labels(self):
		lut = dict()
		for n, l in enumerate(self.instr):
			if l[0] is None:
				continue
			if l[0] in lut:
				raise DuplicateLabel
			lut[l[0]] = n
		for n, l in enumerate(self.instr):
			if l[2] is None:
				continue
			if isinstance(l[2], int):
				continue
			if l[2].isdigit():
				self.instr[n] = (l[0], l[1], int(l[2]))
				continue
			if not l[2] in lut:
				raise LabelNotFound, l[2]
			self.instr[n] = (l[0], l[1], lut[l[2]])
	
	def emit(self):
		ret = []
		for l, c, r in self.instr:
			if not r is None:
				c += r
			ret.append(c)
		return ret

	def assemble(self, f):
		self.parse_file(f)
		self.resolve_labels()
		ret = self.emit()
		return ret + ([0] * (100 - len(ret)))

def assemble(f):
	return LMCAssembler().assemble(f)

def main():
	import optparse
	usage = 'usage: %prog [options] filein [fileout]'
	parser = optparse.OptionParser(usage=usage)
	(options, args) = parser.parse_args()
	if len(args) == 0:
		parser.print_help()
		return
	if len(args) == 1:
		bits = args[0].rsplit('.', 1)
		if bits[-1] == 'lmc':
			bits[-1] = 'lmco'
		args.append('.'.join(bits))
	with open(args[0], 'r') as fi, \
	     open(args[1], 'w') as fo:
		objectfile.save(fo, assemble(fi))

if __name__ == '__main__':
	main()

