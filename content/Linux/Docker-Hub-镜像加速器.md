---
title: "Docker Hub 镜像加速器"
date: 2020-06-18T12:06:21+08:00
description: ""
tags: [Docker, DockerHub]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

国内从 Docker Hub 拉取镜像有时会遇到困难，此时可以配置镜像加速器。Docker 官方和国内很多云服务商都提供了国内加速器服务。*

<!--more-->

## 配置加速地址

> Ubuntu 16.04+、Debian 8+、CentOS 7+

创建或修改 `/etc/docker/daemon.json`：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
    "registry-mirrors": [
        "https://1nj0zren.mirror.aliyuncs.com",
        "https://docker.mirrors.ustc.edu.cn",
        "http://f1361db2.m.daocloud.io",
        "https://registry.docker-cn.com"
    ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Docker Hub 镜像加速器列表

| 镜像加速器 | 镜像加速器地址 | 专属加速器[？](# "需登录后获取平台分配的专属加速器") | 其它加速[？](# "支持哪些镜像来源的镜像加速") |
| --- | --- | --- | --- |
| [Docker 中国官方镜像](https://link.juejin.im/?target=https%3A%2F%2Fdocker-cn.com%2Fregistry-mirror) | `https://registry.docker-cn.com` |  | Docker Hub |
| [DaoCloud 镜像站](https://link.juejin.im/?target=https%3A%2F%2Fdaocloud.io%2Fmirror) | `http://f1361db2.m.daocloud.io` | 可登录，系统分配 | Docker Hub |
| ~~[Azure 中国镜像](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2FAzure%2Fcontainer-service-for-azure-china%2Fblob%2Fmaster%2Faks%2FREADME.md%2322-container-registry-proxy)~~ | ~~`https://dockerhub.azk8s.cn`~~ | 已失效 | Docker Hub、GCR、Quay |
| [科大镜像站](https://link.juejin.im/?target=https%3A%2F%2Fmirrors.ustc.edu.cn%2Fhelp%2Fdockerhub.html) | `https://docker.mirrors.ustc.edu.cn` |  | Docker Hub、[GCR](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fustclug%2Fmirrorrequest%2Fissues%2F91)、[Quay](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fustclug%2Fmirrorrequest%2Fissues%2F135) |
| [阿里云](https://link.juejin.im/?target=https%3A%2F%2Fcr.console.aliyun.com) | `https://<your_code>.mirror.aliyuncs.com` | 需登录，系统分配 | Docker Hub |
| [七牛云](https://link.juejin.im/?target=https%3A%2F%2Fkirk-enterprise.github.io%2Fhub-docs%2F%23%2Fuser-guide%2Fmirror) | `https://reg-mirror.qiniu.com` |  | Docker Hub、GCR、Quay |
| [网易云](https://link.juejin.im/?target=https%3A%2F%2Fc.163yun.com%2Fhub) | `https://hub-mirror.c.163.com` |  | Docker Hub |
| [腾讯云](https://link.juejin.im/?target=https%3A%2F%2Fcloud.tencent.com%2Fdocument%2Fproduct%2F457%2F9113) | `https://mirror.ccs.tencentyun.com` |  | Docker Hub |

## 检查加速器是否生效

命令行执行 `docker info`，如果从结果中看到了如下内容，说明配置成功。

```bash
Registry Mirrors:
 [...]
 https://registry.docker-cn.com/
```

## Docker Hub 镜像测速

使用镜像前后，可使用 `time` 统计所花费的总时间。测速前先移除本地的镜像！

```bash
$ docker rmi node:latest
$ time docker pull node:latest
Pulling repository node
[...]

real   1m14.078s
user   0m0.176s
sys    0m0.120s
```

* * *