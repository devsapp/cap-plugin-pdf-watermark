
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# start-pdf-watermark-v3 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-pdf-watermark-v3&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-pdf-watermark-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-pdf-watermark-v3&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-pdf-watermark-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-pdf-watermark-v3&type=packageDownload">
  </a>
</p>

<description>

本案例将 PDF Watermark，这一方便且实用的工具，快速创建并部署到阿里云函数计算 FC。

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/start-pdf-watermark/tree/V3/src)

</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>



| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=start-pdf-watermark-v3) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=start-pdf-watermark-v3) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init start-pdf-watermark-v3 -d start-pdf-watermark-v3`
  - 进入项目，并进行项目部署：`cd start-pdf-watermark-v3 && s deploy -y`
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

本案例将 PyPDF2，这一广泛使用的 Python 库，快速创建并部署到阿里云函数计算 FC。

PyPDF2 使得处理PDF文件变得既简单又高效。通过这个库，用户可以执行多种对PDF文件的操作，包括读取、写入以及修改PDF。

通过 Serverless 开发平台，您只需要几步，就可以体验  PDF Watermark工具，并享受 Serverless 架构带来的降本提效的技术红利。

</appdetail>

## 使用流程

<usedetail id="flushContent">

### 查看部署的案例

项目部署完成，可以通过控制台进行测试：

1、部署成功后，从资源信息栏，找到对应函数资源，点击函数名称跳转到函数计算控制台，如：
![](https://img.alicdn.com/imgextra/i1/O1CN01BPKckL1yNjuFgfmgE_!!6000000006567-0-tps-1564-446.jpg)
2、在代码页签，单击测试函数右侧的图标，从下拉列表中选择配置测试参数，输入如下示例测试参数，然后单击确定。

```
{
    "pdf_file": "example.pdf",
    "mark_text": "AliyunFC",  
    "pagesize": [595.275590551181, 841.8897637795275], 
    "font": "Helvetica", 
    "font_size": 30, 
    "font_color": [0, 0, 0], 
    "rotate": 30, 
    "opacity": 0.1, 
    "density": [198.4251968503937, 283.46456692913387] 
}
```


| 参数 | 是否必填 | 描述 |
|----------|----------------|------------------|
| pdf_file | 必填 | pdf文件名称 |
| mark_text | 必填 | 水印文字， 如果给 PDF 加水印 |
| pagesize | 可选 | 默认是 A4 大小， (21*cm, 29.7*cm), 其中 1cm=28.346456692913385 |
| font | 可选 | 字体，默认为 Helvetica,  中文字体可选择为 zenhei 或 microhei |
| font_size | 可选 | 字体的大小，默认为 30 |
| font_color | 可选 | 字体颜色，格式为 RGB， 默认为黑色 |
| rotate | 可选 | 旋转角度，默认为 0 |
| opacity | 可选 | 透明度，默认为 0.1， 1 表示不透明 |
| density | 可选 | 水印密度，水印文字间隔，默认是 [141.73228346456693, 141.73228346456693]，即（7*cm, 10*cm),  表示每个水印文字在横坐标和纵坐标的间隔分别是 7cm 和 10 |

3、单击测试函数，函数执行成功后，查看返回结果。

```bash
 upload to oss success!
```

如果您需要使用 SDK 调用这个函数， 可以参考  [OpenAPI](https://next.api.aliyun.com/api/FC) 

生成带有水印的 example_out.pdf 示例，生成的 pdf 文件在和输入的 pdf 文件在相同的 OSS 目录中:

![](https://img.alicdn.com/imgextra/i1/O1CN01Tu6Ovz1gT5GcXhfm0_!!6000000004142-2-tps-647-842.png)

### 二次开发

您可以通过云端控制台的开发功能进行二次开发。如果您之前是在本地创建的项目案例，也可以在本地项目目录`start-pdf-watermark-v3`文件夹下，对项目进行二次开发。开发完成后，可以通过`s deploy`进行快速部署。

</usedetail>

## 注意事项

<matters id="flushContent">
</matters>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
