from channel_msg_receiver_cc import channel_msg_receiver_cc
import DLOG

class ChannelFsm:
	""
	pass

class ChannelInterface:
	""
	pass

class Channel(ChannelInterface):
	""
	def __init__(self, configuration, channel, acq, trk, nav, role, implementation, queue):
		""
		#.h
		self.repeat_ = None
		#.cc
		self.acq_ = acq;
		self.trk_ = trk
		self.nav_ = nav
		self.role_ = role
		self.implementation_ = implementation
		self.channel_ = channel
		self.queue_ = queue
		self.channel_fsm_ = ChannelFsm()

		self.flag_enable_fpga = configuration.get("GNSS-SDR.enable_FPGA", False)
		assert self.flag_enable_fpga == False # JLD

		self.acq_.set_channel(self.channel_)
		self.acq_.set_channel_fsm(self.channel_fsm_)
		self.trk_.set_channel(self.channel_)
		self.nav_.set_channel(self.channel_)

		self.gnss_synchro_ = {'':'Gnss_Synchro'} # Gnss_Synchro()
		self.gnss_synchro_['Channel_ID'] = self.channel_
		self.acq_.set_gnss_synchro(self.gnss_synchro_)
		self.trk_.set_gnss_synchro(self.gnss_synchro_)
		
		_ = 2+2
		
		self.channel_msg_rx = channel_msg_receiver_cc(self.channel_fsm_, self.repeat_)
		
		print('TBC')
		
	def connect(self, top_block):
		""
		if not self.flag_enable_fpga:
			self.acq_.connect(top_block)
		self.trk_.connect(top_block)
		self.nav_.connect(top_block)

		# Synchronous ports
		top_block.connect(self.trk_.get_right_block(), 0, self.nav_.get_left_block(), 0)

		# Message ports
		top_block.msg_connect(self.nav_.get_left_block(), "telemetry_to_trk", self.trk_.get_right_block(), "telemetry_to_trk")
		DLOG.INFO("tracking -> telemetry_decoder")

		# Message ports
		if not self.flag_enable_fpga:
			top_block.msg_connect(self.acq_.get_right_block(), "events", self.channel_msg_rx, "events")
		top_block.msg_connect(self.trk_.get_right_block(), "events", self.channel_msg_rx, "events")

		self.connected_ = True
