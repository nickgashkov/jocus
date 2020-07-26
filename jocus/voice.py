import os
from concurrent import futures

executor = futures.ThreadPoolExecutor(max_workers=1)


def say(text: str) -> None:
    executor.submit(os.system, f"say -r 90 -v yuri {text}")
