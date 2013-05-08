
starbase_data.so : starbase_data.c
	gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing       \
                -I$(ROOT)/include/python2.7                                     \
                -o starbase_data.so starbase_data.c


starbase_data.c : starbase_data.py starbase_data.pxd
	cython starbase_data.py

