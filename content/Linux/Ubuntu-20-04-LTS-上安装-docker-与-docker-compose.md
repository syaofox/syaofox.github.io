---
title: "Ubuntu 20.04 LTS 上安装 Docker 与 Docker-Compose"
date: 2020-06-18T11:14:43+08:00
description: ""
tags: [Ubunt, Docker]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

记录 docker 与 docker-compose 安装过程 基于 Ubuntu 20.04 LTS

# 安装docker

### 更新包列表
```bash
sudo apt update
```
### 安装必备软件包
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
### 将官方Docker存储库的GPG密钥添加到系统
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
### 将Docker存储库添加到APT源
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```
### 再次更新包列表
```bash
sudo apt update
```
### 查看缓存apt，确保从Docker repo而不是默认的Ubuntu 16.04 repo安装

```bash
apt-cache policy docker-ce
```
###  最后，安装Docker
```bash
sudo apt install docker-ce
```
# 安装Docker Compose
### 下载
```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.26.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```
### 设置权限
```bash
sudo chmod +x /usr/local/bin/docker-compose
```
### 验证
```bash
docker-compose --version
```