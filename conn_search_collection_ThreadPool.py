from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
import random
import time
import multiprocessing as mp
from pymilvus import (
  connections,
  Collection,
)

dim = 512
host = "192.168.230.71"
port = "19530"
username = ""
password = ""
collectionName = "hello_milvus"
concurrencyNum = 10

#################################################################################

def search(lock: mp.Lock, q: mp.Queue, cond: mp.Condition):
    # 由于milvus的连接设计缺陷,创建连接只能放在进程里面,不能集中创建连接再使用,涉及到进程空间共享内存问题
    # 多线程是可以,但是python的多线程并不是真正的多线程
    connections.connect(
        user=username,
        password=password,
        host=host,
        port=port
    )
    coll = Collection(name=collectionName)
    search_param = {
    "metric_type": "L2",
    "params": {"ef": 200}
    }
    search_data = [random.random() for _ in range(dim)]
    q.put(1)
    with cond:
        cond.wait()
    #当前时间
    start = time.perf_counter()
    results = coll.search(
        data=[search_data], 
        anns_field="embeddings",
        param=search_param,
        limit=3,
        expr=None,
        output_fields=['book_id'],
        # consistency_level="Strong"
        consistency_level="Eventually"
    )
    #结束时间
    end = time.perf_counter()
    with lock:
        print("search latency:",end - start)

    # print(results)


if __name__ == '__main__':
    with mp.Manager() as m:
        lock,q, cond = m.Lock(), m.Queue(), m.Condition()
        with ThreadPoolExecutor(max_workers=concurrencyNum) as executor:
            print(f"Start search in concurrency {concurrencyNum}")
            future_iter = [executor.submit(search, lock, q, cond) for i in range(concurrencyNum)]
            # 等待所有进程
            while q.qsize() < concurrencyNum:
                time.sleep(0.1)

            with cond:
                start = time.perf_counter()
                cond.notify_all()
                print(f"Syncing all process and start concurrency search, concurrency={concurrencyNum}")
        end = time.perf_counter()
        # 总时间并不准确,包含了资源回收的时间
        print("total search latency:", end - start)