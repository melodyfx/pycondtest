# pydcontest
一款python编写的milvus并发搜索工具，使用了2种方式进行实现。

==风险提示==:

==进程设置过多可能会导致系统无法ssh登录。==



`conn_search_collection_Process`:

for循环创建并启动进程。



`conn_search_collection_ProcessPool`:

使用进程池提交任务。
