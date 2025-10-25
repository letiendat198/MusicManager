import unittest
from time import sleep

import src.thread_manager.ThreadManager as ThreadManager

def task(i, progress_callback):
    start_text = "Test {} starting".format(i)
    print(start_text)
    sleep(1)
    end_text = "Test {} ending".format(i)
    print(end_text)
    return i

class TestThreading(unittest.TestCase):
    def setUp(self):
        self.thread_manager = ThreadManager.get_manager_instance()
        self.thread_count = 0
        self.test_count = 2

    def test_thread_queue(self):
        for i in range(1,self.test_count):
            task_id = self.thread_manager.add_task(task, i)
            worker_signal = self.thread_manager.get_worker_signal(task_id)
            worker_signal.result.connect(self.on_thread_return)
            self.thread_manager.start_task(task_id)
        self.assertEqual(len(self.thread_manager.thread_queue), self.test_count - 12)

    def on_thread_return(self, i):
        print("Test {} returned".format(i))
        self.thread_count += 1

    def test_thread_return(self):
        sleep(5)
        self.assertEqual(self.thread_count, self.test_count)



if __name__ == '__main__':
    unittest.main()