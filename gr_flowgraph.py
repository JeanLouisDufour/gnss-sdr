

class flowgraph():
	""
	def __init__(self):
		""
		self.d_edges = []

	def connect(self, src, dst):
		""
		#check_valid_port(src[0].output_signature(), src[1])
		#check_valid_port(dst[0].input_signature(), dst[1])
		#check_dst_not_used(dst)
		#check_type_match(src, dst)
		
		## Alles klar, Herr Kommissar
		self.d_edges.append((src, dst))
	