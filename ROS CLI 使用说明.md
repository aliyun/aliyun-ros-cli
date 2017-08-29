# ROS CLI 介绍

[TOC]

## 默认配置

初次使用`ros`命令时会在`ros`的安装路径下创建默认配置文件`ros/ros.conf`：

```
[ACCESS]
ACCESS_KEY_ID = YOUR_KEY_ID
ACCESS_KEY_SECRET = YOUR_KEY_SECRET
REGION_ID = YOUR_REGION

[OTHER]
JSON_INDENT = 2
DEBUG = False
```

## 自动补全支持

目前提供对`bash`环境的命令参数自动补全：

* 将`ros-cli/resources/ros_completion`放置于`/etc/bash_completion.d/`目录下
* `source /etc/bash_completion.d/ros_completion`

## 使用说明

### ROS

安装 `ros-cli `后，输入 `ros` 使用本工具。

`ros` 本身支持如下参数：

| 命令                        | 功能                                       |
| ------------------------- | ---------------------------------------- |
| `-h` `--help`             | 查看帮助信息                                   |
| `--config [CONFIG_FILE]`  | 使用指定配置文件，如果没有指定，默认使用当前目录下的 `ros/ros.conf` 作为配置文件 |
| `--json`                  | 以`json`格式输出查询信息，否则以阅读格式输出                |
| `--region-id [REGION_ID]` | 指定区域信息，否则使用配置文件中的区域信息                    |

`json` 格式的输出按照配置文件中的 `JSON_INDENT` 设置缩进。

`ros` 支持如下一级命令：

| 命令                       | 功能            |
| ------------------------ | ------------- |
| `set-userdata`           | 设置默认配置        |
| `create-stack`           | 创建堆栈          |
| `delete-stack`           | 删除堆栈          |
| `update-stack`           | 更新堆栈          |
| `preview-stack`          | 预览堆栈          |
| `abandon-stack`          | 废弃堆栈（开发中）     |
| `list-stacks`            | 列出满足条件的堆栈     |
| `describe-stack`         | 列出指定堆栈的详细信息   |
| `list-resource`          | 列出指定堆栈的资源信息   |
| `describe-resource`      | 列出指定资源的详细信息   |
| `resource-type`          | 列出所有资源类型      |
| `resource-type-detail`   | 列出指定资源类型的详细信息 |
| `resource-type-template` | 列出指定资源类型的模板信息 |
| `get-template`           | 列出指定堆栈的模板信息   |
| `validate-template`      | 验证模板信息        |
| `list-regions`           | 列出所有区域        |
| `list-events`            | 列出满足条件的事件信息   |

### 堆栈相关

#### Create Stack

使用 `ros create-stack` 命令创建堆栈，包含如下参数：

| 命令                                       | 功能          | 备注                                       |
| ---------------------------------------- | ----------- | ---------------------------------------- |
| `--region-id`                            | 指定堆栈所在区域    | `region-id` 将按如下优先级取用：`当前命令指定值 > ros 命令指定值 > 配置文件指定值 ` |
| `--stack-name [STACK_NAME]`              | 指定创建堆栈的名称   | 必须给出                                     |
| `--template-url [TEMPLATE_URL]`          | 指定创建堆栈的模板文件 | 必须给出，模板文件内容为 `json` 格式的模板                |
| `--parameters [PARAMETERS]`              | 给出模板需要的参数   | 与模板中的参数匹配，否则会被服务器拒绝。格式为连续的字符串，形如`key1=value1,key2=value2` |
| `--disable-rollback [DISABLE_ROLLBACK]`  | 指定回滚策略      | 默认 `true` 禁止回滚，                          |
| `--timeout-in-minutes [TIMEOUT_IN_MINUTES]` | 指定超时时间      | 默认 `60` （分钟）                             |

创建成功后，返回堆栈名称和ID，否则返回错误信息。

**成功示例**

```
$ ./bin/ros create-stack --stack-name ros-cli-demo --template-url  PATH\\TO\\template.json --parameters DBUser=demo,InstancePassword=Demo123456,DBPassword=Demo123456,DBRootPassword=Demo123456
Succeed

Id                  :  ***
Name                :  ros-cli-demo
```

**失败示例**

