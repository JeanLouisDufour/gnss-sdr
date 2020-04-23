from gnss_block_interface import GNSSBlockInterface
import DLOG

class SignalConditioner(GNSSBlockInterface):
	""
	def __init__(self, configuration, data_type_adapt, in_filt, res, role, implementation):
		""
		self.data_type_adapt_ = data_type_adapt
		self.in_filt_ = in_filt
		self.res_ = res
		self.role_ = role
		self.implementation_ = implementation
		self.connected_ = False
		
	def connect(self, top_block):
		""
		assert not self.connected_
		self.data_type_adapt_.connect(top_block)
		self.in_filt_.connect(top_block)
		self.res_.connect(top_block)

		top_block.connect(self.data_type_adapt_.get_right_block(), 0, self.in_filt_.get_left_block(), 0);
		DLOG.INFO("data_type_adapter -> input_filter")

		top_block.connect(self.in_filt_.get_right_block(), 0, self.res_.get_left_block(), 0);
		DLOG.INFO("input_filter -> resampler")
		self.connected_ = True
		
	def get_left_block(self):
		""
		return self.data_type_adapt_.get_left_block()
	