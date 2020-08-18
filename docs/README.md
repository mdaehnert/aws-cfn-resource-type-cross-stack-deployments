# SPRT::CrossStack::Executor

Resource schema for cross-account and cross-region stack deployments.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "SPRT::CrossStack::Executor",
    "Properties" : {
        "<a href="#accountid" title="AccountId">AccountId</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: SPRT::CrossStack::Executor
Properties:
    <a href="#accountid" title="AccountId">AccountId</a>: <i>String</i>
</pre>

## Properties

#### AccountId

_Required_: Yes

_Type_: String

_Pattern_: <code>[0-9]{12}</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the AccountId.
