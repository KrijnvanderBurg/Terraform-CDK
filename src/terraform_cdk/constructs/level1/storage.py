"""
Module storage_account_locked_l1

This module defines the StorageL1 class and the StorageL1Config class,
which are responsible for creating and managing an Azure storage account with a management lock using level 0
    constructs.

Classes:
    StorageL1: A level 1 construct that creates and manages an Azure storage account with a management
                            lock.
    StorageL1Config: A configuration class for StorageL1.
"""

from dataclasses import dataclass, field
from typing import Any, Final, Self

from terraform_cdk.constructs.ABC import CombinedMeta
from terraform_cdk.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from terraform_cdk.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from terraform_cdk.constructs.level0.storage_container import StorageContainerL0, StorageContainerL0Config
from constructs import Construct

# Constants for dictionary keys
# root key
STORAGE_L1_KEY: Final[str] = "storage"
# attributes
STORAGE_ACCOUNT_L0_KEY: Final[str] = "storage_account"
STORAGE_CONTAINERS_L0_KEY: Final[str] = "containers"


@dataclass
class StorageL1Config(StorageAccountL0Config):
    """
    A configuration class for StorageL1, inheriting from StorageAccountL0Config and adding containers.

    Attributes:
        containers (list[StorageContainerL0Config]): The configuration for the storage containers.
    """

    containers: list[StorageContainerL0Config] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a StorageL1Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            StorageL1Config: A fully-initialized StorageL1Config.
        """
        config = super().from_dict(dict_)
        containers = [StorageContainerL0Config.from_dict(container) for container in dict_.get("containers", [])]

        return cls(
            sequence_number=config.sequence_number,
            account_replication_type=config.account_replication_type,
            account_tier=config.account_tier,
            location=config.location,
            name=config.name,
            access_tier=config.access_tier,
            account_kind=config.account_kind,
            blob_properties_l0=config.blob_properties_l0,
            cross_tenant_replication_enabled=config.cross_tenant_replication_enabled,
            infrastructure_encryption_enabled=config.infrastructure_encryption_enabled,
            is_hns_enabled=config.is_hns_enabled,
            local_user_enabled=config.local_user_enabled,
            nfsv3_enabled=config.nfsv3_enabled,
            public_network_access_enabled=config.public_network_access_enabled,
            sftp_enabled=config.sftp_enabled,
            shared_access_key_enabled=config.shared_access_key_enabled,
            tags=config.tags,
            containers=containers,
        )


class StorageL1(Construct, metaclass=CombinedMeta):
    """
    A level 1 construct that creates and manages an Azure storage account with a management lock and storage containers.

    Attributes:
        storage_account (StorageAccountL0): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
        storage_containers (list[StorageContainerL0]): The Azure storage containers.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: StorageL1Config,
        resource_group_name: str,
    ) -> None:
        """
        Initializes the StorageL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StorageL1Config): The configuration for the storage account and containers.
            resource_group_name (str): The name of the resource group to create the storage account in.
        """
        super().__init__(scope, id_)

        self._storage_account: StorageAccountL0 = StorageAccountL0(
            self,
            "StorageAccountL0",
            env=env,
            config=config,
            resource_group_name=resource_group_name,
        )

        self._management_lock: ManagementLockL0 = ManagementLockL0(
            self,
            "ManagementLockL0",
            _=env,
            config=ManagementLockL0Config(lock_level="CanNotDelete"),
            resource_id=self._storage_account.storage_account.id,
            resource_name=config.name,
        )

        self._storage_containers: list[StorageContainerL0] = [
            StorageContainerL0(
                self,
                f"StorageContainerL0_{container_config.name}",
                _=env,
                config=container_config,
                storage_account_id=self._storage_account.storage_account.id,
            )
            for container_config in config.containers
        ]

    @property
    def storage_account(self) -> StorageAccountL0:
        """Gets the storage account."""
        return self._storage_account

    @property
    def management_lock(self) -> ManagementLockL0:
        """Gets the management lock."""
        return self._management_lock

    @property
    def storage_containers(self) -> list[StorageContainerL0]:
        """Gets the storage containers."""
        return self._storage_containers
