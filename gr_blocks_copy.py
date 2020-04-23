""" copy.h :
 * \brief output[i] = input[i]
 * \ingroup misc_blk
 *
 * \details
 * When enabled (default), this block copies its input to its
 * output. When disabled, this block drops its input on the floor.
 *
 * Message Ports:
 *
 * - en (input):
 *      Receives a PMT bool message to either enable to disable
 *      copy.
"""

from gr_block import gr_block

class gr_blocks_copy(gr_block):
	"copy.h -> copy_impl.h -> copy_impl.c"
	def __init__(self, itemsize):
		""
		super().__init__("copy", (1, -1, itemsize), (1, -1, itemsize))
		self.d_itemsize = itemsize
		self.d_enabled = True
		self.message_port_register_in("en");
		self.set_msg_handler("en", self.handle_enable) # boost::bind(&copy_impl::handle_enable, this, _1)
	
	def handle_enable(self,msg):
		""
		if isinstance(msg, bool):
			self.d_enabled = msg
	
	def set_enabled(self, enable):
		""
		self.d_enabled = enable
		
	def enabled(self):
		""
		return self.d_enabled
	
	####### impl ############"
	
	