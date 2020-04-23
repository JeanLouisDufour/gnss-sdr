from gr_msg_accepter import gr_msg_accepter

class gr_basic_block(gr_msg_accepter):
	"""
	TRES BIZARRE :
		msg_accepter.post invoke (dynamiquement) basic_bloc._post
	"""
	WHITE, GREY, BLACK = range(3)
	s_next_id = 0
	s_ncurrently_allocated = 0
	
	def __init__(self, name, input_signature, output_signature):
		""
		# .h
		self.d_msg_handlers = {} # fun
		self.msg_queue_ready = {} # &boost::condition_variable
		self.mutex = None
		self.msg_queue = {} # msg_queue_t == std::deque<pmt::pmt_t>
		# .cc
		self.d_name = name
		self.d_input_signature = input_signature
		self.d_output_signature = output_signature
		self.d_unique_id = gr_basic_block.s_next_id
		gr_basic_block.s_next_id += 1
		self.d_color = gr_basic_block.WHITE
		self.d_rpc_set = False
		self.d_message_subscribers = {}
		gr_basic_block.s_ncurrently_allocated += 1
	
	def message_port_register_in(self,port_id):
		""
		assert isinstance(port_id, str)
		self.msg_queue[port_id] = []
		self.msg_queue_ready[port_id] = [False] # new boost::condition_variable()
	
	def message_port_register_out(self, port_id):
		""
		assert isinstance(port_id, str)
		assert port_id not in self.d_message_subscribers
		self.d_message_subscribers[port_id] = None
	
	def message_port_is_hier(self, port_id):
		""
		return False
	
	def message_port_is_hier_in(self, port_id):
		""
		return False
	
	def message_port_is_hier_out(self, port_id):
		""
		return False
	
	def name(self):
		""
		return self.d_name
	
	def output_signature(self):
		""
		return self.d_output_signature
	
	def set_msg_handler(self, which_port, msg_handler):
		""
		self.d_msg_handlers[which_port] = msg_handler
	
	def unique_id(self):
		""
		return self.d_unique_id
	