---
title: "Ubuntu 配置 Postfix 通过 Gmail 发送邮件"
date: 2020-06-18T20:31:51+08:00
description: ""
tags: [Ubuntu, Gmail, Postfix]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

## 修改 Ubuntu 本机 Hostname

### 查看当前 hostname

```bash
hostname -f
```

### 修改当前 hostname

可以通过命令修改 hostname
```ini
hostname syaofox.com
```
但是这样修改只是临时的,系统重启后失效,必须修改配置文件才能永久生效

```bash
sudo nano /etc/hostname
```

修改为
```ini
syaofox.com
```

### 修改 hosts

修改 hosts 文件

```bash
sudo nano /etc/hosts
```

修改 127.0.1.1 解析为刚才修改的 hostname

```ini
127.0.1.1 syaofox.com
```

重启

## 安装 Postfix

```bash
sudo apt update

sudo apt install mailutils
```
选择 Internet Site

![](/linuxubuntu-配置-Postfix-通过-Gmail-发送邮件/Configure_Postfix_Installation.png)

下一步填入hostname

![](/linuxubuntu-配置-Postfix-通过-Gmail-发送邮件/Configure_Postfix_with_FQDN_hostname.png)

>以后可以通过输入以下命令修改配置

```bash
dpkg-reconfigure postfix
```

## 使用Gmail SMTP 配置 Postfix

### 修改配置文件

```bash
sudo nano /etc/postfix/main.cf
```
找到 relayhost= 这行,修改

```ini

myhostname = syaofox.com

relayhost = [smtp.gmail.com]:587

mydestination = localhost.syaofox.com, , localhost
```
配置文件末尾添加

```ini
# Enables SASL authentication for postfix
smtp_sasl_auth_enable = yes
# Disallow methods that allow anonymous authentication
smtp_sasl_security_options = noanonymous
# Location of sasl_passwd we saved
smtp_sasl_password_maps = hash:/etc/postfix/sasl/sasl_passwd
# Enable STARTTLS encryption for SMTP
smtp_tls_security_level = encrypt
# Location of CA certificates for TLS
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
```
### 添加SMTP连接信息文件

```bash
sudo nano /etc/postfix/sasl/sasl_passwd
```
里面添加

```ini
[smtp.gmail.com]:587 syaofox@gmail.com:密码  #你的Gmail地址和密码,开启两步验证的请使用应用专用密码

```
转换配置文件

```bash
sudo postmap /etc/postfix/sasl/sasl_passwd
```
修改配置文件权限

```bash
chown root:root /etc/postfix/sasl/sasl_passwd
chmod 600 /etc/postfix/sasl/sasl_passwd

```

### 重启 Postfix 服务

```bash
sudo service postfix restart

```

## 发送测试邮件

```bash
echo "这是邮件正文" | mail -s "这是邮件标题" syaofox@gmail.com

# 发送带附件的邮件

echo "这是邮件正文" | mail -s "这是邮件标题" -A ~/test.txt syaofox@gmail.com

```

### 修改邮件发件人显示名

默认邮件发送人显示root,可以通过下面命令修改

```bash
# 查看当期邮件发送人
getent passwd $USER | cut -d ':' -f 5 | cut -d ',' -f 1

# 显示
root

# 修改root的显示名

sudo chfn -f "FirstName LastName" root


```