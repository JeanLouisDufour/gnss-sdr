import math, os # SEEK_SET, SEEK_CUR, SEEK_END
from gnss_block_interface import GNSSBlockInterface
from gnss_sdr_valve import Gnss_Sdr_Valve
from gr_blocks_file_source import gr_blocks_file_source
from gr_top_block import gr_top_block
import LOG, DLOG

class FileSignalSource(GNSSBlockInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams, queue):
		""
		# .h
		self.dump_ = self.dump_filename_ = \
		self.enable_throttle_control_ = \
		self.file_source_ = self.filename_ = \
		self.in_streams_ = self.item_size_ = self.item_type_ = \
		self.out_streams_ = \
		self.queue_ = \
		self.repeat_ = self.role_ = \
		self.samples_ = self.sampling_frequency_ = self.sink_ = \
		self.throttle_ = \
		self.valve_ = None
		# .cc
		self.role_ = role
		self.in_streams_ = in_streams
		self.out_streams_ = out_streams
		self.queue_ = queue
		default_filename = "./example_capture.dat"
		default_item_type = "short"
		default_dump_filename = "./my_capture.dat"
		default_seconds_to_skip = 0.0
		header_size = 0
		self.samples_ = configuration.get(role + ".samples", 0)
		self.sampling_frequency_ = configuration.get(role + ".sampling_frequency", 0)
		self.filename_ = configuration.get(role + ".filename", default_filename)
		self.item_type_ = configuration.get(role + ".item_type", default_item_type)
		self.repeat_ = configuration.get(role + ".repeat", False)
		self.dump_ = configuration.get(role + ".dump", False)
		self.dump_filename_ = configuration.get(role + ".dump_filename", default_dump_filename)
		self.enable_throttle_control_ = configuration.get(role + ".enable_throttle_control", False)
		seconds_to_skip = configuration.get(role + ".seconds_to_skip", default_seconds_to_skip)
		header_size = configuration.get(role + ".header_size", 0)
		samples_to_skip = 0
		is_complex = False
		if self.item_type_ == "gr_complex":
			self.item_size_ = 8 # sizeof(gr_complex)
		elif self.item_type_ == "float":
			self.item_size_ = 4 # sizeof(float)
		elif self.item_type_ == "short":
			self.item_size_ = 2 # sizeof(int16_t)
		elif self.item_type_ == "ishort":
			self.item_size_ = 2 # sizeof(int16_t)
			is_complex = True
		elif self.item_type_ == "byte":
			self.item_size_ = 1 # sizeof(int8_t)
		elif self.item_type_ == "ibyte":
			self.item_size_ = 1 # sizeof(int8_t)
			is_complex = True
		else:
			assert False
		self.file_source_ = gr_blocks_file_source(self.item_size_, self.filename_, self.repeat_)
		if seconds_to_skip > 0:
			samples_to_skip = seconds_to_skip * self.sampling_frequency_
			if is_complex:
				samples_to_skip *= 2
		if header_size > 0:
			samples_to_skip += header_size
		if samples_to_skip > 0:
			ok = self.file_source_.seek(samples_to_skip, SEEK_SET)
			assert ok, "Error skipping bytes!"
		if self.samples_ == 0: # read all file
			"""
             * BUG workaround: The GNU Radio file source does not stop the receiver after reaching the End of File.
             * A possible solution is to compute the file length in samples using file size, excluding the last 100 milliseconds, and enable always the
             * valve block
            """
			size = self.file_source_.py_stat_.st_size
			if size > 0:
				bytes_to_skip = samples_to_skip * self.item_size_
				bytes_to_process = size - bytes_to_skip
				self.samples_ = math.floor(float(bytes_to_process) / float(self.item_size_)) \
						  - math.ceil(0.002 * float(self.sampling_frequency_))
				# process all the samples available in the file excluding at least the last 1 ms
		assert self.samples_ > 0
		signal_duration_s = float(self.samples_) / float(self.sampling_frequency_)
		if is_complex:
			signal_duration_s /= 2.0
		print("GNSS signal recorded time to be processed: {} [s]".format(signal_duration_s))
		self.valve_ = Gnss_Sdr_Valve(self.item_size_, self.samples_, self.queue_)
		if self.dump_:
			assert False
		if self.enable_throttle_control_:
			assert False
		assert self.in_streams_ <= 0
		assert self.out_streams_ <= 1

	def connect(self, top_block):
		""
		assert isinstance(top_block, gr_top_block) 
		if self.samples_ > 0:
			if self.enable_throttle_control_:
				top_block.connect(self.file_source_, 0, self.throttle_, 0)
				DLOG.INFO("connected file source to throttle")
				top_block.connect(self.throttle_, 0, self.valve_, 0)
				DLOG.INFO("connected throttle to valve")
				if self.dump_:
					assert False
			else:
				top_block.connect(self.file_source_, 0, self.valve_, 0)
				DLOG.INFO("connected file source to valve")
				if self.dump_:
					assert False
		else:
			if self.enable_throttle_control_:
				top_block.connect(self.file_source_, 0, self.throttle_, 0)
				DLOG.INFO("connected file source to throttle")
				if self.dump_:
					assert False
			else:
				if self.dump_:
					assert False

	def get_right_block(self):
		""
		if self.samples_ > 0:
			return self.valve_
		elif self.enable_throttle_control_ == True:
			return self.throttle_
		else:
			return self.file_source_
		
	def implementation(self):
		""
		return "File_Signal_Source"
	