```
$ ./bin/ros create-stack --stack-name ros-cli-demo --template-url  PATH\\TO\\template.json --parameters DBUser=demo,InstancePassword=Demo123456,DBPassword=Demo123456,DBRootPassword=Demo123456
Failed

Message             :  The Stack (ros-cli-demo) already exists.
Code                :  StackExists
```

#### Delete Stack

使用 `ros delete-stack` 命令删除堆栈，包含如下参数：

| 命令                          | 功能       | 备注   |
| --------------------------- | -------- | ---- |
| `--region-id`               | 指定堆栈所在区域 | 必须给出 |
| `--stack-name [STACK_NAME]` | 指定堆栈的名称  | 必须给出 |
| `--stack-id [STACK_ID]`     | 指定堆栈的ID  | 必须给出 |

删除成功后，提示成功，无返回值，否则返回错误信息。

**成功示例**

```
$ ros delete-stack --region-id cn-beijing --stack-name test-6-21 --stack-id ***
Succeed
```

**失败示例**

```
$ ros delete-stack --region-id cn-beijing --stack-name test-6-21-1 --stack-id ***
Failed

Message             :  The Stack (test-6-21-1) could not be found.
Code                :  StackNotFound
```

#### Update Stack

使用 `ros update-stack` 命令更新堆栈，包含如下参数：

| 命令                                       | 功能          | 备注                                       |
| ---------------------------------------- | ----------- | ---------------------------------------- |
| `--region-id`                            | 指定堆栈所在区域    | 必须给出                                     |
| `--stack-name [STACK_NAME]`              | 指定更新堆栈的名称   | 必须给出                                     |
| `--stack-id [STACK_ID]`                  | 指定更新堆栈的ID   | 必须给出                                     |
| `--template-url [TEMPLATE_URL]`          | 指定更新堆栈的模板文件 | 必须给出，模板文件内容为 `json` 格式的模板                |
| `--parameters [PARAMETERS]`              | 给出模板需要的参数   | 与模板中的参数匹配，否则会被服务器拒绝。格式为连续的字符串，形如`key1=value1,key2=value2` |
| `--disable-rollback [DISABLE_ROLLBACK]`  | 指定回滚策略      | 默认 `true` 禁止回滚，                          |
| `--timeout-in-minutes [TIMEOUT_IN_MINUTES]` | 指定超时时间      | 默认 `60` （分钟）                             |

更新成功后，返回堆栈名称和ID，否则返回错误信息。

**成功示例**

```
$ ros update-stack --stack-name ros-cli-demo --template-url  PATH\\TO\\template.json --parameters DBUser=demo,InstancePassword=Demo123456,DBPassword=Demo123456,DBRootPassword=Demo123456 --region-id cn-beijing --stack-id ***
Succeed

Id                  :  ***
Name                :  ros-cli-demo
```

**失败示例**

```
$ ros update-stack --stack-name ros-cli-demo --template-url  PATH\\TO\\template.json --parameters DBUser=demo,InstancePassword=Demo123456,DBPassword=Demo123456,DBRootPassword=Demo123456 --region-id cn-beijing --stack-id ***
Failed

Message             :  Updating a stack when it is in (UPDATE, IN_PROGRESS) is not supported.
Code                :  NotSupported
```

#### Preview Stack

使用 `ros preview-stack` 命令创建堆栈，包含如下参数：

| 命令                                       | 功能          | 备注                                       |
| ---------------------------------------- | ----------- | ---------------------------------------- |
| `--region-id`                            | 指定堆栈所在区域    | `region-id` 将按如下优先级取用：`当前命令指定值 > ros 命令指定值 > 配置文件指定值 ` |
| `--stack-name [STACK_NAME]`              | 指定预览堆栈的名称   | 必须给出                                     |
| `--template-url [TEMPLATE_URL]`          | 指定预览堆栈的模板文件 | 必须给出，模板文件内容为 `json` 格式的模板                |
| `--parameters [PARAMETERS]`              | 给出模板需要的参数   | 与模板中的参数匹配，否则会被服务器拒绝。格式为连续的字符串，形如`key1=value1,key2=value2` |
| `--disable-rollback [DISABLE_ROLLBACK]`  | 指定回滚策略      | 默认 `true` 禁止回滚，                          |
| `--timeout-in-minutes [TIMEOUT_IN_MINUTES]` | 指定超时时间      | 默认 `60` （分钟）                             |

