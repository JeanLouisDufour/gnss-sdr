from gnss_block_interface import GNSSBlockInterface
from gr_blocks_copy import gr_blocks_copy
import DLOG

class Pass_Through(GNSSBlockInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		# .h
		self.conjugate_cc_ = self.conjugate_ic_ = self.conjugate_sc_ = \
		self.in_streams_ = None
		self.inverted_spectrum = None # BIZARRE, pas de _ final
		self.item_size_ = self.item_type_ = \
		self.kludge_copy_ = \
		self.out_streams_ = \
		self.role_ = None
		# .cc
		self.role_ = role
		self.in_streams_ = in_streams
		self.out_streams_ = out_streams
		default_item_type = "gr_complex"
		input_type = configuration.get(role + ".input_item_type", default_item_type)
		output_type = configuration.get(role + ".output_item_type", default_item_type)
		assert input_type == output_type
		self.item_type_ = configuration.get(role + ".item_type", input_type)
		self.inverted_spectrum = configuration.get(role + ".inverted_spectrum", False)
		if self.item_type_ == "float":
			assert False
		elif self.item_type_ == "gr_complex":
			self.item_size_ = 8 # sizeof(gr_complex)
			assert self.inverted_spectrum is False
		else:
			assert False
		self.kludge_copy_ = gr_blocks_copy(self.item_size_) # gr::blocks::copy::make(item_size_);
		max_source_buffer_samples = configuration.get("GNSS-SDR.max_source_buffer_samples", 0)
		assert max_source_buffer_samples == 0
		
	def connect(self, top_block):
		""
		DLOG.INFO("nothing to connect internally")
	
	def get_left_block(self):
		""
		assert self.inverted_spectrum is False
		return self.kludge_copy_
	
	def get_right_block(self):
		""
		assert self.inverted_spectrum is False
		return self.kludge_copy_
	