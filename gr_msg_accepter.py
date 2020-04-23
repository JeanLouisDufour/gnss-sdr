class gr_msg_accepter:
	"""
	runtime/include/gnuradio/msg_accepter.h  inclus et herite de  .../gnuradio/messages/msg_accepter.h
	namespace                                                     namespace gr::messages
	.../gnuradio-runtime/lib/msg_accepter.cc                      .../gnuradio-runtime/lib/messages/msg_accepter.cc (nop)
	
 * \brief Accepts messages and inserts them into a message queue,
 * then notifies subclass gr::basic_block there is a message pending.
	"""
	def post(self,which_port, msg):
		""
		# block* p = dynamic_cast<block*>(this);
		print(type(self))
		self._post(which_port, msg)
	