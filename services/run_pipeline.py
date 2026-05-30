from datetime import datetime
from datetime import timezone
import os

import logging
from ingest import do_ingest
from transform import do_transform


logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG, filename='logs/pipeline.log', filemode='a')

start = datetime.now(timezone.utc)
logger.info(f"Starting pipeline run: {start}")

logger.info(f"Ingesting")
result = do_ingest()

logger.info(f"Transforming")
result = do_transform()

end = datetime.now(timezone.utc)
logger.info(f"Pipeline run end: {end}")
