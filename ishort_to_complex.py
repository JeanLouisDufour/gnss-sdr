from gnss_block_interface import GNSSBlockInterface
from gr_blocks_interleaved_short_to_complex import gr_blocks_interleaved_short_to_complex
import DLOG

class IshortToComplex(GNSSBlockInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		# .h
		self.config_ = self.conjugate_cc_ = \
		self.dump_ = self.dump_filename_ = \
		self.file_sink_ = \
		self.gr_interleaved_short_to_complex_ = \
		self.in_streams_ = self.input_item_type_ = None
		self.inverted_spectrum = None  ## BIZARRE, pas de _ final
		self.out_streams_ = self.output_item_type_ = \
		self.role_ = None
		# .cc
		self.config_ = configuration
		self.role_ = role
		self.in_streams_ = in_streams
		self.out_streams_ = out_streams
		default_input_item_type = "short"
		default_output_item_type = "gr_complex"
		default_dump_filename = "../data/input_filter.dat"
		DLOG.INFO("role " + self.role_)
		self.input_item_type_ = self.config_.get(self.role_ + ".input_item_type", default_input_item_type)
		self.dump_ = self.config_.get(self.role_ + ".dump", False)
		self.dump_filename_ = self.config_.get(self.role_ + ".dump_filename", default_dump_filename)
		self.inverted_spectrum = configuration.get(role + ".inverted_spectrum", False)
		item_size = 8 # sizeof(gr_complex);
		self.gr_interleaved_short_to_complex_ = gr_blocks_interleaved_short_to_complex()
		# DLOG.INFO("data_type_adapter_(" + self.gr_interleaved_short_to_complex_->unique_id() + ")")
		assert self.inverted_spectrum is False
		assert self.dump_ is False
		assert self.in_streams_ <= 1
		assert self.out_streams_ <= 1

	def connect(self, top_block):
		""
		assert self.dump_ is False
		assert self.inverted_spectrum is False
		DLOG.INFO("Nothing to connect internally")
	
	def get_left_block(self):
		""
		return self.gr_interleaved_short_to_complex_
		
	def get_right_block(self):
		""
		assert self.inverted_spectrum is False
		return self.gr_interleaved_short_to_complex_