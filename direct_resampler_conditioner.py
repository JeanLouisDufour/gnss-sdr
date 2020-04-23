from gnss_block_interface import GNSSBlockInterface
from gr_block import gr_block
import gr_complex
import DLOG
import math, sys

class direct_resampler_conditioner_cc(gr_block):
	""
	def __init__(self, sample_freq_in, sample_freq_out):
		""
		super().__init__("direct_resampler_conditioner_cc", (1, 1, gr_complex.sizeof), (1, 1, gr_complex.sizeof))
		self.d_sample_freq_in = sample_freq_in
		self.d_sample_freq_out = sample_freq_out
		self.d_phase = 0
		self.d_lphase = 0
		if self.d_sample_freq_in >= self.d_sample_freq_out:
			self.d_phase_step = int(math.floor((2**32 * sample_freq_out) / sample_freq_in))
		else:
			self.d_phase_step = int(math.floor((2**32 * sample_freq_in) / sample_freq_out));
		self.set_relative_rate(1.0 * sample_freq_out / sample_freq_in);
		self.set_output_multiple(1);

	def forecast(self, noutput_items, ninput_items_required):
		""
		nreqd = max(1, (noutput_items + 1) * self.sample_freq_in / self.sample_freq_out + self.d_history - 1)
		ninputs = len(ninput_items_required)
		for i in range(ninputs):
			ninput_items_required[i] = nreqd
		
	def general_work(self, noutput_items, ninput_items, input_items, output_items):
		""
		assert False
		
	########### impl ################
	
	
class DirectResamplerConditioner(GNSSBlockInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		# .h
		self.dump_ = \
		self.dump_filename_ = \
		self.file_sink_ = \
		self.in_stream_ = \
		self.item_size_ = \
		self.item_type_ = \
		self.out_stream_ = \
		self.resampler_ = \
		self.role_ = \
		self.sample_freq_in_ = \
		self.sample_freq_out_ = None
		# cc
		self.role_ = role
		self.in_streams_ = in_streams
		self.out_streams_ = out_streams
		default_item_type = "short"
		default_dump_file = "./data/signal_conditioner.dat"
		fs_in_deprecated = configuration.get("GNSS-SDR.internal_fs_hz", 2048000.0)
		fs_in = configuration.get("GNSS-SDR.internal_fs_sps", fs_in_deprecated)
		self.sample_freq_in_ = configuration.get(self.role_ + ".sample_freq_in", 4000000.0)
		self.sample_freq_out_ = configuration.get(self.role_ + ".sample_freq_out", fs_in)
		if math.fabs(fs_in - self.sample_freq_out_) > sys.float_info.epsilon:
			assert False
		self.item_type_ = configuration.get(role + ".item_type", default_item_type)
		self.dump_ = configuration.get(role + ".dump", False)
		self.dump_filename_ = configuration.get(role + ".dump_filename", default_dump_file)
		if self.item_type_ == "gr_complex":
			self.item_size_ = 8 # sizeof(gr_complex)
			self.resampler_ = direct_resampler_conditioner_cc(self.sample_freq_in_, self.sample_freq_out_)
		else:
			assert False
		assert self.dump_ is False
		
	def connect(self, top_block):
		""
		assert self.dump_ is False
		DLOG.INFO("nothing to connect internally")
	
	def get_left_block(self):
		""
		return self.resampler_
	