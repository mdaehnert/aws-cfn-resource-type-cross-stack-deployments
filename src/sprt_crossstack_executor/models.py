# DO NOT modify this file by hand, changes will be overwritten
import sys
from dataclasses import dataclass
from inspect import getmembers, isclass
from typing import (
    AbstractSet,
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

T = TypeVar("T")


def set_or_none(value: Optional[Sequence[T]]) -> Optional[AbstractSet[T]]:
    if value:
        return set(value)
    return None


@dataclass
class ResourceHandlerRequest(BaseResourceHandlerRequest):
    # pylint: disable=invalid-name
    desiredResourceState: Optional["ResourceModel"]
    previousResourceState: Optional["ResourceModel"]


@dataclass
class ResourceModel(BaseModel):
    AccountId: Optional[str]
    Region: Optional[str]
    AssumeRolePath: Optional[str]
    AssumeRoleName: Optional[str]
    CfnStackName: Optional[str]
    CfnCapabilities: Optional[Sequence[str]]
    CfnParameters: Optional[MutableMapping[str, Any]]
    CfnTemplate: Optional[str]
    CfnTemplateUrl: Optional[str]
    CfnStackId: Optional[str]
    CfnStackOutput1: Optional[str]
    CfnStackOutput2: Optional[str]
    CfnStackOutput3: Optional[str]
    CfnStackOutput4: Optional[str]
    CfnStackOutput5: Optional[str]
    CfnStackOutput6: Optional[str]
    CfnStackOutput7: Optional[str]
    CfnStackOutput8: Optional[str]
    CfnStackOutput9: Optional[str]
    LogLevel: Optional[int]

    @classmethod
    def _deserialize(
        cls: Type["_ResourceModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourceModel"]:
        if not json_data:
            return None
        dataclasses = {n: o for n, o in getmembers(sys.modules[__name__]) if isclass(o)}
        recast_object(cls, json_data, dataclasses)
        return cls(
            AccountId=json_data.get("AccountId"),
            Region=json_data.get("Region"),
            AssumeRolePath=json_data.get("AssumeRolePath"),
            AssumeRoleName=json_data.get("AssumeRoleName"),
            CfnStackName=json_data.get("CfnStackName"),
            CfnCapabilities=json_data.get("CfnCapabilities"),
            CfnParameters=json_data.get("CfnParameters"),
            CfnTemplate=json_data.get("CfnTemplate"),
            CfnTemplateUrl=json_data.get("CfnTemplateUrl"),
            CfnStackId=json_data.get("CfnStackId"),
            CfnStackOutput1=json_data.get("CfnStackOutput1"),
            CfnStackOutput2=json_data.get("CfnStackOutput2"),
            CfnStackOutput3=json_data.get("CfnStackOutput3"),
            CfnStackOutput4=json_data.get("CfnStackOutput4"),
            CfnStackOutput5=json_data.get("CfnStackOutput5"),
            CfnStackOutput6=json_data.get("CfnStackOutput6"),
            CfnStackOutput7=json_data.get("CfnStackOutput7"),
            CfnStackOutput8=json_data.get("CfnStackOutput8"),
            CfnStackOutput9=json_data.get("CfnStackOutput9"),
            LogLevel=json_data.get("LogLevel"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


