from gnss_block_interface import GNSSBlockInterface
from gps_l1_ca_telemetry_decoder_gs import gps_l1_ca_telemetry_decoder_gs

class TelemetryDecoderInterface(GNSSBlockInterface):
	""
	pass

class GpsL1CaTelemetryDecoder(TelemetryDecoderInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		#.h
		self.satellite_ = None
		# .cc
		default_dump_filename = "./navigation.dat"
		self.dump_ = configuration.get(role + ".dump", False)
		self.telemetry_decoder_ = gps_l1_ca_telemetry_decoder_gs(self.satellite_, self.dump_)  #? // TODO fix me
	
	def connect(self, top_block):
		""
		pass # // Nothing to connect internally

	def get_left_block(self):
		""
		return self.telemetry_decoder_
	
	def set_channel(self, channel):
		""
		self.telemetry_decoder_.set_channel(channel)
		
	