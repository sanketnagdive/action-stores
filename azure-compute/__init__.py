from kubiya import ActionStore
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("Loading Azure Compute action store")
action_store = ActionStore("azure-compute", "0.1.0")

action_store.uses_secrets(["AZURE_CLIENT_SECRET", "AZURE_CLIENT_ID", "AZURE_TENANT_ID"])

logger.info("Connected to Azure Compute API")