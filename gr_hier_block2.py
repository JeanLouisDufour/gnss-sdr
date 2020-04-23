# inlies hier_block2_detail :
# chaque methode foo se termine par d_detail->foo(...), que l'on inline 

from gr_basic_block import gr_basic_block
from gr_flowgraph import flowgraph

class gr_hier_block2(gr_basic_block):
	""
	def __init__(self, name, input_signature, output_signature):
		""
		super().__init__(name, input_signature, output_signature)
		self.hier_message_ports_in = []
		self.hier_message_ports_out = []
		#### self.d_detail = gr_hier_block2_detail(self)
		# .h
		## d_owner devient self
		self.d_blocks = []
		# .c
		self.d_parent_detail = 0
		self.d_fg = flowgraph()
		min_inputs, max_inputs = input_signature[:2]
		min_outputs, max_outputs = output_signature[:2]
		assert not(max_inputs == -1 or max_outputs == -1 or min_inputs != max_inputs or min_outputs != max_outputs)
		self.d_inputs = [None] * max_inputs # 
		self.d_outputs = [None] * max_outputs
		self.d_max_output_buffer = []
		self.d_min_output_buffer = []
		
	"""
	/*!
     * \brief Add a stand-alone (possibly hierarchical) block to
     * internal graph
     *
     * This adds a gr-block or hierarchical block to the internal
     * graph without wiring it to anything else.
     */
    void connect(basic_block_sptr block);

    /*!
     * \brief Add gr-blocks or hierarchical blocks to internal graph
     * and wire together
     *
     * This adds (if not done earlier by another connect) a pair of
     * gr-blocks or hierarchical blocks to the internal flowgraph, and
     * wires the specified output port to the specified input port.
     */
    void connect(basic_block_sptr src, int src_port, basic_block_sptr dst, int dst_port);
	"""
	def connect(self, block, src_port=-1, dst=None, dst_port=-1):
		""
		assert isinstance(block, gr_basic_block)
		if dst == None: ## premier cas
			assert src_port == dst_port == -1
			#### d_detail->connect(block)
			assert block not in self.d_blocks
			assert block.d_input_signature[1] == 0 and block.d_output_signature[1] == 0
			if isinstance(block, gr_hier_block2) and block != self: ### ???????
				assert block.d_parent_detail == None
				block.d_parent_detail = self
			self.d_blocks.append(block)
		else:
			assert isinstance(dst, gr_basic_block)
			assert src_port >= 0 and dst_port >= 0
			src = block
			#### d_detail->connect(src, src_port, dst, dst_port)
			assert src != dst
			if isinstance(src, gr_hier_block2) and src != self: ### ???????
				assert src.d_parent_detail == None
				src.d_parent_detail = self
			if isinstance(dst, gr_hier_block2) and dst != self: ### ???????
				assert dst.d_parent_detail == None
				dst.d_parent_detail = self
			if src == self:
				assert False
			elif dst == self:
				assert False
			else:
				self.d_fg.connect((src, src_port), (dst, dst_port))

	def message_port_is_hier(self, port_id):
		""
		return self.message_port_is_hier_in(port_id) or self.message_port_is_hier_out(port_id)
	
	def message_port_is_hier_in(self, port_id):
		""
		return port_id in self.hier_message_ports_in
	
	def message_port_is_hier_out(self, port_id):
		""
		return port_id in self.hier_message_ports_out

	def msg_connect(self, src, src_port, dst, dst_port):
		""
		assert isinstance(src, gr_basic_block) and isinstance(dst, gr_basic_block)
		#### d_detail.msg_connect(src, src_port, dst, dst_port)
		if dst not in self.d_blocks:
			self.d_blocks.append(src)
			self.d_blocks.append(dst)
		hier_in = hier_out = False
		if self == src:
			assert False
		elif self == dst:
			assert False
		else:
			hier_out = src.message_port_is_hier_out(src_port)
			hier_in = dst.message_port_is_hier_in(dst_port)
			

###################################################
		
class INH_gr_hier_block2_detail:
	""
	def __init__(self, owner):
		""
		self.d_owner = owner
	
	def msg_connect(self, src, src_port, dst, dst_port):
		""
		pass
