# [bloompy](https://pypi.org/project/bloompy/)

An implementation of 4 kinds of Bloom Filter in Python3.[中文](https://github.com/01ly/bloompy/blob/master/zh-cn.md)
> bloompy includes the standard BloomFilter,CountingBloomFilter,ScalableBloomFilter,ScalableCountingBloomFilter.
> It's Update from pybloom.

## Installation

> pip install bloompy

## Use

There's 4 kinds of BloomFilter you can use by bloompy.
* **standard bloom filter**

the standard one can only query or add elements in it. 
```python
>>> import bloompy
>>> bf = bloompy.BloomFilter(error_rate=0.001,element_num=10**3)

# query the status of the element inside the bf immediately 
# and add it into the bf.False returned indicates the element
# does not inside the filter.
>>> bf.add(1) 
False
>>> bf.add(1)
True
>>> 1 in bf
True
>>> bf.exists(1)
True
>>> bf.add([1,2,3])
False
>>> bf.add([1,2,3])
True
>>> [1,2,3] in bf
True
>>> bf.exists([1,2,3])
True

# store the bf into a file.
>>> bf.tofile('filename.suffix')

# recover a bf from a file.Auto recognize which kind of filters it is.
>>> recovered_bf = bloompy.get_filter_fromfile('filename.suffix')

# or you can use a classmethod 'fromfile' of the BloomFilter Class to get
# a BloomFilter instance from a file.Same as other kind of filter Classes .
>>> recovered_bf = bloompy.BloomFilter.fromfile('filename.suffix')

# return the total number of the elements inside the bf.
>>> bf.count
2

# the capacity of the current filter.
>>> bf.capacity
1000

# the bits array of the current filter. 
>>> bf.bit_array
bitarray('00....')

# the total length of the bitarray.
>>> bf.bit_num
14400

# the hash seeds inside the filter.
# they are prime numbers by default.It's modifiable.
>>> bf.seeds
[2, 3, 5, 7, 11,...]

# the amount of hash functions 
>>> bf.hash_num
10

```
* **counting bloom filter**

The counting bloom filter is a subclass of the standard bloom filter.But it supports the **delete** operation.
It is set inside that 4bits represent a **bit** of the standard bf. So it costs more momery than the standard bf,
it's 4 times the standard one.
```python
>>> import  bloompy
>>> cbf  = bloompy.CountingBloomFilter(error_rate=0.001,element_num=10**3)

# same as the standard bf at add operation.
>>> cbf.add(12)
False
>>> cbf.add(12)
True
>>> 12 in cbf
True
>>> cbf.count
1

# query the status of the element inside the cbf immediately 
# if the element inside the cbf,delete it.
>>> cbf.delete(12)
True
>>> cbf.delete(12)
False
>>> 12 in cbf
False
>>> cbf.count
0

# recover a cbf from a file.Same as the bf.
>>> recovered_cbf = bloompy.CountingBloomFilter.fromfile('filename.suffix')
```
You can do any operations of the BloomFilter on it as well. 


* **scalable bloom filter**

Auto increase the capacity of the filter if the current amount of inserted elements is up to the limits.
It's set 2times the pre capacity inside by default.
```python
>>> import bloompy
>>> sbf = bloompy.ScalableBloomFilter(error_rate=0.001,initial_capacity=10**3)

# at first, the sbf is at 1000 capacity limits.
>>> len(sbf)
0
>>> 12 in sbf
False
>>> sbf.add(12)
False
>>> 12 in sbf 
True
>>> len(sbf)
1
>>> sbf.filters
[<bloompy.BloomFilter object at 0x000000000B6F5860>]
>>> sbf.capacity
1000

# when the amount of inserting elements surpass the limits 1000.
# the sbf appends a new filter inside it which capacity 2times 1000.
>>> for i in range(1000):
        sbf.add(i)
>>> 600 in sbf
True
>>> len(sbf)
2
>>> sbf.filters
[<bloompy.BloomFilter object at 0x000000000B6F5860>, <bloompy.BloomFilter object at 0x000000000B32F748>]
>>> sbf.capacity
3000

# recover a sbf from a file.Same as bf.
>>> recovered_sbf = bloompy.ScalableBloomFilter.fromfile('filename.suffix')
```
You can do any operations of the BloomFilter on it as well. 

* **scalable counting bloom filter**

It's a subclass of the ScalableBloomFilter.But it supports the **delete** operation.
You can do any operations of the ScalableBloomFilter on it as well. 
```python
>>> import bloompy
>>> scbf = bloompy.SCBloomFilter(error_rate=0.001,initial_capacity=10**3)

>>> scbf.add(1)
False
>>> 1 in scbf
True
>>> scbf.delete(1)
True
>>> 1 in scbf
False
>>> len(scbf)
1
>>> scbf.filters
[<bloompy.CountingBloomFilter object at 0x000000000B6F5828>]

# add elements in sbf to make it at a capacity limits
>>> for i in range(1100):
        scbf.add(i)
>>> len(scbf)
2
>>> scbf.filters
[<bloompy.CountingBloomFilter object at 0x000000000B6F5828>, <bloompy.CountingBloomFilter object at 0x000000000B6F5898>]

# recover a scbf from a file.Same as bf.
>>> recovered_scbf = bloompy.SCBloomFilter.fromfile('filename.suffix')
```
## Store and recover

As shown in the standard bloom filter.You can store a filter in 2 ways:
- classmethod 'fromfile'
- get_filter_fromfile() 

> if you do clearly know that there is a BloomFilter stored in a file.
> you can recover it with:
> 
> ``` bloompy.BloomeFilter.fromfile('filename.suffix) ```
> 
> or it's a CountingBloomFilter inside it:
> 
> ```bloompy.CountingBloomFilter.fromfile('filename.suffix)```
>
> Same as others. 
> 
> But if you don't know what kind of filter it is stored in the file.Use:
> 
> ```bloompy.get_filter_fromfile('filename.suffix') ```
> 
> It will auto recognize the filter stored inside a file.Then you can do something with it.
