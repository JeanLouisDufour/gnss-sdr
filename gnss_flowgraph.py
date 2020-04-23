from channel_status_msg_receiver import channel_status_msg_receiver
from gnss_block_factory import GNSSBlockFactory
from gr_top_block import gr_top_block
import jld_channels
import DLOG, LOG

class GNSSFlowgraph:
	""
# reverse dans jld_channels
#	evGPS_1C,evGPS_2S,evGPS_L5,evSBAS_1C,evGAL_1B,evGAL_5X, \
#	evGLO_1G,evGLO_2G,evBDS_B1,evBDS_B3 = range(10)
	
	def __init__(self, configuration, queue):
		""
		# .h
		self.acq_channels_count_ = None
		self.acq_resamplers_ = {}
		self.available_xx_signals_ = [[] for _ in range(10)]
		self.channels_ = []
		self.ch_out_sample_counter = None # BIZARRE : pas de _ terminal
		self.channels_count_ = None # int
		self.channels_state_ = []
		self.channels_status_ = None
		self.config_file_ = None # string
		self.configuration_ = None
		self.connected_ = None
		self.enable_monitor_ = None
		self.GnssSynchroMonitor_ = None
		self.mapStringValues_ = {}
		self.max_acq_channels_ = None
		self.null_sinks_ = []
		self.observables_ = None
		self.pvt_ = None
		self.queue_ = None
		self.running_ = None
		self.sig_conditioner_ = [] # vector GNSSBlockInterface
		self.sig_source_ = [] # vector GNSSBlockInterface
		self.signal_list_mutex = None
		self.sources_count_ = None
		self.top_block_ = None
		# .c
		self.configuration_ = configuration
		self.queue_ = queue
		self.block_factory_ = GNSSBlockFactory()
		self.channels_status_ = channel_status_msg_receiver()
		self.sources_count_ = self.configuration_.get("Receiver.sources_count", 1)
		RF_Channels = 0
		signal_conditioner_ID = 0
		if self.sources_count_ > 1:
			assert False
		else:
			self.sig_source_.append(self.block_factory_.GetSignalSource(self.configuration_, self.queue_, -1))
			RF_Channels = self.configuration_.get(self.sig_source_[0].role_ + ".RF_channels", 0)
			if RF_Channels != 0:
				assert False
			else:
				self.sig_conditioner_.append(self.block_factory_.GetSignalConditioner(self.configuration_, -1))
		self.observables_ = self.block_factory_.GetObservables(self.configuration_)
		default_str = "Default"
		obs_implementation = self.configuration_.get("Observables.implementation", default_str)
		if obs_implementation in ("GPS_L1_CA_Observables", "GPS_L2C_Observables", "Galileo_E1B_Observables", "Galileo_E5A_Observables"):
			assert False
		self.pvt_ = self.block_factory_.GetPVT(self.configuration_)
		pvt_implementation = self.configuration_.get("PVT.implementation", default_str)
		if pvt_implementation in ("GPS_L1_CA_PVT", "Galileo_E1_PVT", "Hybrid_PVT"):
			assert False
		channels = self.block_factory_.GetChannels(self.configuration_, self.queue_)
		self.channels_count_ = len(channels)
		self.channels_.extend(channels)
		
		self.top_block_ = gr_top_block("GNSSFlowgraph")
		
#		self.mapStringValues_["1C"] = GNSSFlowgraph.evGPS_1C
#		self.mapStringValues_["2S"] = GNSSFlowgraph.evGPS_2S
#		self.mapStringValues_["L5"] = GNSSFlowgraph.evGPS_L5
#		self.mapStringValues_["1B"] = GNSSFlowgraph.evGAL_1B
#		self.mapStringValues_["5X"] = GNSSFlowgraph.evGAL_5X
#		self.mapStringValues_["1G"] = GNSSFlowgraph.evGLO_1G
#		self.mapStringValues_["2G"] = GNSSFlowgraph.evGLO_2G
#		self.mapStringValues_["B1"] = GNSSFlowgraph.evBDS_B1
#		self.mapStringValues_["B3"] = GNSSFlowgraph.evBDS_B3
		self.mapStringValues_ = jld_channels.cid
		
		# fill the signals queue with the satellites ID's to be searched by the acquisition
		self.set_signals_list();
		self.set_channels_state();
		DLOG.INFO("Blocks instantiated. " + str(self.channels_count_) + " channels.")
		# Instantiate the receiver monitor block, if required
		self.enable_monitor_ = self.configuration_.get("Monitor.enable_monitor", False)
		assert not self.enable_monitor_
		### JLD
		assert self.sources_count_ == len(self.sig_source_)
		assert self.channels_count_ == len(self.channels_)
	
	def connect(self):
		"""
		Connects the defined blocks in the flow graph
		Signal Source > Signal conditioner > Channels >> Observables >> PVT > Output filter
		"""
		LOG.INFO("Connecting flowgraph")
		assert not self.connected_
		#ifndef ENABLE_FPGA
		for ss in self.sig_source_:
			if self.configuration_.get(ss.role_ + ".enable_FPGA", False) == False:
				ss.connect(self.top_block_)
		for sc in self.sig_conditioner_:
			if self.configuration_.get(sc.role_ + ".enable_FPGA", False) == False:
				sc.connect(self.top_block_)
		#endif
		for ch in self.channels_:
			ch.connect(self.top_block_)
		self.observables_.connect(self.top_block_)
		self.pvt_.connect(self.top_block_)
		DLOG.INFO("blocks connected internally")
		#ifndef ENABLE_FPGA
		RF_Channels = 0
		signal_conditioner_ID = 0
		for i, ss in enumerate(self.sig_source_):
			if ss.implementation() == "Raw_Array_Signal_Source":
				assert False
			else:
				RF_Channels = self.configuration_.get(ss.role_ + ".RF_channels", 1)
				for j in range(RF_Channels):
					#
					if ss.get_right_block().output_signature()[1] > 1 or ss.get_right_block().output_signature()[1] == -1:
						if len(self.sig_conditioner_) > signal_conditioner_ID:
							LOG.INFO("connecting sig_source_ " + str(i) + " stream " + str(j) + " to conditioner " + str(j))
							self.top_block_.connect(ss.get_right_block(), j, self.sig_conditioner_[signal_conditioner_ID].get_left_block(), 0);
					else:
						assert False
		_ = 2+2
		assert False
				
		
		
		
		
	
	def start(self):
		""
		assert not self.running_
		self.top_block_.start()
		self.running = True

	def set_signals_list(self):
		""
		pass
	
	def set_channels_state(self):
		""
		pass