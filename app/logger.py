import logging


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s  - %(levelname)s - %(message)s",
                    #      handlers=[logging.FileHandler("access.log"), logging.StreamHandler()]
                    )

logging.getLogger("watchfiles.main").disabled = True

access_logger = logging.getLogger("AccessLogger")
