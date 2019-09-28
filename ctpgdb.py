import gdb

gdb.execute('file osce')
g = gdb.execute('run', to_string=True)
print(g)
#o = gdb.execute('info r', to_string=True)
#print(o)
d = gdb.execute('x/5s $sp', to_string=True)
print(d)
gdb.execute('quit')