创建成功后，返回资源信息，否则返回错误信息。

**成功示例**

```
$ ros preview-stack --stack-name ros-cli-demo2 --template-url  PATH\\TO\\template.json --parameters DBUser=demo,InstancePassword=Demo123456,DBPassword=Demo123456,DBRootPassword=Demo123456
Id                  :  None
Name                :  ros-cli-demo2
Description         :  Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.
Region              :  cn-beijing
DisableRollback     :  True
TimeoutMins         :  60
Created             :  2017-06-27T06:46:34.231047
Updated             :  None
Webhook             :  None
TemplateDescription :  Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.

Parameters:
    SystemDiskCategory  : ***
    ALIYUN::StackName   : ros-cli-demo2
    ALIYUN::NoValue     : None
    ALIYUN::StackId     : None
    ALIYUN::Region      : cn-beijing
    DBRootPassword      : ******
    ImageId             : ***
    InstancePassword    : ******
    DBPassword          : ******
    DBName              : MyDatabase
    DBUser              : ******
    ALIYUN::AccountId   : ***
    InstanceType        : ***
    NginxUrl            : ***

Resources:

-----------------------------------------------------------------------

Resource:

    StackName           :  None
    ResourceType        :  None
    ResourceName        :  None
    ResourceStatus      :  None
    ResourceStatusReason:  None
    ResourceData        :  None
    Description         :  Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.
    ResourceAction      :  None
    PhysicalResourceId  :  None
    CreatedTime         :  None
    UpdatedTime         :  None
    DeletedTime         :  None

    RequiredBy:
        WebServer
        WebServerWaitCondition

  ...

```

以 `json` 格式输出

```
$ ros --json preview-stack --stack-name ros-cli-demo2 --template-url  PATH\\TO\\template.json --parameters DBUser=demo,InstancePassword=Demo123456,DBPassword=Demo123456,DBRootPassword=Demo123456
{
  "Created": "2017-06-27T06:48:52.893040",
  "Description": "Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.",
  "DisableRollback": true,
  "Id": "None",
  "Name": "ros-cli-demo2",
  "Parameters": {
    "ALIYUN::AccountId": "***",
    "ALIYUN::NoValue": "None",
    "ALIYUN::Region": "cn-beijing",
    "ALIYUN::StackId": "None",
    "ALIYUN::StackName": "ros-cli-demo2",
    "DBName": "MyDatabase",
    "DBPassword": "******",
    "DBRootPassword": "******",
    "DBUser": "******",
    "ImageId": "***",
    "InstancePassword": "******",
    "InstanceType": "***",
    "NginxUrl": "***",
    "SystemDiskCategory": "***"
  },
  "Region": "cn-beijing",
  "Resources": [
    {
      "Attributes": {
        "CurlCli": null
      },
      "CreatedTime": null,
      "DeletedTime": null,
      "Description": "",
      "Metadata": {},
      "PhysicalResourceId": "",
      "Properties": {},
      "RequiredBy": [
        "WebServerWaitCondition",
        "WebServer"
      ],

  ...
}
```

**失败示例**

```
$ ros preview-stack --stack-name ros-cli-demo2 --template-url  PATH\\TO\\template.json --parameters DBUser=demo
Something wrong:
HTTP Status: 400 Error:UserParameterMissing The Parameter (DBRootPassword) was not provided. RequestID: None
```

#### Abandon Stack

使用 `ros abandon-stack` 命令废弃堆栈，包含如下参数：

| 命令                          | 功能       | 备注   |
| --------------------------- | -------- | ---- |
| `--region-id`               | 指定堆栈所在区域 | 必须给出 |
| `--stack-name [STACK_NAME]` | 指定堆栈的名称  | 必须给出 |
| `--stack-id [STACK_ID]`     | 指定堆栈的ID  | 必须给出 |

**失败示例**

```
$ ros abandon-stack --stack-name ros-cli-demo --stack-id *** --region-id cn-beijing
Failed

Message             :  The server could not comply with the request since it is either malformed or otherwise incorrect.
Code                :  HTTPBadRequest
```

#### List Stacks

使用 `ros list-stacks` 命令查看堆栈列表，包含如下参数：

