import numpy as np

class gr_fft_complex:
	""
	def __init__(self, fft_size, forward = True, nthreads = 1):
		""
		self.d_forward = forward
		self.d_inbuf = np.zeros(fft_size, dtype=np.complex64)
		self.d_outbuf = np.zeros(fft_size, dtype=np.complex64)
	
	def execute(self):
		""
		assert False