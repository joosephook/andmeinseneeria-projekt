from datetime import datetime
from datetime import timezone
import sys

import logging
from ingest import do_ingest
from transform import do_transform
import traceback

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler('logs/pipeline.log'),logging.StreamHandler(sys.stdout)] )

def run():
    try:
        start = datetime.now(timezone.utc)
        logger.info(f"Starting pipeline run: {start}")

        logger.info(f"Ingesting")
        ok = do_ingest()
        if not ok:
            logger.info("Ingestion failed, skipping rest of the pipeline")
            end = datetime.now(timezone.utc)
            logger.info(f"Pipeline run interrupted: {end}")
            return False

        logger.info(f"Transforming")
        ok = do_transform()
        if not ok:
            logger.info("Transformation failed, skipping rest of the pipeline")
            end = datetime.now(timezone.utc)
            logger.info(f"Pipeline run interrupted: {end}")
            return False

        end = datetime.now(timezone.utc)
        logger.info(f"Pipeline run end: {end}")
    except Exception as error:
        logger.error(f"Error occurred in pipeline: {''.join(traceback.format_exception(error))}")
        return False
    return True

if __name__ == '__main__':
    run()
