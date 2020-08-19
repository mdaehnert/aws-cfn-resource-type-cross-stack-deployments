# SPRT::CrossStack::Executor

Resource schema for cross-account and cross-region stack deployments.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "SPRT::CrossStack::Executor",
    "Properties" : {
        "<a href="#accountid" title="AccountId">AccountId</a>" : <i>String</i>,
        "<a href="#region" title="Region">Region</a>" : <i>String</i>,
        "<a href="#assumerolepath" title="AssumeRolePath">AssumeRolePath</a>" : <i>String</i>,
        "<a href="#assumerolename" title="AssumeRoleName">AssumeRoleName</a>" : <i>String</i>,
        "<a href="#cfnstackname" title="CfnStackName">CfnStackName</a>" : <i>String</i>,
        "<a href="#cfncapabilities" title="CfnCapabilities">CfnCapabilities</a>" : <i>[ String, ... ]</i>,
        "<a href="#cfntemplate" title="CfnTemplate">CfnTemplate</a>" : <i>Map</i>,
        "<a href="#tags" title="Tags">Tags</a>" : <i>[ <a href="tag.md">Tag</a>, ... ]</i>,
        "<a href="#loglevel" title="LogLevel">LogLevel</a>" : <i>Integer</i>
    }
}
</pre>

### YAML

<pre>
Type: SPRT::CrossStack::Executor
Properties:
    <a href="#accountid" title="AccountId">AccountId</a>: <i>String</i>
    <a href="#region" title="Region">Region</a>: <i>String</i>
    <a href="#assumerolepath" title="AssumeRolePath">AssumeRolePath</a>: <i>String</i>
    <a href="#assumerolename" title="AssumeRoleName">AssumeRoleName</a>: <i>String</i>
    <a href="#cfnstackname" title="CfnStackName">CfnStackName</a>: <i>String</i>
    <a href="#cfncapabilities" title="CfnCapabilities">CfnCapabilities</a>: <i>
      - String</i>
    <a href="#cfntemplate" title="CfnTemplate">CfnTemplate</a>: <i>Map</i>
    <a href="#tags" title="Tags">Tags</a>: <i>
      - <a href="tag.md">Tag</a></i>
    <a href="#loglevel" title="LogLevel">LogLevel</a>: <i>Integer</i>
</pre>

## Properties

#### AccountId

_Required_: Yes

_Type_: String

_Pattern_: <code>^[0-9]{12}$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Region

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-z]+-[a-z]-[0-9]+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### AssumeRolePath

_Required_: No

_Type_: String

_Pattern_: <code>^/.*/$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### AssumeRoleName

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CfnStackName

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### CfnCapabilities

Set the capability permissions for execution. Can be left out or contains one or more of the following Capabilities: https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStack.html#API_CreateStack_RequestParameters

_Required_: No

_Type_: List of String

_Allowed Values_: <code>CAPABILITY_IAM</code> | <code>CAPABILITY_NAMED_IAM</code> | <code>CAPABILITY_AUTO_EXPAND</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### CfnTemplate

_Required_: Yes

_Type_: Map

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Tags

_Required_: No

_Type_: List of <a href="tag.md">Tag</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### LogLevel

Set the log level for execution. Can be one of Python's integer log values: https://docs.python.org/3/library/logging.html#logging-levels

_Required_: No

_Type_: Integer

_Allowed Values_: <code>0</code> | <code>10</code> | <code>20</code> | <code>30</code> | <code>40</code> | <code>50</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the CrossStackId.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### CfnStackId

Returns the <code>CfnStackId</code> value.

