import concurrent.futures


# --- THREAD POOL --------------------------------------------------------------
thread_pool = concurrent.futures \
    .ThreadPoolExecutor(max_workers=4)