| 命令                                       | 功能       | 备注                  |
| ---------------------------------------- | -------- | ------------------- |
| `--region-id`                            | 指定堆栈所在区域 |                     |
| `--stack-name [STACK_NAME]`              | 指定堆栈的名称  |                     |
| `--stack-id [STACK_ID]`                  | 指定堆栈的ID  |                     |
| `--status {CREATE_COMPLETE, CREATE_FAILED, CREATE_IN_PROGRESS, DELETE_COMPLETE, DELETE_FAILED, DELETE_IN_PROGRESS, ROLLBACK_COMPLETE, ROLLBACK_FAILED, ROLLBACK_IN_PROGRESS}` | 指定堆栈的状态  | 必须使用指定值             |
| `--page-number [PAGE_NUMBER]`            | 输入查看的页码  | 查询结果将分页返回，从1开始，默认为1 |
| `--page-size [PAGE_SIZE]`                | 指定每页显示数量 | 默认为10，不超过100        |

输出当前的翻页情况及结果列表：

**成功示例** 

```
$ ros list-stacks --page-number 2 --page-size 3

Total Records: 8     Page: 2/3

Id                  :  ***
Name                :  test_ros_condition_v1
Description         :  None
Region              :  cn-beijing
Status              :  ROLLBACK_COMPLETE
StatusReason        :  Stack ROLLBACK completed successfully
TimeoutMins         :  60
DisableRollback     :  False
Created             :  2017-06-15T03:08:22
Updated             :  None


Id                  :  ***
Name                :  test_clouder_v1
Description         :  None
Region              :  cn-beijing
Status              :  CREATE_COMPLETE
StatusReason        :  Stack CREATE completed successfully
TimeoutMins         :  60
DisableRollback     :  False
Created             :  2017-06-01T08:19:51
Updated             :  None

...

```

**失败示例**

```
$ ros list-stacks --page-number 2 --page-size 3 --region-id cn-beijing2
Something wrong:
SDK.InvalidRegionId Can not find endpoint to access.
```

#### Describe Stack

使用 `ros describe-stack` 命令获取堆栈详细信息，包含如下参数：

| 命令                          | 功能      | 备注   |
| --------------------------- | ------- | ---- |
| `--stack-name [STACK_NAME]` | 指定堆栈的名称 | 必须给出 |
| `--stack-id [STACK_ID]`     | 指定堆栈的ID | 必须给出 |

成功后输出堆栈信息，否则输出错误信息。

**成功示例**

```
$ ros describe-stack --stack-name ros-cli-demo --stack-id ***
Name                :  ros-cli-demo
Id                  :  ***
Description         :  Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.
Region              :  cn-beijing
Status              :  UPDATE_COMPLETE
StatusReason        :  Stack successfully updated
DisableRollback     :  True
TimeoutMins         :  60
Created             :  2017-06-27T06:25:32
Updated             :  2017-06-27T06:31:37
Webhook             :  None

Parameters:
    SystemDiskCategory  : ***
    ALIYUN::StackName   : ros-cli-demo
    InstanceType        : ***
    ALIYUN::NoValue     : None
    ALIYUN::StackId     : ***
    ALIYUN::Region      : cn-beijing
    DBRootPassword      : ******
    ImageId             : ***
    InstancePassword    : ******
    DBPassword          : ******
    DBUser              : ******
    ALIYUN::AccountId   : ***
    DBName              : MyDatabase
    NginxUrl            : ***

Outputs:
    NginxWebsiteURL     : *** --- URL for newly created Nginx home page.
```

**失败示例**

```
$ ros describe-stack --stack-name ros-cli-demo --stack-id ***
Something wrong:
HTTP Status: 404 Error:StackNotFound The Stack (ros-cli-demo) could not be found. RequestID: None
```

### 资源相关

#### List Resources

使用 `ros list-resources` 命令获取堆栈资源信息，包含如下参数：

| 命令                          | 功能      | 备注   |
| --------------------------- | ------- | ---- |
| `--stack-name [STACK_NAME]` | 指定堆栈的名称 | 必须给出 |
| `--stack-id [STACK_ID]`     | 指定堆栈的ID | 必须给出 |

成功后输出堆栈资源信息，否则输出错误信息。

**成功示例**

