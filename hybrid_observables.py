from gnss_block_interface import GNSSBlockInterface
from hybrid_observables_gs import hybrid_observables_gs
import DLOG

class ObservablesInterface(GNSSBlockInterface):
	""
	pass

class HybridObservables(ObservablesInterface):
	""
	def __init__(self, configuration, role, in_streams, out_streams):
		""
		# .h
		self.dump_ = \
		self.dump_filename_ = \
		self.dump_mat_ = \
		self.in_streams_ = \
		self.observables_ = \
		self.out_streams_ = \
		self.role_ = None
		# .cc
		self.role_ = role
		self.in_streams_ = in_streams
		self.out_streams_ = out_streams
		default_dump_filename = "./observables.dat"
		DLOG.INFO("role " + role)
		self.dump_ = configuration.get(role + ".dump", False)
		self.dump_mat_ = configuration.get(role + ".dump_mat", True)
		self.dump_filename_ = configuration.get(role + ".dump_filename", default_dump_filename)
		self.observables_ = hybrid_observables_gs(self.in_streams_, self.out_streams_, self.dump_, self.dump_mat_, self.dump_filename_)
		
	def connect(self, top_block):
		""
		pass # // Nothing to connect internally