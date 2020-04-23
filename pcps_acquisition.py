"""
This class implements a Parallel Code Phase Search Acquisition
 *
 *  Acquisition strategy (Kay Borre book + CFAR threshold).
 *  <ol>
 *  <li> Compute the input signal power estimation
 *  <li> Doppler serial search loop
 *  <li> Perform the FFT-based circular convolution (parallel time search)
 *  <li> Record the maximum peak and the associated synchronization parameters
 *  <li> Compute the test statistics and compare to the threshold
 *  <li> Declare positive or negative acquisition using a message queue
 *  </ol>
 *
 * Kay Borre book: K.Borre, D.M.Akos, N.Bertelsen, P.Rinder, and S.H.Jensen,
 * "A Software-Defined GPS and Galileo Receiver. A Single-Frequency
 * Approach", Birkhauser, 2007. pp 81-84
"""
from channel import ChannelFsm
from gr_block import gr_block
import gr_complex
from gr_fft_complex import gr_fft_complex
import math, numpy as np

class pcps_acquisition(gr_block):
	""
	def __init__(self, conf):
		""
		super().__init__("pcps_acquisition", (1, 1, conf['it_size']), (0, 0, conf['it_size']))
		self.d_conf = conf # acq_parameters
		self.message_port_register_out("events")
		self.d_sample_counter = 0
		self.d_active = False
		self.d_positive_acq = 0
		self.d_state = 0
		self.d_doppler_bias = 0
		self.d_num_noncoherent_integrations_counter = 0
		tmp = conf['sampled_ms'] * conf['samples_per_ms'] * (2 if conf['bit_transition_flag'] else 1)
		self.d_consumed_samples = int(math.floor(tmp+0.5))
		assert abs(self.d_consumed_samples - tmp) < 1e-5
		self.d_fft_size = self.d_consumed_samples * (1 if conf['sampled_ms'] == conf['ms_per_code'] else 2)
		self.d_mag = 0
		self.d_input_power = 0.0
		self.d_num_doppler_bins = 0
		self.d_threshold = 0.0
		self.d_doppler_step = 0
		self.d_doppler_center = 0
		self.d_doppler_center_step_two = 0.0
		self.d_test_statistics = 0.0
		self.d_channel = 0
		self.d_cshort = not (conf['it_size'] == gr_complex.sizeof)
		if conf['bit_transition_flag']:
			self.d_fft_size = self.d_consumed_samples * 2
			conf['max_dwells'] = 1
		self.d_tmp_buffer = np.zeros(self.d_fft_size, dtype=np.float32)
		self.d_fft_codes = np.zeros(self.d_fft_size, dtype=np.complex64)
		self.d_input_signal = np.zeros(self.d_fft_size, dtype=np.complex64)
		self.d_fft_if = gr_fft_complex(self.d_fft_size, True)
		self.d_ifft = gr_fft_complex(self.d_fft_size, False)
		self.d_gnss_synchro = None
		self.d_worker_active = False
		self.d_data_buffer = np.zeros(self.d_consumed_samples, dtype=np.complex64)
		if self.d_cshort:
			assert False
		self.grid_ = np.zeros(0, dtype=np.float32)
		self.narrow_grid_ = np.zeros(0, dtype=np.float32)
		self.d_step_two = False
		self.d_num_doppler_bins_step2 = conf['num_doppler_bins_step2']
		self.d_samplesPerChip = conf['samples_per_chip']
		self.d_buffer_count = 0
		if conf['max_dwells'] == 1:
			self.d_use_CFAR_algorithm_flag = conf['use_CFAR_algorithm_flag']
		else:
			self.d_use_CFAR_algorithm_flag = False
		self.d_dump_number = 0
		self.d_dump_channel = conf['dump_channel']
		self.d_dump = conf['dump']
		self.d_dump_filename = conf['dump_filename']
		if self.d_dump:
			assert False

	def set_channel(self, channel):
		""
		assert isinstance(channel, int)
		self.d_channel = channel
	
	def set_channel_fsm(self, channel_fsm):
		""
		assert isinstance(channel_fsm, ChannelFsm)
		self.d_channel_fsm = channel_fsm
	
	def set_gnss_synchro(self, gnss_synchro):
		""
		assert gnss_synchro[''] == 'Gnss_Synchro'
		self.d_gnss_synchro = gnss_synchro
	