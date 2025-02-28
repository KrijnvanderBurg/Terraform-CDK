"""
Module resource_group

This module defines the ResourceGroupL0 class and the ResourceGroupL0Config class,
which are responsible for creating and managing an Azure resource group with specific configurations.

Classes:
    ResourceGroupL0: A level 0 construct that creates and manages an Azure resource group.
    ResourceGroupL0Config: A configuration class for ResourceGroupL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup

from terraform_cdk.constants import AzureLocation, AzureResource
from terraform_cdk.constructs.ABC import CombinedMeta, ConstructABC, ConstructConfigABC
from terraform_cdk.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
# root key
RESOURCE_GROUP_KEY: Final[str] = "resource_group"
# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"


@dataclass
class ResourceGroupL0Config(ConstructConfigABC):
    """
    A configuration class for ResourceGroupL0.

    Attributes:
        name (str): The name of the resource group.
        location (AzureLocation): The Azure location.
        sequence_number (str): The sequence number.
        management_lock_l0 (ManagementLockL0Config | None): The management lock configuration.
    """

    name: str
    location: AzureLocation
    sequence_number: str

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a ResourceGroupL0Config instance by unpacking parameters from a configuration dictionary.

        The expected format of 'dict_' is:
        {
            "name": "<resource group name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>",
        }

        Args:
            dict_ (dict[str, Any]): A dictionary containing resource group configuration.

        Returns:
            ResourceGroupL0Config: A fully-initialized ResourceGroupL0Config instance.
        """
        name = dict_[NAME_KEY]
        location = AzureLocation.from_full_name(dict_[LOCATION_KEY])
        sequence_number = dict_[SEQUENCE_NUMBER_KEY]

        return cls(
            name=name,
            location=location,
            sequence_number=sequence_number,
        )


class ResourceGroupL0(Construct, ConstructABC, metaclass=CombinedMeta):
    """
    A level 0 construct that creates and manages an Azure resource group.

    Attributes:
        resource_group (ResourceGroup): The Azure resource group.
        management_lock (ManagementLockL0 | None): The management lock applied to the resource group.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: ResourceGroupL0Config,
    ) -> None:
        """
        Initializes the ResourceGroupL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (ResourceGroupL0Config): The configuration for the resource group.
        """
        super().__init__(scope, id_)

        self.full_name = (
            f"{AzureResource.RESOURCE_GROUP.abbr}-{config.name}-{env}-{config.location.abbr}-{config.sequence_number}"
        )

        self._resource_group = ResourceGroup(
            self,
            f"ResourceGroup_{self.full_name}",
            name=self.full_name,
            location=config.location.full_name,
        )

    @property
    def resource_group(self) -> ResourceGroup:
        """Gets the Azure resource group."""
        return self._resource_group
