from gr_hier_block2 import gr_hier_block2

class gr_top_block(gr_hier_block2):
	""
	def __init__(self, name, catch_exceptions = True):
		""
		super().__init__(name, (0,0,0), (0,0,0))
		# d_impl = new top_block_impl(this, catch_exceptions)
		
	##################
	# connect herite #
	##################
	
	######################
	# msg_connect herite #
	######################
	
	def start(self, max_noutput_items = 100000000):
		""
		pass
	