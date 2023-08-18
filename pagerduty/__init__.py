from kubiya import ActionStore
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


logger.info("Loading PagerDuty action store")
action_store = ActionStore("pagerduty", "0.1.0")

action_store.uses_secrets(["PAGERDUTY_API_URL", "PAGERDUTY_API_TOKEN"])

logger.info("Connecting to PagerDuty API")
logger.info("Connected to PagerDuty API")
