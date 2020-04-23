from gr_sync_block import gr_sync_block

class Gnss_Sdr_Valve(gr_sync_block):
	""
	def __init__(self, sizeof_stream_item, nitems, queue, stop_flowgraph=True):
		""
		super().__init__("valve", (1, 20, sizeof_stream_item), (1, 20, sizeof_stream_item))
	
