from channel import ChannelFsm
from gnss_block_interface import GNSSBlockInterface
import GPS, gr_complex
from pcps_acquisition import pcps_acquisition
import DLOG
import math, numpy as np

class AcquisitionInterface(GNSSBlockInterface):
	""
	pass

class GpsL1CaPcpsAcquisition(AcquisitionInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		# .h
		self.acq_parameters_ = {'it_size' : 1, 'resampler_ratio' : 1.0} # Acq_Conf
		### tous les autres a 0/false
		# .cc
		self.role_ = role
		self.in_streams_ = in_streams
		self.out_streams_ = out_streams
		self.configuration_ = configuration
		default_item_type = "gr_complex"
		default_dump_filename = "./acquisition.mat"

		DLOG.INFO("role " + role)

		self.item_type_ = configuration.get(role + ".item_type", default_item_type)
		fs_in_deprecated = configuration.get("GNSS-SDR.internal_fs_hz", 2048000) # int64_t
		self.acq_parameters_['fs_in'] = self.fs_in_ = configuration.get("GNSS-SDR.internal_fs_sps", fs_in_deprecated)
		self.acq_parameters_['dump'] = self.dump_ = configuration.get(role + ".dump", False)
		self.acq_parameters_['dump_channel'] = configuration.get(role + ".dump_channel", 0)
		self.acq_parameters_['blocking'] = self.blocking_ = configuration.get(role + ".blocking", True)
		self.acq_parameters_['doppler_max'] = self.doppler_max_ = configuration.get(role + ".doppler_max", 5000)
		self.acq_parameters_['sampled_ms'] = self.sampled_ms_ = configuration.get(role + ".coherent_integration_time_ms", 1)
		self.acq_parameters_['ms_per_code'] = 1
		self.acq_parameters_['bit_transition_flag'] = self.bit_transition_flag_ = configuration.get(role + ".bit_transition_flag", False)
		self.acq_parameters_['use_CFAR_algorithm_flag'] = self.use_CFAR_algorithm_flag_ = configuration.get(role + ".use_CFAR_algorithm", True) # will be false in future versions
		self.acq_parameters_['max_dwells'] = self.max_dwells_ = configuration.get(role + ".max_dwells", 1)
		self.acq_parameters_['dump_filename'] = self.dump_filename_ = configuration.get(role + ".dump_filename", default_dump_filename)
		self.acq_parameters_['num_doppler_bins_step2'] = configuration.get(role + ".second_nbins", 4)
		self.acq_parameters_['doppler_step2'] = configuration.get(role + ".second_doppler_step", 125.0)
		self.acq_parameters_['make_2_steps'] = configuration.get(role + ".make_two_steps", False)
		self.acq_parameters_['use_automatic_resampler'] = configuration.get("GNSS-SDR.use_acquisition_resampler", False)
		if self.acq_parameters_['use_automatic_resampler'] and self.item_type_ != "gr_complex":
			assert False
		if self.acq_parameters_['use_automatic_resampler']:
			if self.acq_parameters_['fs_in'] > GPS.L1.CA.OPT_ACQ_FS_HZ:
				2+2
			assert False
		else:
			self.acq_parameters_['resampled_fs'] = self.fs_in_
			#--- Find number of samples per spreading code -------------------------
			self.code_length_ = int(math.floor(self.fs_in_ / (GPS.L1.CA.CODE_RATE_HZ / GPS.L1.CA.CODE_LENGTH_CHIPS)))
			self.acq_parameters_['samples_per_ms'] = self.fs_in_ * 0.001
			self.acq_parameters_['samples_per_chip'] = int(math.ceil(GPS.L1.CA.CHIP_PERIOD * float(self.acq_parameters_['fs_in'])))
		"""
    if (acq_parameters_.use_automatic_resampler == true and item_type_ != "gr_complex")
        {
            LOG(WARNING) << "GPS L1 CA acquisition disabled the automatic resampler feature because its item_type is not set to gr_complex";
            acq_parameters_.use_automatic_resampler = false;
        }
    if (acq_parameters_.use_automatic_resampler)
        {
            if (acq_parameters_.fs_in > GPS_L1_CA_OPT_ACQ_FS_HZ)
                {
                    acq_parameters_.resampler_ratio = floor(static_cast<float>(acq_parameters_.fs_in) / GPS_L1_CA_OPT_ACQ_FS_HZ);
                    uint32_t decimation = acq_parameters_.fs_in / GPS_L1_CA_OPT_ACQ_FS_HZ;
                    while (acq_parameters_.fs_in % decimation > 0)
                        {
                            decimation--;
                        };
                    acq_parameters_.resampler_ratio = decimation;
                    acq_parameters_.resampled_fs = acq_parameters_.fs_in / static_cast<int>(acq_parameters_.resampler_ratio);
                }
            //--- Find number of samples per spreading code -------------------------
            code_length_ = static_cast<unsigned int>(std::floor(static_cast<double>(acq_parameters_.resampled_fs) / (GPS_L1_CA_CODE_RATE_HZ / GPS_L1_CA_CODE_LENGTH_CHIPS)));
            acq_parameters_.samples_per_ms = static_cast<float>(acq_parameters_.resampled_fs) * 0.001;
            acq_parameters_.samples_per_chip = static_cast<unsigned int>(ceil(GPS_L1_CA_CHIP_PERIOD * static_cast<float>(acq_parameters_.resampled_fs)));
        }
    else
        {
            acq_parameters_.resampled_fs = fs_in_;
            //--- Find number of samples per spreading code -------------------------
            code_length_ = static_cast<unsigned int>(std::floor(static_cast<double>(fs_in_) / (GPS_L1_CA_CODE_RATE_HZ / GPS_L1_CA_CODE_LENGTH_CHIPS)));
            acq_parameters_.samples_per_ms = static_cast<float>(fs_in_) * 0.001;
            acq_parameters_.samples_per_chip = static_cast<unsigned int>(ceil(GPS_L1_CA_CHIP_PERIOD * static_cast<float>(acq_parameters_.fs_in)));
        }
		"""
		self.acq_parameters_['samples_per_code'] = self.acq_parameters_['samples_per_ms'] * float(GPS.L1.CA.CODE_PERIOD * 1000.0)
		tmp = math.floor(self.acq_parameters_['sampled_ms'] * self.acq_parameters_['samples_per_ms']) * (2 if self.acq_parameters_['bit_transition_flag'] else 1)
		self.vector_length_ = int(math.floor(tmp+0.5))
		assert abs(self.vector_length_ - tmp) < 1e-5
		self.code_ = np.zeros(self.vector_length_, dtype=np.complex64)

		if self.item_type_ == "cshort":
			assert False # item_size_ = sizeof(lv_16sc_t);
		else:
			self.item_size_ = gr_complex.sizeof

		self.acq_parameters_['it_size'] = self.item_size_
		self.acq_parameters_['blocking_on_standby'] = configuration.get(role + ".blocking_on_standby", False)
		self.acquisition_ = pcps_acquisition(self.acq_parameters_)
		DLOG.INFO("acquisition(" + str(self.acquisition_.unique_id()) + ")")
	"""
    if (item_type_ == "cbyte")
        {
            cbyte_to_float_x2_ = make_complex_byte_to_float_x2();
            float_to_complex_ = gr::blocks::float_to_complex::make();
        }

    channel_ = 0;
    threshold_ = 0.0;
    doppler_step_ = 0;
    doppler_center_ = 0;
    gnss_synchro_ = nullptr;

    if (in_streams_ > 1)
        {
            LOG(ERROR) << "This implementation only supports one input stream";
        }
    if (out_streams_ > 0)
        {
            LOG(ERROR) << "This implementation does not provide an output stream";
        }
		"""
		
	def connect(self, top_block):
		""
		assert self.item_type_ == "gr_complex"
		pass # // nothing to connect
	
	def get_right_block(self):
		""
		return self.acquisition_
	
	def set_channel(self, channel):
		""
		assert isinstance(channel, int)
		self.channel_ = channel
		self.acquisition_.set_channel(channel)
	
	def set_channel_fsm(self, channel_fsm):
		""
		assert isinstance(channel_fsm, ChannelFsm)
		self.channel_fsm_ = channel_fsm
		self.acquisition_.set_channel_fsm(channel_fsm)
		
	def set_gnss_synchro(self, gnss_synchro):
		""
		assert gnss_synchro[''] == 'Gnss_Synchro'
		self.gnss_synchro_ = gnss_synchro
		self.acquisition_.set_gnss_synchro(gnss_synchro)
	