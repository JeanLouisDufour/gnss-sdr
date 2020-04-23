from gr_basic_block import gr_basic_block

class gr_block(gr_basic_block):
	""
	def __init__(self, name, input_signature, output_signature):
		""
		super().__init__(name, input_signature, output_signature)
		self.d_output_multiple = 1
		self.d_output_multiple_set = False
		self.d_unaligned = 0
		self.d_is_unaligned = False
		self.d_relative_rate = 1.0
		self.d_mp_relative_rate = 1.0
		self.d_history = 1
		self.d_attr_delay = 0
		self.d_fixed_rate = False
		self.d_max_noutput_items_set = False
		self.d_max_noutput_items = 0
		self.d_min_noutput_items = 0
		#self.d_tag_propagation_policy = TPP_ALL_TO_ALL
		self.d_priority = -1
		self.d_pc_rpc_set = False
		self.d_update_rate = False
		#self.d_max_output_buffer(std::max(output_signature->max_streams(), 1), -1)
		#self.d_min_output_buffer(std::max(output_signature->max_streams(), 1), -1)
		#self.d_pmt_done(pmt::intern("done"))
		#self.d_system_port(pmt::intern("system"))
		#
		#global_block_registry.register_primitive(alias(), this);
		#message_port_register_in(d_system_port);
		#set_msg_handler(d_system_port, boost::bind(&block::system_handler, this, _1));
		#
		#configure_default_loggers(d_logger, d_debug_logger, symbol_name());
	
	def set_fixed_rate(self, fixed_rate):
		""
		assert isinstance(fixed_rate, bool)
		self.d_fixed_rate = fixed_rate
	
	def set_output_multiple(self, multiple):
		""
		assert multiple >= 1
		self.d_output_multiple_set = True
		self.d_output_multiple = multiple

	def set_relative_rate(self, relative_rate):
		""
		assert relative_rate > 0
		self.d_relative_rate = relative_rate
		self.d_mp_relative_rate = relative_rate