```
$ ros list-resources --stack-name ros-cli-demo --stack-id ***

Id                  :  WebServerConditionHandle
Name                :  WebServerConditionHandle
Type                :  ALIYUN::ROS::WaitConditionHandle
Status              :  CREATE_COMPLETE
StatusReason        :  state changed
ResourceData        :  None
PhysicalId          :  
Created             :  2017-06-27T06:25:32
Updated             :  2017-06-27T06:25:33
Deleted             :  None


Id                  :  SecurityGroup
Name                :  SecurityGroup
Type                :  ALIYUN::ECS::SecurityGroup
Status              :  CREATE_COMPLETE
StatusReason        :  state changed
ResourceData        :  None
PhysicalId          :  ***
Created             :  2017-06-27T06:25:32
Updated             :  2017-06-27T06:25:39
Deleted             :  None


Id                  :  WebServer
Name                :  WebServer
Type                :  ALIYUN::ECS::Instance
Status              :  UPDATE_COMPLETE
StatusReason        :  state changed
ResourceData        :  None
PhysicalId          :  ***
Created             :  2017-06-27T06:25:32
Updated             :  2017-06-27T06:31:44
Deleted             :  None


...

```

**失败示例**

```
$ ros list-resources --stack-name ros-cli-demo --stack-id ***2
Message             :  The Stack (ros-cli-demo) could not be found.
Code                :  StackNotFound
```

#### Describe Resource

使用 `ros describe-resource` 命令获取堆栈资源信息，包含如下参数：

| 命令                               | 功能      | 备注   |
| -------------------------------- | ------- | ---- |
| `--stack-name [STACK_NAME]`      | 指定堆栈的名称 | 必须给出 |
| `--stack-id [STACK_ID]`          | 指定堆栈的ID | 必须给出 |
| `--resource-name [RESOUCE_NAME]` | 指定的资源名称 | 必须给出 |

成功后输出堆栈资源信息，否则输出错误信息。

**成功示例**

```
$ ros describe-resource --stack-name ros-cli-demo --stack-id *** --resource-name Vpc

Id                  :  Vpc
Name                :  Vpc
Type                :  ALIYUN::ECS::VPC
Status              :  CREATE_COMPLETE
StatusReason        :  state changed
ResourceData        :  None
PhysicalId          :  ***
Created             :  2017-06-27T06:25:32
Updated             :  2017-06-27T06:25:37
Deleted             :  None
```

**失败示例**

```
$ ros describe-resource --stack-name ros-cli-demo --stack-id *** --resource-name Vpc2
Something wrong:
HTTP Status: 404 Error:ResourceNotFound The Resource (Vpc2) could not be found in Stack ros-cli-demo. RequestID: None
```

#### Resource Type

使用 `ros resoucre-type` 命令获取资源种类信息，包含如下参数：

| 命令                                       | 功能   | 备注              |
| ---------------------------------------- | ---- | --------------- |
| `--status {UNKNOWN, SUPPORTED, DEPRECATED, UNSUPPORTED, HIDDEN}` | 资源状态 | 默认使用`SUPPORTED` |

成功后输出资源种类信息。如果没有符合要求的，无输出。

**成功示例**

