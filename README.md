# pydcontest
一款python编写的milvus并发搜索工具，使用了2种方式进行实现。

==风险提示==:

==进程设置过多可能会导致系统无法ssh登录。==



`conn_search_collection_Process`:

for循环创建并启动进程。



`conn_search_collection_ProcessPool`:

使用进程池提交任务。



`conn_search_collection_Thread`:

for循环创建并启动线程。



`conn_search_collection_ThreadPool`:

使用线程池提交任务。



python的多线程并不是真正的多线程，不能利用多核cpu的优势。

由于存在`全局解释器锁(Global Interpreter Lock)`，同一时刻只有一个线程可以执行 Python 代码（虽然某些性能导向的库可能会去除此限制）。 如果你想让你的应用更好地利用多核CPU，推荐你使用 multiprocessing 或 concurrent.futures.ProcessPoolExecutor。 但是，如果你想要同时运行多个 I/O 密集型任务，则多线程仍然是一个合适的模型。



# milvus性能测试:

一些心得:

+ 关于milvus的并发、QPS、时延

  这三者是一个相互制约的关系，并发高则时延高、并发低则时延低。

  并发:同一时刻发送的请求。

  QPS:一秒钟处理的请求。

+ milvus有一个合并请求的功能

  `queryNode.grouping.maxNQ`默认为1000。

  这个参数和QPS也是一个相互制约的关系，设置的大QPS就小，设置的小QPS就大。

+ milvus的并发能力并不高

+ python不适合做高并发性能测试、可以使用golang

+ 官方的性能测试数据不能全信、需要自己实践得出数据

