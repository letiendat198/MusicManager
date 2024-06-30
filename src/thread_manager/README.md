# ThreadManger overview

## Methods
1. add_task(): Create a Worker (QObject) and add it to worker_queue with an id
2. start_task(id): Do the follow things:
   
   - Check if threadpool size exceed max_thread_count. If yes then push worker to thread_queue
   - If threadpool still have space:
     - Init a new QThread
     - Move worker to said thread
     - thread.started signal connect to worker.run slot
     - thread.finished signal connect to clean-up method on_thread_finished()
     - worker.info_signal.finished connect to thread.quit slot (Because thread won't end
     even if worker has returned. Therefore, thread need to be killed)
3. cancel_task(id): Cancel a thread if found in threadpool. Otherwise, pop it from thread_queue
4. start_queued_thread(): To be called once a thread finishes to start a queued thread
5. get_worker_signal(id): Return info_signal of worker with said id
6. on_thread_finished(id): Clean up thread, pop it from threadpool then start a queued thread
7. set_max_thread_count(int): Set max_thread_count to allow more thread in threadpool

## Notes
- There should only be **ONE** instance of ThreadManager running. Call get_manager_instance() to get
the current instance
- ThreadManager should be inited in the main file. Just need to import ThreadManager and leave it

## Questions I may ask myself later:
- Q: Why don't you just use QRunnable and QThreadpool?
  - A: Cause QRunnable have no event loop, so it won't receive any signal. Therefore, you can't
  cancel it.
- Q: Why not override QThread run():
  - A: That would overwrite the call to exec(), thus no event loop
- Q: Why this README?
  - A: Cause I may forget why I implement this in the first place. Also, someone may need to
  use this later (probably me)
  - A: Also because I thought this would be confusing to look at later. Turns out it is quite
  straightforward. But I already make this README so.... too late

