from gr_block import gr_block

class dll_pll_veml_tracking(gr_block):
	""
	def __init__(self, conf):
		""
		#                                  sizeof(gr_complex) sizeof(Gnss_Synchro)
		super().__init__("dll_pll_veml_tracking", (1, 1, 8), (1, 1, 8))

	def set_channel(self, channel):
		""
		assert isinstance(channel, int)
		self.d_channel = channel
		
	def set_gnss_synchro(self, gnss_synchro):
		""
		assert gnss_synchro[''] == 'Gnss_Synchro'
		self.d_acquisition_gnss_synchro = gnss_synchro