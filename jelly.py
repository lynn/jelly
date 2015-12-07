import ast, functools, helper, itertools, math, operator, sympy

class attrdict(dict):
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		self.__dict__ = self

def arities(links):
	return [link.arity for link in links]

def copy(value):
	atoms['®'].call = lambda: value
	return value

def depth(link):
	if type(link) != list and type(link) != tuple:
		return 0
	return 1 + depth(link[0])

def depth_match(link_depth, arg):
	return link_depth == -1 or link_depth == depth(arg)

def literal(string):
	return attrdict(
		arity = 0,
		call = lambda: ast.literal_eval(string)
	)

def variadic_chain(chain, args):
	args = list(filter(None.__ne__, args))
	if len(args) == 0:
		return niladic_chain(chain)
	if len(args) == 1:
		return monadic_chain(chain, args[0])
	if len(args) == 2:
		return dyadic_chain(chain, args)
	raise hell # unimplemented

def niladic_link(link):
	return link.call()

def niladic_chain(chain):
	if len(chain) > 1 and chain[1].arity == 0:
		return dyadic_chain(chain[2:], (chain[0].call(), chain[1].call()))
	return monadic_chain(chain[1:], chain[0].call())

def monadic_link(link, arg):
	if depth_match(link.depth, arg):
		return link.call(arg)
	if depth(arg) < link.depth:
		return monadic_link(link, [arg])
	return [monadic_link(link, z) for z in arg]

def monadic_chain(chain, arg):
	ret = arg
	while chain:
		if arities(chain[0:3]) == [2, 2, 0]:
			ret = dyadic_link(chain[0], (ret, dyadic_link(chain[1], (arg, niladic_link(chain[2])))))
			chain = chain[3:]
		elif arities(chain[0:2]) == [2, 1]:
			ret = dyadic_link(chain[0], (ret, monadic_link(chain[1], arg)))
			chain = chain[2:]
		elif arities(chain[0:2]) == [2, 0]:
			ret = dyadic_link(chain[0], (ret, niladic_link(chain[1])))
			chain = chain[2:]
		elif arities(chain[0:2]) == [0, 2]:
			ret = dyadic_link(chain[1], (niladic_link(chain[0]), ret))
			chain = chain[2:]
		elif chain[0].arity == 2:
			ret = dyadic_link(chain[0], (ret, arg))
			chain = chain[1:]
		else:
			ret = monadic_link(chain[0], ret)
			chain = chain[1:]
	return ret

def dyadic_link(link, args):
	larg, rarg = args
	if depth_match(link.ldepth, larg) and depth_match(link.rdepth, rarg):
		return link.call(larg, rarg)
	if depth(larg) < link.ldepth:
		return dyadic_link(link, ([larg], rarg))
	if depth(rarg) < link.rdepth:
		return dyadic_link(link, (larg, [rarg]))
	if depth(larg) - depth(rarg) < link.ldepth - link.rdepth:
		return [dyadic_link(link, (larg, y)) for y in rarg]
	if depth(larg) - depth(rarg) > link.ldepth - link.rdepth:
		return [dyadic_link(link, (x, rarg)) for x in larg]
	return [dyadic_link(link, z) for z in zip(*args)]

def dyadic_chain(chain, args):
	larg, rarg = args
	if chain[0].arity in (-1, 2):
		ret = dyadic_link(chain[0], args)
		chain = chain[1:]
	else:
		ret = larg
	while chain:
		if arities(chain[0:3]) == [2, 2, 0]:
			ret = dyadic_link(chain[1], (dyadic_link(chain[0], (ret, rarg)), niladic_link(chain[2])))
			chain = chain[3:]
		elif arities(chain[0:2]) == [2, 2]:
			ret = dyadic_link(chain[0], (ret, dyadic_link(chain[1], args)))
			chain = chain[2:]
		elif arities(chain[0:2]) == [2, 0]:
			ret = dyadic_link(chain[0], (ret, niladic_link(chain[1])))
			chain = chain[2:]
		elif chain[0].arity == 2:
			ret = dyadic_link(chain[0], (ret, rarg))
			chain = chain[1:]
		elif chain[0].arity == 1:
			ret = monadic_link(chain[0], ret)
			chain = chain[1:]
		else:
			raise hell # unimplemented
	return ret

