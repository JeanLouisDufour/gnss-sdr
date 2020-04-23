from channel import Channel
from direct_resampler_conditioner import DirectResamplerConditioner
from file_signal_source import FileSignalSource
from gps_l1_ca_dll_pll_tracking import GpsL1CaDllPllTracking
from gps_l1_ca_pcps_acquisition import GpsL1CaPcpsAcquisition
from gps_l1_ca_telemetry_decoder import GpsL1CaTelemetryDecoder
from hybrid_observables import HybridObservables
import in_memory_configuration
from ishort_to_complex import IshortToComplex
from pass_through import Pass_Through
from rtklib_pvt import Rtklib_Pvt
from signal_conditioner import SignalConditioner
import LOG
import jld_channels

class GNSSBlockFactory():
	""
	def __init__(self):
		""
		pass
	
	def GetSignalSource(self, configuration, queue, ID):
		"return GNSSBlockInterface"
		default_implementation = "File_Signal_Source"
		role = "SignalSource"
		assert ID == -1
		implementation = configuration.get(role + ".implementation", default_implementation)
		LOG.INFO("Getting SignalSource with implementation " + implementation)
		return self.GetBlock(configuration, role, implementation, 0, 1, queue)
	
	def GetSignalConditioner(self,configuration, ID = -1):
		"returns GNSSBlockInterface"
		default_implementation = "Pass_Through"
		role_conditioner = "SignalConditioner"
		role_datatypeadapter = "DataTypeAdapter"
		role_inputfilter = "InputFilter"
		role_resampler = "Resampler"
		assert ID == -1
		signal_conditioner = configuration.get(role_conditioner + ".implementation", default_implementation)
		if signal_conditioner == "Pass_Through":
			data_type_adapter = "Pass_Through"
			input_filter = "Pass_Through"
			resampler = "Pass_Through"
		else:
			data_type_adapter = configuration.get(role_datatypeadapter + ".implementation", default_implementation)
			input_filter = configuration.get(role_inputfilter + ".implementation", default_implementation)
			resampler = configuration.get(role_resampler + ".implementation", default_implementation)

		LOG.INFO("Getting SignalConditioner with DataTypeAdapter implementation: " \
              + data_type_adapter + ", InputFilter implementation: " \
              + input_filter + ", and Resampler implementation: " \
              + resampler)

		if signal_conditioner == "Array_Signal_Conditioner":
			# instantiate the array version
			assert False
		else:
			# single-antenna version
			c = SignalConditioner(configuration,
				self.GetBlock(configuration, role_datatypeadapter, data_type_adapter, 1, 1),
				self.GetBlock(configuration, role_inputfilter, input_filter, 1, 1),
				self.GetBlock(configuration, role_resampler, resampler, 1, 1),
				role_conditioner, "Signal_Conditioner")
		return c

	def GetChannel_1C(self, configuration, acq, trk, tlm, channel, queue):
		""
		aux = configuration.get("Acquisition_1C" + str(channel) + ".implementation", "W")
		appendix1 = str(channel) if aux != "W" else ""
		aux = configuration.get("Tracking_1C" + str(channel) + ".implementation", "W")
		appendix2 = str(channel) if aux != "W" else ""
		aux = configuration.get("TelemetryDecoder_1C" + str(channel) + ".implementation", "W")
		appendix3 = str(channel) if aux != "W" else ""
		#
		default_item_type = "gr_complex"
		acq_item_type = configuration.get("Acquisition_1C" + appendix1 + ".item_type", default_item_type)
		trk_item_type = configuration.get("Tracking_1C" + appendix2 + ".item_type", default_item_type)
		assert acq_item_type == trk_item_type
		in_memory_configuration.d["Channel.item_type"] = acq_item_type
		self.acq_ = self.GetAcqBlock(configuration, "Acquisition_1C" + appendix1, acq, 1, 0)
		self.trk_ = self.GetTrkBlock(configuration, "Tracking_1C" + appendix2, trk, 1, 1)
		self.tlm_ = self.GetTlmBlock(configuration, "TelemetryDecoder_1C" + appendix3, tlm, 1, 1)
		self.channel_ = Channel(configuration, channel, self.acq_, self.trk_, self.tlm_, "Channel", "1C", queue)
		return self.channel_

	def GetChannels(self, configuration, queue):
		""
		default_implementation = "Pass_Through"
		channel_absolute_id = 0
		Channels_xx_count = {k:configuration.get("Channels_{}.count".format(k), 0) for k in jld_channels.cid}
		total_channels = sum(Channels_xx_count.values())
		channels = [None] * total_channels # vector GNSSBlockInterface
		#
		LOG.INFO("Getting " + str(Channels_xx_count['1C']) + " GPS L1 C/A channels")
		acquisition_implementation = configuration.get("Acquisition_1C.implementation", default_implementation)
		tracking_implementation = configuration.get("Tracking_1C.implementation", default_implementation)
		telemetry_decoder_implementation = configuration.get("TelemetryDecoder_1C.implementation", default_implementation)
		for i in range(Channels_xx_count['1C']):
			acquisition_implementation_specific = configuration.get(
                        "Acquisition_1C" + str(channel_absolute_id) + ".implementation",
                        acquisition_implementation)
			tracking_implementation_specific = configuration.get(
                        "Tracking_1C" + str(channel_absolute_id) + ".implementation",
                        tracking_implementation)
			telemetry_decoder_implementation_specific = configuration.get(
                        "TelemetryDecoder_1C" + str(channel_absolute_id) + ".implementation",
                        telemetry_decoder_implementation)
			channels[channel_absolute_id] = self.GetChannel_1C(configuration,
                        acquisition_implementation_specific,
                        tracking_implementation_specific,
                        telemetry_decoder_implementation_specific,
                        channel_absolute_id,
                        queue)
			channel_absolute_id += 1
		return channels
		
	def GetObservables(self, configuration):
		""
		default_implementation = "Hybrid_Observables"
		implementation = configuration.get("Observables.implementation", default_implementation)
		LOG.INFO("Getting Observables with implementation " + implementation)
		Galileo_channels = configuration.get("Channels_1B.count", 0)
		Galileo_channels += configuration.get("Channels_5X.count", 0)
		GPS_channels = configuration.get("Channels_1C.count", 0)
		GPS_channels += configuration.get("Channels_2S.count", 0)
		GPS_channels += configuration.get("Channels_L5.count", 0)
		Glonass_channels = configuration.get("Channels_1G.count", 0)
		Glonass_channels += configuration.get("Channels_2G.count", 0)
		Beidou_channels = configuration.get("Channels_B1.count", 0)
		Beidou_channels += configuration.get("Channels_B3.count", 0)
		extra_channels = 1  # For monitor channel sample counter
		return self.GetBlock(configuration, "Observables", implementation,
        Galileo_channels +
            GPS_channels +
            Glonass_channels +
            Beidou_channels +
            extra_channels,
        Galileo_channels +
            GPS_channels +
            Glonass_channels +
            Beidou_channels)
	
	def GetPVT(self, configuration):
		""
		default_implementation = "RTKLIB_PVT"
		implementation = configuration.get("PVT.implementation", default_implementation)
		LOG.INFO("Getting PVT with implementation " + implementation)
		Galileo_channels = configuration.get("Channels_1B.count", 0)
		Galileo_channels += configuration.get("Channels_5X.count", 0)
		GPS_channels = configuration.get("Channels_1C.count", 0)
		GPS_channels += configuration.get("Channels_2S.count", 0)
		GPS_channels += configuration.get("Channels_L5.count", 0)
		Glonass_channels = configuration.get("Channels_1G.count", 0)
		Glonass_channels += configuration.get("Channels_2G.count", 0)
		Beidou_channels = configuration.get("Channels_B1.count", 0)
		Beidou_channels += configuration.get("Channels_B3.count", 0)
		return self.GetBlock(configuration, "PVT", implementation,
				        Galileo_channels + GPS_channels + Glonass_channels + Beidou_channels, 0)
	
	def GetBlock(self, configuration, role, implementation, in_streams, out_streams, queue = None):
		""
		if implementation == "Pass_Through":
			block = Pass_Through(configuration, role, in_streams, out_streams)
		elif implementation == "File_Signal_Source":
			block = FileSignalSource(configuration, role, in_streams, out_streams, queue)
		elif implementation == "Ishort_To_Complex":
			block = IshortToComplex(configuration, role, in_streams, out_streams)
		elif implementation == "Direct_Resampler":
			block = DirectResamplerConditioner(configuration, role, in_streams, out_streams)
		elif implementation in ("Hybrid_Observables", "GPS_L1_CA_Observables", "GPS_L2C_Observables", "Galileo_E5A_Observables"):
			block = HybridObservables(configuration, role, in_streams, out_streams)
		elif implementation in ("RTKLIB_PVT", "GPS_L1_CA_PVT", "Galileo_E1_PVT", "Hybrid_PVT"):
			block = Rtklib_Pvt(configuration, role, in_streams, out_streams)
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		elif implementation == "":
			assert False
		else:
			assert False, implementation
		return block

	######## private #######
	
	def GetChannel_xx(self, kind, configuration, acq, trk, tlm, channel, queue):
		"xx = kind = 1C/2S/..."
		assert False
		
	def GetAcqBlock(self, configuration, role, implementation, in_streams, out_streams):
		""
		if implementation == "GPS_L1_CA_PCPS_Acquisition":
			block = GpsL1CaPcpsAcquisition(configuration, role, in_streams, out_streams)
		elif implementation == "":
			assert False
		else:
			assert False
		return block
		
	def GetTrkBlock(self, configuration, role, implementation, in_streams, out_streams):
		""
		if implementation == "GPS_L1_CA_DLL_PLL_Tracking":
			block = GpsL1CaDllPllTracking(configuration, role, in_streams, out_streams)
		elif implementation == "":
			assert False
		else:
			assert False
		return block
		
	def GetTlmBlock(self, configuration, role, implementation, in_streams, out_streams):
		""
		if implementation == "GPS_L1_CA_Telemetry_Decoder":
			block = GpsL1CaTelemetryDecoder(configuration, role, in_streams, out_streams)
		elif implementation == "":
			assert False
		else:
			assert False
		return block
