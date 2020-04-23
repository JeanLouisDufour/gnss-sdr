#from channel import ChannelFsm
from dll_pll_veml_tracking import dll_pll_veml_tracking
from gnss_block_interface import GNSSBlockInterface
import DLOG

class TrackingInterface(GNSSBlockInterface):
	""
	pass

class GpsL1CaDllPllTracking(TrackingInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		trk_param = {} # Dll_Pll_Conf()
		default_item_type = "gr_complex"
		item_type = configuration.get(role + ".item_type", default_item_type)
		
		if item_type == "gr_complex":
			self.item_size_ = 8
			self.tracking_ = dll_pll_veml_tracking(trk_param)
		else:
			assert False
	
	def connect(self, top_block):
		""
		pass # // nothing to connect, now the tracking uses gr_sync_decimator
	
	def get_right_block(self):
		""
		return self.tracking_

	def set_channel(self, channel):
		""
		assert isinstance(channel, int)
		self.channel_ = channel
		self.tracking_.set_channel(channel)
		
	def set_gnss_synchro(self, gnss_synchro):
		""
		assert gnss_synchro[''] == 'Gnss_Synchro'
		self.tracking_.set_gnss_synchro(gnss_synchro)