from run_pipeline import run

from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
import logging

logger = logging.getLogger(__file__)

def generate_deadlines(start: datetime, step: timedelta):
    delta = step
    while True:
        yield start + delta
        delta += step


def run_on_schedule():
    now = datetime.now(timezone.utc)
    target = now.replace(hour=2,minute=0,second=0,microsecond=0)
    step = timedelta(days=1)
    deadlines = generate_deadlines(target, step)
    retries = 3

    # run once when starting, then once for each deadline
    for attempt in range(1,1+retries):
        ok = run()
        if ok:
            break
        else:
            logger.info(f'{attempt=} failed, retrying...')


    for deadline in deadlines:
        now = datetime.now(timezone.utc)
        to_sleep = (deadline - now).total_seconds()
        if to_sleep < 0:
            logger.info(f'missed last {deadline=}, skipping')
        else:
            logger.info(f'sleeping until {deadline=}')
            time.sleep(to_sleep)
        for attempt in range(1,1+retries):
            ok = run()
            if ok:
                break
            else:
                logger.info(f'{attempt=} failed, retrying...')


if __name__ == '__main__':
    run_on_schedule()
