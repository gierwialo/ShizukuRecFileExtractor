import struct

# FORMAT
# File structure: <header LE><record LE>...<record BE> EOF
# <header LE>: 132 bytes little-endian
# <record LE>: 28 bytes little-endian: <4 x unknown bytes><unsigned int:time_ms><4x unknown bytes><float:vbus><float:ibus><float:data+><float:data->
# Unknown bytes are read as char to _unknown list in each object record for future purpose

class _single_record:
    def __init__(self, unknown1, unknown2, unknown3, unknown4, time_ms, unknown5, unknown6, unknown7, unknown8, vbus, ibus, data_plus, data_minus, dt):
        self._time_ms = time_ms
        self._vbus = vbus
        self._ibus = ibus
        self._data_plus = data_plus
        self._data_minus = data_minus
        self._unknown = [unknown1, unknown2, unknown3, unknown4, unknown5, unknown6, unknown7, unknown8, ]
        self._energy = float(self._vbus * self._ibus * dt)
        self._capacity = float(self._ibus * dt)
        self._dt = dt

    def to_string(self):
        return self.__repr__(fmt='')
    
    def to_csv(self, sep=';'):
        return f'{self._time_ms}{sep}{self._vbus}{sep}{self._ibus}{sep}{self._data_plus}{sep}{self._data_minus}{sep}'
        
    def __repr__(self, fmt='.4f'):
        return f'<timestamp:{self._time_ms} [ms]; V = {self._vbus:{fmt}}[V]; I = {self._ibus:{fmt}}[A]; D+ = {self._data_plus:{fmt}}[V]; D- = {self._data_minus:{fmt}}[V];>'

class get_record:
    def __init__(self, fd, delta_time=1/3600):
        self._fd = fd
        self._dt = delta_time
        self._curr_idx = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        raw = self._fd.read(28)
        if raw:
            return _single_record(*struct.unpack("<ccccIccccffff", raw), self._dt)
        raise StopIteration

class reader:
    def __init__ (self, filename):
        if not filename.endswith('.ShizukuRec'):
            raise RuntimeError('Filename does not contain .ShizukuRec extension')
        
        self._fd = open(filename, mode='rb')
        self._fd.seek(132)
    
    def __enter__(self):
        return self._fd
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._fd.close()