```
$ ros resource-type
ALIYUN::CS::App
ALIYUN::CS::Cluster
ALIYUN::ECS::BandwidthPackage
ALIYUN::ECS::Disk
ALIYUN::ECS::DiskAttachment
ALIYUN::ECS::EIP
ALIYUN::ECS::EIPAssociation
ALIYUN::ECS::ForwardEntry
ALIYUN::ECS::Instance
ALIYUN::ECS::InstanceClone
ALIYUN::ECS::InstanceGroup
ALIYUN::ECS::InstanceGroupClone
ALIYUN::ECS::JoinSecurityGroup
ALIYUN::ECS::NatGateway
ALIYUN::ECS::PrepayInstance
ALIYUN::ECS::PrepayInstanceGroupClone
ALIYUN::ECS::Route
ALIYUN::ECS::SNatEntry
ALIYUN::ECS::SSHKeyPair
ALIYUN::ECS::SSHKeyPairAttachment
ALIYUN::ECS::SecurityGroup
ALIYUN::ECS::SecurityGroupClone
ALIYUN::ECS::SecurityGroupEgress
ALIYUN::ECS::SecurityGroupIngress
ALIYUN::ECS::VPC
ALIYUN::ECS::VSwitch
ALIYUN::ESS::ScalingConfiguration
ALIYUN::ESS::ScalingGroup
ALIYUN::ESS::ScalingGroupEnable
ALIYUN::MEMCACHE::Instance
ALIYUN::MONGODB::Instance
ALIYUN::MONGODB::PrepayInstance
ALIYUN::MarketPlace::Image
ALIYUN::MarketPlace::ImageSubscription
ALIYUN::MarketPlace::Order
ALIYUN::OSS::Bucket
ALIYUN::RAM::AccessKey
ALIYUN::RAM::Group
ALIYUN::RAM::ManagedPolicy
ALIYUN::RAM::Role
ALIYUN::RAM::User
ALIYUN::RAM::UserToGroupAddition
ALIYUN::RDS::DBInstance
ALIYUN::RDS::DBInstanceParameterGroup
ALIYUN::RDS::DBInstanceSecurityIps
ALIYUN::RDS::PrepayDBInstance
ALIYUN::REDIS::Instance
ALIYUN::REDIS::PrepayInstance
ALIYUN::ROS::WaitCondition
ALIYUN::ROS::WaitConditionHandle
ALIYUN::SLB::BackendServerAttachment
ALIYUN::SLB::Listener
ALIYUN::SLB::LoadBalancer
ALIYUN::SLB::LoadBalancerClone
ALIYUN::SLB::VServerGroup
ALIYUN::SLS::ApplyConfigToMachineGroup
ALIYUN::SLS::MachineGroup
ALIYUN::VPC::PeeringRouterInterfaceBinding
ALIYUN::VPC::PeeringRouterInterfaceConnection
ALIYUN::VPC::RouterInterface
```

#### Resource Type Detail

使用 `ros resource-type-detail` 命令获取资源种类信息，包含如下参数：

| 命令              | 功能        | 备注   |
| --------------- | --------- | ---- |
| `--name [NAME]` | 指定资源类型的名称 | 必须给出 |

成功后返回资源详细信息，否则输出错误信息。

**成功示例**

由于不同资源的属性有区别，阅读模式下递归列出资源信息。

```
$ ros resource-type-detail --name ALIYUN::ECS::Instance


===================================================

ResourceType :   ALIYUN::ECS::Instance

===================================================

Attributes :

    -----------------------------------------------

    InstanceId :
        Description :   The instance id of created ecs instance

    -----------------------------------------------

    HostName :
        Description :   Host name of created instance.

    -----------------------------------------------

    ZoneId :
        Description :   Zone id of created instance.

    ...

```

`json` 格式输出：

```
$ ros --json resource-type-detail --name ALIYUN::ECS::Instance
{
  "Attributes": {
    "HostName": {
      "Description": "Host name of created instance."
    },
    "InnerIp": {
      "Description": "Inner IP address of the specified instance. Only for classical instance."
    },
    "InstanceId": {
      "Description": "The instance id of created ecs instance"
    },
    "PrivateIp": {
      "Description": "Private IP address of created ecs instance. Only for VPC instance."
    },
    "PublicIp": {
      "Description": "Public IP address of created ecs instance."
    },
    "ZoneId": {
      "Description": "Zone id of created instance."
    }
  },
    ...
}
```

**失败示例** 

```
$ ros --json resource-type-detail --name ALIYUN::ECS::Instance2
Something wrong:
HTTP Status: 404 Error:ResourceTypeNotFound The Resource Type (ALIYUN::ECS::Instance2) could not be found. RequestID: None
```

#### Resource Type template

使用 `ros resource-type-template`命令获取资源种类模板，包含如下参数：

| 命令              | 功能        | 备注   |
| --------------- | --------- | ---- |
| `--name [NAME]` | 指定资源类型的名称 | 必须给出 |

成功后返回资源模板信息，否则输出错误信息。

**成功示例**

```
$ ros --json resource-type-template --name ALIYUN::ECS::Instance
{
  "Outputs": {
    "HostName": {
      "Description": "Host name of created instance.",
      "Value": {
        "Fn::GetAtt": [
          "Instance",
          "HostName"
        ]
      }
    },
    ...
}
```

**失败示例**

