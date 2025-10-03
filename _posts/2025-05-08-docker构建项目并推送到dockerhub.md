---
layout: post
title: docker构建项目并推送到dockerhub
date: 2025-05-08 11:43:00 +0800
categories: [tips]
tags: [docker]
---

 ## 以 syaofox/homer 为例

先在hub上创建名为homer的仓库

### 构建镜像

```shell
 docker build -t syaofox/homer:latest .
```

### 本地测试

```shell
docker run -d -p  1000:80 syaofox/homer:latest
```

### 登录hub

```shell
docker login
```

### 打标

```shell
docker tag syaofox/homer syaofox/homer:v1.0 
```

### 推送到hub

```shell
docker push syaofox/homer:v1.0 
```

### 私人的仓库多登录步骤

```shell
docker login
```
