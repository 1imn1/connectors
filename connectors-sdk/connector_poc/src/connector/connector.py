import sys

import connectors_sdk.models.octi as octi
from pycti import (
    OpenCTIConnectorHelper,  # type: ignore[import-untyped]  # pycti does not provide stubs
)

from .config_loader import ConnectorConfig
from .converter_to_stix import ConverterToStix


class ConnectorPOC:
    """Define connector behavior."""

    def __init__(self, config: ConnectorConfig):
        """Init and register connector onto OpenCTI."""
        self.config = config
        self.helper = OpenCTIConnectorHelper(config=config.model_dump_pycti())
        self.converter = ConverterToStix(config=self.config)

        self.work_id = None

    def _collect_intelligence(self) -> list[octi.BaseEntity]:
        """Create OpenCTI entities from external provider's data.
        :return: List of OCTI objects.
        """
        data = ...  # any data returned by external data prodiver's API

        return self.converter.process_on(data)

    def process(self) -> None:
        """Connector main process to collect intelligence."""
        self.helper.connector_logger.info(
            "[CONNECTOR] Running connector...",
            {"connector_name": self.helper.connect_name},
        )

        try:
            octi_objects = self._collect_intelligence()
            if octi_objects:
                self.work_id = self.helper.api.work.initiate_work(
                    connector_id=self.helper.connector_id,
                    friendly_name="Connector SDK POC",
                )

                stix_objects = [
                    otci_object.to_stix2_object() for otci_object in octi_objects
                ]
                stix_objects_bundle = self.helper.stix2_create_bundle(stix_objects)
                bundles_sent = self.helper.send_stix2_bundle(
                    stix_objects_bundle,
                    work_id=self.work_id,
                    cleanup_inconsistent_bundle=True,
                )

                self.helper.connector_logger.info(
                    "Sending STIX objects to OpenCTI...",
                    {"bundles_sent": {str(len(bundles_sent))}},
                )

                message = f"{self.helper.connect_name} connector successfully run"
                self.helper.api.work.to_processed(self.work_id, message)
                self.helper.connector_logger.info(message)
                self.work_id = None

        except (KeyboardInterrupt, SystemExit):
            self.helper.connector_logger.info(
                "[CONNECTOR] Connector stopped...",
                {"connector_name": self.helper.connect_name},
            )
            sys.exit(0)
        except Exception as err:
            self.helper.connector_logger.error(str(err))
        finally:
            # Close any pending work in case of errors
            if self.work_id:
                self.helper.api.work.to_processed(self.work_id, "Connector stopped")

    def run(self) -> None:
        """Run the main process encapsulated in a scheduler.
        It allows you to schedule the process to run at a certain intervals
        This specific scheduler from the pycti connector helper will also check the queue size of a connector
        If `CONNECTOR_QUEUE_THRESHOLD` is set, if the connector's queue size exceeds the queue threshold,
        the connector's main process will not run until the queue is ingested and reduced sufficiently,
        allowing it to restart during the next scheduler check. (default is 500MB)
        It requires the `duration_period` connector variable in ISO-8601 standard format
        Example: `CONNECTOR_DURATION_PERIOD=PT5M` => Will run the process every 5 minutes.
        """
        self.helper.schedule_process(
            message_callback=self.process,
            duration_period=self.config.connector.duration_period.total_seconds(),
        )
