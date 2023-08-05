import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_codepipeline_api
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codecommit", "0.27.0", __name__, "aws-codecommit@0.27.0.jsii.tgz")
class CfnRepository(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codecommit.CfnRepository"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, repository_name: str, repository_description: typing.Optional[str]=None, triggers: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["RepositoryTriggerProperty", aws_cdk.cdk.Token]]]]=None) -> None:
        props: CfnRepositoryProps = {"repositoryName": repository_name}

        if repository_description is not None:
            props["repositoryDescription"] = repository_description

        if triggers is not None:
            props["triggers"] = triggers

        jsii.create(CfnRepository, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRepositoryProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> str:
        return jsii.get(self, "repositoryId")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.CfnRepository.RepositoryTriggerProperty")
    class RepositoryTriggerProperty(jsii.compat.TypedDict, total=False):
        branches: typing.List[str]
        customData: str
        destinationArn: str
        events: typing.List[str]
        name: str


class _CfnRepositoryProps(jsii.compat.TypedDict, total=False):
    repositoryDescription: str
    triggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", aws_cdk.cdk.Token]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.CfnRepositoryProps")
class CfnRepositoryProps(_CfnRepositoryProps):
    repositoryName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.CommonPipelineSourceActionProps")
class CommonPipelineSourceActionProps(aws_cdk.aws_codepipeline_api.CommonActionProps, jsii.compat.TypedDict, total=False):
    branch: str
    outputArtifactName: str
    pollForSourceChanges: bool

@jsii.interface(jsii_type="@aws-cdk/aws-codecommit.IRepository")
class IRepository(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        ...

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, branch: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="toCodePipelineSourceAction")
    def to_code_pipeline_source_action(self, *, branch: typing.Optional[str]=None, output_artifact_name: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> "PipelineSourceAction":
        ...


class _IRepositoryProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codecommit.IRepository"
    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnCommit", [name, target, options])

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnPullRequest", [name, target, options])

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, branch: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        return jsii.invoke(self, "onCommit", [name, target, branch])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onEvent", [name, target, options])

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onPullRequestStateChange", [name, target, options])

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceCreated", [name, target, options])

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceDeleted", [name, target, options])

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceUpdated", [name, target, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @jsii.member(jsii_name="toCodePipelineSourceAction")
    def to_code_pipeline_source_action(self, *, branch: typing.Optional[str]=None, output_artifact_name: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> "PipelineSourceAction":
        props: CommonPipelineSourceActionProps = {"actionName": action_name}

        if branch is not None:
            props["branch"] = branch

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        if run_order is not None:
            props["runOrder"] = run_order

        return jsii.invoke(self, "toCodePipelineSourceAction", [props])


class PipelineSourceAction(aws_cdk.aws_codepipeline_api.SourceAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codecommit.PipelineSourceAction"):
    def __init__(self, *, repository: "IRepository", branch: typing.Optional[str]=None, output_artifact_name: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: PipelineSourceActionProps = {"repository": repository, "actionName": action_name}

        if branch is not None:
            props["branch"] = branch

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(PipelineSourceAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, stage: aws_cdk.aws_codepipeline_api.IStage, _scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [stage, _scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.PipelineSourceActionProps")
class PipelineSourceActionProps(CommonPipelineSourceActionProps, jsii.compat.TypedDict):
    repository: "IRepository"

@jsii.implements(IRepository)
class RepositoryBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codecommit.RepositoryBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _RepositoryBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(RepositoryBase, self, [scope, id])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "RepositoryImportProps":
        ...

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnCommit", [name, target, options])

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnPullRequest", [name, target, options])

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, branch: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        return jsii.invoke(self, "onCommit", [name, target, branch])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onEvent", [name, target, options])

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onPullRequestStateChange", [name, target, options])

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceCreated", [name, target, options])

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceDeleted", [name, target, options])

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceUpdated", [name, target, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @jsii.member(jsii_name="toCodePipelineSourceAction")
    def to_code_pipeline_source_action(self, *, branch: typing.Optional[str]=None, output_artifact_name: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> "PipelineSourceAction":
        props: CommonPipelineSourceActionProps = {"actionName": action_name}

        if branch is not None:
            props["branch"] = branch

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        if run_order is not None:
            props["runOrder"] = run_order

        return jsii.invoke(self, "toCodePipelineSourceAction", [props])

    @property
    @jsii.member(jsii_name="repositoryArn")
    @abc.abstractmethod
    def repository_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    @abc.abstractmethod
    def repository_clone_url_http(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    @abc.abstractmethod
    def repository_clone_url_ssh(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> str:
        ...


class _RepositoryBaseProxy(RepositoryBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")


class Repository(RepositoryBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codecommit.Repository"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, repository_name: str, description: typing.Optional[str]=None) -> None:
        props: RepositoryProps = {"repositoryName": repository_name}

        if description is not None:
            props["description"] = description

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, repository_name: str) -> "IRepository":
        props: RepositoryImportProps = {"repositoryName": repository_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="notify")
    def notify(self, arn: str, *, branches: typing.Optional[typing.List[str]]=None, custom_data: typing.Optional[str]=None, events: typing.Optional[typing.List["RepositoryEventTrigger"]]=None, name: typing.Optional[str]=None) -> "Repository":
        options: RepositoryTriggerOptions = {}

        if branches is not None:
            options["branches"] = branches

        if custom_data is not None:
            options["customData"] = custom_data

        if events is not None:
            options["events"] = events

        if name is not None:
            options["name"] = name

        return jsii.invoke(self, "notify", [arn, options])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        return jsii.get(self, "repositoryName")


@jsii.enum(jsii_type="@aws-cdk/aws-codecommit.RepositoryEventTrigger")
class RepositoryEventTrigger(enum.Enum):
    All = "All"
    UpdateRef = "UpdateRef"
    CreateRef = "CreateRef"
    DeleteRef = "DeleteRef"

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.RepositoryImportProps")
class RepositoryImportProps(jsii.compat.TypedDict):
    repositoryName: str

class _RepositoryProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.RepositoryProps")
class RepositoryProps(_RepositoryProps):
    repositoryName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.RepositoryTriggerOptions")
class RepositoryTriggerOptions(jsii.compat.TypedDict, total=False):
    branches: typing.List[str]
    customData: str
    events: typing.List["RepositoryEventTrigger"]
    name: str

__all__ = ["CfnRepository", "CfnRepositoryProps", "CommonPipelineSourceActionProps", "IRepository", "PipelineSourceAction", "PipelineSourceActionProps", "Repository", "RepositoryBase", "RepositoryEventTrigger", "RepositoryImportProps", "RepositoryProps", "RepositoryTriggerOptions", "__jsii_assembly__"]

publication.publish()
