from gr_block import gr_block

class gr_sync_block(gr_block):
	""
	def __init__(self, name, input_signature, output_signature):
		""
		super().__init__(name, input_signature, output_signature)
		self.set_fixed_rate(True)