```
$ ros resource-type-template --name ALIYUN::ECS::Instance2
Something wrong:
HTTP Status: 404 Error:ResourceTypeNotFound The Resource Type (ALIYUN::ECS::Instance2) could not be found. RequestID: None
```

### 模板相关

#### Get Template

使用 `ros get-template` 命令获取指定堆栈的模板，包含如下参数：

| 命令                          | 功能      | 备注   |
| --------------------------- | ------- | ---- |
| `--stack-name [STACK_NAME]` | 指定堆栈的名称 | 必须给出 |
| `--stack-id [STACK_ID]`     | 指定堆栈的ID | 必须给出 |

获取成功后，输出模板，否则输出错误信息。

**成功示例**

```
$ ros get-template --stack-name ros-cli-demo --stack-id ***


===================================================

ROSTemplateFormatVersion :   2015-09-01

===================================================

Resources :

    -----------------------------------------------

    WebServerConditionHandle :
        Type :   ALIYUN::ROS::WaitConditionHandle

    -----------------------------------------------

    SecurityGroup :
        Type :   ALIYUN::ECS::SecurityGroup
        Properties :
            SecurityGroupIngress :

                    Priority :   1
                    IpProtocol :   all
                    NicType :   intranet
                    SourceCidrIp :   ***
                    PortRange :   -1/-1
            VpcId :
                Ref :   Vpc
            SecurityGroupEgress :

                    Priority :   1
                    IpProtocol :   all
                    NicType :   intranet
                    PortRange :   -1/-1
                    DestCidrIp :   ***

   ...
```

`json` 格式输出：

```
$ ros --json get-template --stack-name ros-cli-demo --stack-id ***
{
  "Description": "Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.",
  "Outputs": {
    "NginxWebsiteURL": {
      "Description": "URL for newly created Nginx home page.",
      "Value": {
        "Fn::Join": [
          "",
          [
            "http://",
            {
              "Fn::GetAtt": [
                "WebServer",
                "PublicIp"
              ]
            },
            ":80/test.php"
          ]
        ]
      }
    }
  },
  ...
```

**失败示例**

```
$ ros get-template --stack-name ros-cli-demo --stack-id ***
Something wrong:
HTTP Status: 404 Error:SDK.UnknownServerError Can not parse error message from server response. RequestID: None
```

#### Validate Template

使用 `ros validate-template` 命令验证指定堆栈的模板，包含如下参数：

| 命令                              | 功能     | 备注   |
| ------------------------------- | ------ | ---- |
| `--template-url [TEMPLATE_URL]` | 指定模板地址 | 必须给出 |

获取成功后，输出模板，否则输出错误信息。

**成功示例**

```
$ ros validate-template --template-url PATH\\TO\\template.json
The template is ok:



===================================================

Description :   Deploy LNMP(Linux+Nginx+MySQL+PHP) stack on 1 ECS instance. *** WARNING *** Only support CentOS-7.

===================================================

Parameters :

    -----------------------------------------------

    SystemDiskCategory :
        Description :   System disk category: average cloud disk(cloud), efficient cloud disk(cloud_efficiency) or SSD cloud disk(cloud_ssd)
        Default :   cloud_ssd
        Label :   SystemDiskCategory
        NoEcho :   false
        AllowedValues :
                cloud
                cloud_efficiency
                cloud_ssd
        Type :   String
...
```

**失败示例**

```
$ ros validate-template --template-url C:\\Users\\quming.ly\\Desktop\\nodejs.json
Something wrong:
HTTP Status: 400 Error:InvalidTemplateVersion The template version is invalid: "ROSTemplateFormatVersion: 2015-09-02". "ROSTemplateFormatVersion" should be: 2015-09-01 RequestID: None
```

### 其他

#### List Regions

列出所有的区域，无需参数。

**成功示例**

```
$ ros list-regions
LocalName                               RegionId

华北 1                                  cn-qingdao
华北 2                                  cn-beijing
华北 3                                  cn-zhangjiakou
华东 1                                  cn-hangzhou
华东 2                                  cn-shanghai
华南 1                                  cn-shenzhen
香港                                    cn-hongkong
亚太东北 1 (东京)                       ap-northeast-1
亚太东南 1 (新加坡)                     ap-southeast-1
亚太东南 2 (悉尼)                       ap-southeast-2
美国东部 1 (弗吉尼亚)                   us-east-1
美国西部 1 (硅谷)                       us-west-1
中东东部 1 (迪拜)                       me-east-1
欧洲中部 1 (法兰克福)                   eu-central-1
```

