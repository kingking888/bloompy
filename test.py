
import unittest
import bitarray

from bloompy3 import BloomFilter,\
    CountingBloomFilter,ScalableBloomFilter,\
    SCBloomFilter,get_filter_fromfile

def is_prime(k):
    if k<=1:
        return False
    for i in range(2,k):
        if k%i==0:
            return False
    return True

class TestBloomFilter(unittest.TestCase):

    def setUp(self):
        self.bf = BloomFilter(0.001,10**3)

    def test_init(self):
        self.assertTrue(isinstance(self.bf.bit_array,bitarray.bitarray))
        self.assertTrue(self.bf.error_rate>0)
        self.assertTrue(all(is_prime(i)for i in self.bf.seeds))
        self.assertTrue(self.bf.bit_array.count() == 0)

    def test_add(self):
        self.assertFalse(self.bf.add(12))
        self.assertFalse(self.bf.add(-12))
        self.assertFalse(self.bf.add(12.0))
        self.assertFalse(self.bf.add('12'))
        self.assertFalse(self.bf.add([12]))
        self.assertFalse(self.bf.add((12,)))
        self.assertFalse(self.bf.add({12:''}))
        self.assertFalse(self.bf.add(b'12'))
        self.assertFalse(self.bf.add(type('12',(),{})))

        self.assertTrue(self.bf.add(12))
        self.assertTrue(self.bf.add(-12))
        self.assertTrue(self.bf.add(12.0))
        self.assertTrue(self.bf.add('12'))
        self.assertTrue(self.bf.add([12]))
        self.assertTrue(self.bf.add((12,)))
        self.assertTrue(self.bf.add({12: ''}))
        self.assertTrue(self.bf.add(b'12'))
        self.assertTrue(self.bf.add(type('12', (), {})))

    def test_exists(self):
        self.bf.add(12)
        self.assertTrue((12 in self.bf))
        self.assertFalse('12' in self.bf)

    def test_tofile(self):
        self.assertFalse(self.bf.tofile(r'test\bf.bf'))

    def test_fromfile(self):
        self.assertTrue(isinstance(self.bf.fromfile(r'test\bf.bf'),BloomFilter))


class TestCountingBloomFilter(unittest.TestCase):

    def setUp(self):
        self.bf = CountingBloomFilter(0.001,10**3)

    def test_init(self):
        self.assertTrue(isinstance(self.bf.bit_array, bitarray.bitarray))
        self.assertTrue(self.bf.error_rate > 0)
        self.assertTrue(all(is_prime(i) for i in self.bf.seeds))
        self.assertTrue(self.bf.bit_array.length()/self.bf._bit_array.length()==4)
        self.assertTrue(self.bf.bit_array.count()==0)

    def test_add(self):
        self.assertFalse(self.bf.add(12))
        self.assertFalse(self.bf.add(-12))
        self.assertFalse(self.bf.add(12.0))
        self.assertFalse(self.bf.add('12'))
        self.assertFalse(self.bf.add([12]))
        self.assertFalse(self.bf.add((12,)))
        self.assertFalse(self.bf.add({12: ''}))
        self.assertFalse(self.bf.add(b'12'))
        self.assertFalse(self.bf.add(type('12', (), {})))

        self.assertTrue(self.bf.add(12))
        self.assertTrue(self.bf.add(-12))
        self.assertTrue(self.bf.add(12.0))
        self.assertTrue(self.bf.add('12'))
        self.assertTrue(self.bf.add([12]))
        self.assertTrue(self.bf.add((12,)))
        self.assertTrue(self.bf.add({12: ''}))
        self.assertTrue(self.bf.add(b'12'))
        self.assertTrue(self.bf.add(type('12', (), {})))

    def test_delete(self):
        self.bf.add(1)
        self.assertTrue(self.bf.bit_array.count()==self.bf.hash_num)
        self.assertTrue(1 in self.bf)
        self.assertTrue(self.bf.delete(1))
        self.assertFalse(self.bf.delete(1))
        self.assertFalse(1 in self.bf)
        self.assertTrue(self.bf.bit_array.count()==0)

    def test_exists(self):
        self.bf.add(12)
        self.assertTrue((12 in self.bf))
        self.assertFalse('12' in self.bf)

    def test_tofile(self):
        for i in range(100):
            self.bf.add(i)
        self.assertFalse(self.bf.tofile(r'test\cbf.bf'))

    def test_fromfile(self):
        self.assertTrue(isinstance(self.bf.fromfile(r'test\cbf.bf'),CountingBloomFilter))


class TestScalableBloomFilter(unittest.TestCase):

    def setUp(self):
        self.bf = ScalableBloomFilter(0.001, 10 ** 3,2)

    def test_add(self):
        for i in range(1100):
             self.assertFalse(self.bf.add(i))
        self.assertTrue(self.bf.filters[0]._at_half_fill())
        self.assertTrue(0 in self.bf)
        self.assertTrue(1101 not in self.bf)
        self.assertTrue(len(self.bf.filters)==2)
        self.assertTrue(self.bf.capacity==3000)
        self.assertTrue(self.bf.filters[0].count<=1000)
        for i in range(1100):
            self.assertTrue(self.bf.add(i))
        self.assertTrue(self.bf.count==1100)

    def test_tofile(self):
        self.assertFalse(self.bf.tofile(r'test\sbf.bf'))

    def test_fromfile(self):
        self.assertTrue(isinstance(self.bf.fromfile(r'test\sbf.bf'),ScalableBloomFilter))

class TestSCBloomFilter(unittest.TestCase):
    def setUp(self):
        self.bf = SCBloomFilter(0.001, 10 ** 3,2)

    def test_add(self):
        for i in range(1100):
             self.assertFalse(self.bf.add(i))
        self.assertTrue(self.bf.filters[0].count==1000)
        self.assertTrue(0 in self.bf)
        self.assertTrue(1101 not in self.bf)
        self.assertTrue(len(self.bf.filters)==2)
        self.assertTrue(self.bf.capacity==3000)
        self.assertTrue(self.bf.filters[0].count<=1000)
        for i in range(1100):
            self.assertTrue(self.bf.add(i))
        self.assertTrue(self.bf.count==1100)

    def test_delete(self):
        for i in range(100):
            self.assertFalse(self.bf.add(i))
        for i in range(100):
            self.assertTrue(i in self.bf)
        for i in range(100):
            self.assertTrue(self.bf.delete(i))
        for i in range(100):
            self.assertFalse(i in self.bf)

    def test_tofile(self):
        for i in range(100):
            self.assertFalse(self.bf.add(i))
        self.assertFalse(self.bf.tofile(r'test\scbf.bf'))

    def test_fromfile(self):
        self.assertTrue(isinstance(self.bf.fromfile(r'test\scbf.bf'),SCBloomFilter))
        a = self.bf.fromfile(r'test\scbf.bf')
        self.assertTrue(a.count==100)
        self.assertTrue(a.capacity==1000)


class TestGetFilterFromfile(unittest.TestCase):

    def test_get_filter_fromfile(self):
        bf = get_filter_fromfile(r'test\bf.bf')
        cbf = get_filter_fromfile(r'test\cbf.bf')
        sbf = get_filter_fromfile(r'test\sbf.bf')
        scbf = get_filter_fromfile(r'test\scbf.bf')

        self.assertTrue(isinstance(bf,BloomFilter))
        self.assertTrue(isinstance(cbf, CountingBloomFilter))
        self.assertTrue(isinstance(sbf, ScalableBloomFilter))
        self.assertTrue(isinstance(scbf, SCBloomFilter))



if __name__ == '__main__':
    unittest.main()