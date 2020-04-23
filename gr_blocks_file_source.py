from gr_sync_block import gr_sync_block
import os, stat
import numpy as np

class gr_blocks_file_source(gr_sync_block):
	""
	ol = [] # JLD
	# make
	def __init__(self, itemsize, filename, repeat=False, offset=0, length=0):
		""
		super().__init__("file_source", (0,0,0), (1,1,itemsize))
		self.d_itemsize = itemsize
		self.d_start_offset_items = offset
		self.d_length_items = length
		self.d_fp = 0
		self.d_new_fp = 0
		self.d_repeat = repeat
		self.d_updated = False
		self.d_file_begin = True
		self.d_repeat_cnt = 0
		self.d_add_begin_tag = None # pmt::PMT_NIL
		#
		self.open(filename, repeat, offset, length);
		self.do_update();
		self._id = self.name() + str(self.unique_id())
		# .h
		self.d_seekable = None
		self.d_items_remaining = None
		# JLD
		gr_blocks_file_source.ol.append(self)

	def seek(self, seek_point, whence):
		"""
		seek sur d_fp
		seek_point est 1) en items 2) en relatif p.r. start_offset
		"""
		assert self.d_seekable
		seek_point += self.d_start_offset_items
		if whence == os.SEEK_SET:
			pass
		elif whence == os.SEEK_CUR:
			seek_point += (self.d_length_items - self.d_items_remaining)
		elif whence == os.SEEK_END:
			seek_point = self.d_length_items - seek_point
		else:
			assert False, whence
		assert seek_point >= self.d_start_offset_items \
			and seek_point < self.d_start_offset_items + self.d_length_items
		# Return the new cursor position in bytes, starting from the beginning
		r = os.lseek(self.d_fp, seek_point * self.d_itemsize, os.SEEK_SET)
		return r == seek_point * self.d_itemsize

	def open(self, filename, repeat, offset_items=0, length_items=0):
		""
		if self.d_new_fp > 2:
			os.close(self.d_new_fp)
			self.d_new_fp = 0
		assert self.d_new_fp == 0
		self.d_new_fp = os.open(filename, os.O_RDONLY | os.O_BINARY)
		assert self.d_new_fp > 2
		self.py_stat_ = os.fstat(self.d_new_fp)
		self.d_seekable = stat.S_ISREG(self.py_stat_.st_mode)
		if self.d_seekable:
			file_size = os.lseek(self.d_new_fp, 0, os.SEEK_END)
			assert file_size == self.py_stat_.st_size # 1600000000
			items_available, fs_mod = divmod(file_size, self.d_itemsize)
			assert fs_mod == 0
		else:
			file_size = np.iinfo(np.int64).max
			items_available, fs_mod = divmod(file_size, self.d_itemsize)
			file_size -= fs_mod
		assert items_available > offset_items
		items_available -= offset_items
		if length_items == 0:
			length_items = items_available
		assert length_items <= items_available
		if self.d_seekable:
			r = os.lseek(self.d_new_fp, offset_items * self.d_itemsize, os.SEEK_SET)
			assert r == offset_items * self.d_itemsize
		self.d_updated = True;
		self.d_repeat = repeat;
		self.d_start_offset_items = offset_items;
		self.d_length_items = length_items;
		self.d_items_remaining = length_items
	
	def close(self):
		""
		assert False
	
	def do_update(self):
		""
		if self.d_updated:
			if self.d_fp != 0:
				os.close(self.d_fp)
			self.d_fp = self.d_new_fp
			self.d_new_fp = 0
			self.d_updated = False
			self.d_file_begin = True