`json`格式输出：

```
$ ros --json list-regions
{
  "Regions": [
    {
      "LocalName": "华北 1",
      "RegionId": "cn-qingdao"
    },
    {
      "LocalName": "华北 2",
      "RegionId": "cn-beijing"
    },
    {
      "LocalName": "华北 3",
      "RegionId": "cn-zhangjiakou"
    },
    {
      "LocalName": "华东 1",
      "RegionId": "cn-hangzhou"
    },
    {
      "LocalName": "华东 2",
      "RegionId": "cn-shanghai"
    },
    {
      "LocalName": "华南 1",
      "RegionId": "cn-shenzhen"
    },
    {
      "LocalName": "香港",
      "RegionId": "cn-hongkong"
    },
    {
      "LocalName": "亚太东北 1 (东京)",
      "RegionId": "ap-northeast-1"
    },
    {
      "LocalName": "亚太东南 1 (新加坡)",
      "RegionId": "ap-southeast-1"
    },
    {
      "LocalName": "亚太东南 2 (悉尼)",
      "RegionId": "ap-southeast-2"
    },
    {
      "LocalName": "美国东部 1 (弗吉尼亚)",
      "RegionId": "us-east-1"
    },
    {
      "LocalName": "美国西部 1 (硅谷)",
      "RegionId": "us-west-1"
    },
    {
      "LocalName": "中东东部 1 (迪拜)",
      "RegionId": "me-east-1"
    },
    {
      "LocalName": "欧洲中部 1 (法兰克福)",
      "RegionId": "eu-central-1"
    }
  ]
}
```

#### List Events

使用 `ros list-events` 命令查看事件列表，包含如下参数：

| 命令                                       | 功能       | 备注                  |
| ---------------------------------------- | -------- | ------------------- |
| `--stack-name [STACK_NAME]`              | 指定堆栈的名称  |                     |
| `--stack-id [STACK_ID]`                  | 指定堆栈的ID  |                     |
| `--resource-status {'COMPLETE', 'FAILED', 'IN_PROGRESS'}` | 指定资源的状态  | 必须使用指定值             |
| `--resource-name`                        | 指定筛选资源   |                     |
| `--resource-type`                        | 指定筛选资源类型 |                     |
| `--page-number [PAGE_NUMBER]`            | 输入查看的页码  | 查询结果将分页返回，从1开始，默认为1 |
| `--page-size [PAGE_SIZE]`                | 指定每页显示数量 | 默认为10，不超过100        |

输出当前的翻页情况及结果列表：

**成功示例**

```
$ ros list-events --stack-name ros-cli-demo --stack-id *** --page-number 2 --page-size 3 --resource-status COMPLETE

Total Records: 12     Page: 2/4

Time                :  2017-06-27T06:31:21
ResourceName        :  WebServer
ResourceType        :  ALIYUN::ECS::Instance
Type                :  None
Status              :  UPDATE_COMPLETE
StatusReason        :  state changed


Time                :  2017-06-27T06:28:14
ResourceName        :  ros-cli-demo
ResourceType        :  ALIYUN::ROS::Stack
Type                :  None
Status              :  CREATE_COMPLETE
StatusReason        :  Stack CREATE completed successfully


Time                :  2017-06-27T06:28:14
ResourceName        :  WebServerWaitCondition
ResourceType        :  ALIYUN::ROS::WaitCondition
Type                :  None
Status              :  CREATE_COMPLETE
StatusReason        :  state changed
```

#### Set userdata

使用 `set-userdata` 命令设置默认的用户配置。

| 命令                            | 功能                           | 备注   |
| ----------------------------- | ---------------------------- | ---- |
| `--key-id [KEY_ID]`           | 默认的 ALIYUN Access Key ID     |      |
| `--key-secret [KEY_SECRET]`   | 默认的 ALIYUN Access Key Secret |      |
| `--region-id [REGION_ID]`     | 默认的 region-id                |      |
| `--json-indent [JSON_INDENT]` | JSON输出时的缩进                   |      |
| `--debug {'False', 'True'}`   | 是否开启Debug输出                  |      |
   