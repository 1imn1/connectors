from typing import Any

import connectors_sdk.models.octi as octi

from .config_loader import ConnectorConfig


class ConverterToStix:
    """Provides methods for converting various types of input data into OpenCTI objects (STIX2.1 compatible)."""

    def __init__(self, config: ConnectorConfig):
        """Create default atuhor and TLP Marking."""
        self.config = config

        self.author = self.create_author()
        self.tlp_marking = self.create_tlp_marking(level=self.config.poc.tlp_level)

    @staticmethod
    def create_author() -> octi.OrganizationAuthor:
        """Create Author.
        :return: OpenCTI Organization as author.
        """
        return octi.OrganizationAuthor(
            name="POC Author",
            description="POC Author description",
        )

    @staticmethod
    def create_tlp_marking(level: str) -> octi.TLPMarking:
        """Create TLP Marking.
        :return: OpenCTI TLPMarking.
        """
        return octi.TLPMarking(level=level)

    def process_on(self, data: Any) -> list[octi.BaseEntity]:
        """Convert external data into OpenCTI objects.
        :param data: Any external data
        :return: OpenCTI objects.
        """
        _ = data  # any data returned by external prodivder's API - discarded for POC

        octi_objects = [self.author, self.tlp_marking]

        intrusion_set = octi.IntrusionSet(
            name="POC IntrusionSet",
            author=self.author,
            markings=[self.tlp_marking],
        )
        sector = octi.Sector(
            name="POC Sector",
            author=self.author,
            markings=[self.tlp_marking],
        )
        country = octi.Country(
            name="France",
            author=self.author,
            markings=[self.tlp_marking],
        )
        octi_objects.extend([intrusion_set, sector, country])

        targets = octi.Targets(
            source=intrusion_set,
            target=country,
            author=self.author,
            markings=[self.tlp_marking],
        )
        # # OR using pipe syntax:
        # targets = intrusion_set | octi.targets | country
        # targets.author = self.author
        # targets.markings = [self.tlp_marking]
        located_at = octi.LocatedAt(
            source=sector,
            target=country,
            author=self.author,
            markings=[self.tlp_marking],
        )
        octi_objects.extend([targets, located_at])

        return octi_objects
