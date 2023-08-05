from libc.string cimport memset

def memzero(x):
	memset(<char*> x, 0, len(x))

