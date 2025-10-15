---
title: "docker构建项目，并推送到dockerhub"
created_at: "2025-10-03 07:25:14"
updated_at: "2025-10-09 11:20:13"
issue_number: 8
labels: ['docker']
url: https://github.com/syaofox/syaofox.github.io/issues/8
---

# docker构建项目，并推送到dockerhub

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


### 飞牛os拉取私人镜像

先ssh连接飞牛,再执行登录
```shell
docker login
```

如果是管理权限

```shell
sudo docker login
```

