import zlib
import struct

class UnknownFormat(Exception): pass
class FormatError(Exception): pass

def load(f):
	header = f.read(4)
	if header == 'LMC0':
		return load_lmc0(f)
	else:
		raise UnknownFormat

def load_lmc0(f):
	ret = []
	l = struct.unpack('<H', f.read(2))[0]
	s = zlib.decompress(f.read(l))
	if len(s) != 300:
		raise FormatError
	for i in xrange(100):
		ret.append(int(s[3*i:3*i+3]))
	return ret

def save(f, mem):
	save_lmc0(f, mem)

def save_lmc0(f, mem):
	f.write('LMC0')
	mem = mem + ([0] * (100 - len(mem)))
	r = ''
	for v in mem:
		r += str(v).zfill(3)
	r = zlib.compress(r)
	f.write(struct.pack('<H', len(r)))
	f.write(r)
