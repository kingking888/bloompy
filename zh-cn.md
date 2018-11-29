# bloompy

布隆过滤器的Python3实现，包括标准、计数、标准扩容、计数扩容。更新自pybloom。

## 安装

> pip install bloompy

## 使用

通过bloompy你可以使用四种布隆过滤器
* **标准布隆过滤器**

标准布隆过滤器只能进行数据的查询和插入，是下面几种过滤器的基类，可以进行过滤器的存储和恢复
```python
>>> import bloompy
>>> bf = bloompy.BloomFilter(error_rate=0.001,element_num=10**3)

# 查询元素是否在过滤器里返回状态标识
# 如果不在里面则插入，返回False表示元素不在过滤器里
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

# 将过滤器存储在一个文件里
>>> bf.tofile('filename.suffix')

# 从一个文件里恢复过滤器。自动识别过滤器的种类。
>>> recovered_bf = bloompy.get_filter_fromfile('filename.suffix')

# 或者使用过滤器类的类方法 'fromfile' 来进行过滤器的复原。对应的类只能恢复对应的过滤器
>>> recovered_bf = bloompy.BloomFilter.fromfile('filename.suffix')

# 返回已经插入的元素个数
>>> bf.count
2

# 过滤器的容量
>>> bf.capacity
1000

# 过滤器的位向量
>>> bf.bit_array
bitarray('00....')

# 过滤器位数组长度
>>> bf.bit_num
14400

# 过滤器的哈希种子，默认是素数，可修改
>>> bf.seeds
[2, 3, 5, 7, 11,...]

# 过滤器哈希函数个数
>>> bf.hash_num
10

```
* **计数布隆过滤器**

标准布隆过滤器的子类，但是计数布隆过滤器可以执行**删除**元素额操作。内置默认使用4位二进制位来表示标准布隆过滤器的1个位，从而实现可以增减。
```python
>>> import  bloompy
>>> cbf  = bloompy.CountingBloomFilter(error_rate=0.001,element_num=10**3)

# 与标准布隆过滤器一样
>>> cbf.add(12)
False
>>> cbf.add(12)
True
>>> 12 in cbf
True
>>> cbf.count
1

# 查询元素状态返回标识，如果元素存在过滤器里则删除
>>> cbf.delete(12)
True
>>> cbf.delete(12)
False
>>> 12 in cbf
False
>>> cbf.count
0

# 从文件中恢复过滤器
>>> recovered_cbf = bloompy.CountingBloomFilter.fromfile('filename.suffix')
```
计数布隆过滤器其他的功能与标准的差不多。


* **标准扩容布隆过滤器**

当插入的元素个数超过当前过滤器的容量时，自动增加过滤器的容量，默认内置一次扩容2倍。支持查询和插入功能。
```python
>>> import bloompy
>>> sbf = bloompy.ScalableBloomFilter(error_rate=0.001,initial_capacity=10**3)

# 默认初次可以设置容量1000
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

#当过滤器的元素个数达到容量极限时，过滤器会自动增加内置的标准过滤器，
#每次增加2倍容量，自动实现扩容
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

# 从文件中恢复过滤器
>>> recovered_sbf = bloompy.ScalableBloomFilter.fromfile('filename.suffix')
```
其他功能可以参见标准布隆过滤器。

* **计数扩容布隆过滤器**

标准扩容布隆过滤器的子类，功能继承自标准扩容布隆过滤器，但支持**删除**元素的操作。
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

# 插入元素使其达到过滤器当前容量极限值
>>> for i in range(1100):
        scbf.add(i)
>>> len(scbf)
2
>>> scbf.filters
[<bloompy.CountingBloomFilter object at 0x000000000B6F5828>, <bloompy.CountingBloomFilter object at 0x000000000B6F5898>]

# 从文件中恢复过滤器
>>> recovered_scbf = bloompy.SCBloomFilter.fromfile('filename.suffix')
```
## 存储与恢复

参见标准布隆过滤器，可以通过两种方式来进行过滤器的存储与复原：
- **类方法'fromfile'**
- **函数get_filter_fromfile() **

> 如果你很清楚的知道当前文件中的过滤器是一个标准布隆过滤器，那么你可以使类方法类恢复这个过滤器:
> 
> ``` bloompy.BloomeFilter.fromfile('filename.suffix) ```
> 
> 如果是个计数布隆过滤器，那么就是使用:
> 
> ```bloompy.CountingBloomFilter.fromfile('filename.suffix)```
>
> 其他也是使用对应的类方法来恢复对应的过滤器。 
> 
> 但如果你不知道文件里存储是哪种过滤器，可以使用函数:
> 
> ```bloompy.get_filter_fromfile('filename.suffix') ```
> 
> 它将会加载文件字节数据，自动判断过滤器类型并返回对应实例进行复原。