atoms = {
	'Ȧ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[0], z)
	),
	'ȧ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[0], (x, y))
	),
	'Ḃ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[1], z)
	),
	'ḃ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[1], (x, y))
	),
	'Ċ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[2], z)
	),
	'ċ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[2], (x, y))
	),
	'Ḋ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[3], z)
	),
	'ḋ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[3], (x, y))
	),
	'Ė': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[4], z)
	),
	'ė': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[4], (x, y))
	),
	'Ḟ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[5], z)
	),
	'ḟ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[5], (x, y))
	),
	'Ġ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[6], z)
	),
	'ġ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[6], (x, y))
	),
	'Ḣ': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(link_stack[7], z)
	),
	'ḣ': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(link_stack[7], (x, y))
	),
	'a': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = lambda x, y: x and y
	),
	'B': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: helper.toBase(z, 2)
	),
	'b': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = lambda x, y: helper.toBase(x, y)
	),
	'c': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = lambda x, y: helper.div(helper.pi(x), helper.pi(x - y) * helper.pi(y))
	),
	'I': attrdict(
		arity = 1,
		depth = 1,
		call = lambda z: helper.fromBase(z, 2)
	),
	'i': attrdict(
		arity = 2,
		ldepth = 1,
		rdepth = 0,
		call = lambda x, y: helper.fromBase(x, y)
	),
	'L': attrdict(
		arity = 1,
		depth = -1,
		call = len
	),
	'S': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: functools.reduce(lambda x, y: dyadic_link(atoms['+'], (x, y)), z, 0)
	),
	'N': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: -z
	),
	'O': attrdict(
		arity = 1,
		depth = 1,
		call = lambda z: functools.reduce(operator.add, [[u + 1] * v for u, v in enumerate(z)])
	),
	'o': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = lambda x, y: x or y
	),
	'P': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: functools.reduce(lambda x, y: dyadic_link(atoms['×'], (x, y)), z, 1)
	),
	'R': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: list(range(1, z + 1))
	),
	'r': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = lambda x, y: list(range(x, y))
	),
	'U': attrdict(
		arity = 1,
		depth = 1,
		call = lambda z: z[::-1]
	),
	'x': attrdict(
		arity = 2,
		ldepth = 1,
		rdepth = 1,
		call = lambda x, y: functools.reduce(operator.add, [u * [v] for u, v in zip(x, y)])
	),
	'!': attrdict(
		arity = 1,
		depth = 0,
		call = helper.pi
	),
	'=': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.eq
	),
	';': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: (x if depth(x) else [x]) + (y if depth(y) else [y])
	),
	'+': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.add
	),
	'_': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.sub
	),
	'×': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.mul
	),
	'÷': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = helper.div
	),
	'%': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.mod
	),
	'*': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.pow
	),
	'&': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.and_
	),
	'^': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.xor
	),
	'|': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = operator.or_
	),
	'~': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: ~z
	),
	'²': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: z ** 2
	),
	'½': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: z ** 0.5
	),
	'¬': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: int(not z)
	),
	'‘': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: z + 1
	),
	'’': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: z - 1
	),
	'«': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = min
	),
	'»': attrdict(
		arity = 2,
		ldepth = 0,
		rdepth = 0,
		call = max
	),
	'©': attrdict(
		arity = 1,
		depth = -1,
		call = copy
	),
	'®': attrdict(
		arity = 0,
		depth = -1
	),
	'{': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: x
	),
	'¹': attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: z
	),
	'}': attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: y
	),
	'ÆC': attrdict(
		arity = 1,
		depth = 0,
		call = sympy.ntheory.generate.primepi
	),
	'ÆN': attrdict(
		arity = 1,
		depth = 0,
		call = sympy.ntheory.generate.prime
	),
	'Æn': attrdict(
		arity = 1,
		depth = 0,
		call = sympy.ntheory.generate.nextprime
	),
	'ÆP': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: int(sympy.primetest.isprime(z))
	),
	'Æp': attrdict(
		arity = 1,
		depth = 0,
		call = sympy.ntheory.generate.prevprime
	),
	'ÆR': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: list(sympy.ntheory.generate.primerange(2, z + 1))
	),
	'Æ²': attrdict(
		arity = 1,
		depth = 0,
		call = lambda z: int(helper.isqrt(z) ** 2 == z)
	),
	'Æ½': attrdict(
		arity = 1,
		depth = 0,
		call = helper.isqrt
	),
}

overs = {
	'/': lambda atom: attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: functools.reduce(lambda x, y: dyadic_link(atom, (x, y)), z)
	),
	'\\': lambda atom: attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: list(itertools.accumulate(z, lambda x, y: dyadic_link(atom, (x, y))))
	)
}

hypers = {
	'@': lambda atom: attrdict(
		arity = 2,
		ldepth = atom.rdepth,
		rdepth = atom.ldepth,
		call = lambda x, y: atom.call(y, x)
	)
}

joints = {
	'$': lambda atoms: attrdict(
		arity = 0,
		call = lambda z: niladic_chain(atoms)
	),
	'€': lambda atoms: attrdict(
		arity = 1,
		depth = -1,
		call = lambda z: monadic_chain(atoms, z)
	),
	'£': lambda atoms: attrdict(
		arity = 2,
		ldepth = -1,
		rdepth = -1,
		call = lambda x, y: dyadic_chain(atoms, (x, y))
	)
}