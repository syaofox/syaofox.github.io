---
title: "如何在 Ubuntu 安装 Samba 实现文件夹共享"
date: 2020-06-18T11:05:14+08:00
description: ""
tags: [Ubuntu, SMB]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: Linux
comment : false
draft: false 
author: "syaofox"
type: post
---

samba的优点在于可以在WindowsLinuxAndriod之间实现文件夹共享传输文件，适用的范围更广，更推荐大家选择这种方式_
<!-- more -->

## 一、安装samba

```shell
# 获取最新的版本信息
sudo apt update
# 安装samba
sudo apt-get install samba
# 安装samba客户端（可选）
sudo apt-get install smbclient 
```

## 二、创建samba配置文件

```shell
# 创建共享目录
sudo mkdir -p /share
# 对目录进行赋权
sudo chmod 777 /share
# 对配置文件进行备份
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
# 修改配置文件
sudo nano /etc/samba/smb.conf
# 在配置文件的末尾添加下面的代码：
[share]

        path = /share

        browseable = yes

        writable = yes

        comment = smb share test

        public = yes
```

```perl
# 配置文件的名称解释：

        [share] # 该共享的共享名

        comment = smb share test # 该共享的备注

        path = /home/share # 共享路径

        allow hosts = host(subnet) # 设置该Samba服务器允许的工作组或者域

        deny hosts = host(subnet) # 设置该Samba服务器拒绝的工作组或者域

        available = yes|no # 设置该共享目录是否可用

        browseable = yes|no # 设置该共享目录是否可显示

        writable = yes|no # 指定了这个目录缺省是否可写，也可以用readonly = no来设置可写

        public = yes|no # 指明该共享资源是否能给游客帐号访问，guest ok = yes其实和public = yes是一样的

        user = user, @group # user设置所有可能使用该共享资源的用户，也可以用@group代表group这个组的所有成员，不同的项目之间用空格或者逗号隔开

        valid users = user, @group # 指定能够使用该共享资源的用户和组

        invalid users = user, @group # 指定不能够使用该共享资源的用户和组

        read list = user, @group # 指定只能读取该共享资源的用户和组

        write list = user, @group # 指定能读取和写该共享资源的用户和组

        admin list = user, @group # 指定能管理该共享资源（包括读写和权限赋予等）的用户和组

        hide dot files = yes|no # 指明是否像UNIX那样隐藏以“.”号开头的文件

        create mode = 0755 # 指明新建立的文件的属性，一般是0755

        directory mode = 0755 # 指明新建立的目录的属性，一般是0755

        sync always = yes|no # 指明对该共享资源进行写操作后是否进行同步操作

        short preserve case = yes|no # 指明是否区分文件名大小写

        preserve case = yes|no # 指明是否保持大小写

        case sensitive = yes|no # 指明是否对大小写敏感，一般选no，不然可能引起错误

        mangle case = yes|no # 指明混合大小写

        default case = upper|lower # 指明缺省的文件名是全部大写还是小写

        force user = testuser # 强制把建立文件的属主是谁。如果我有一个目录，让guest可以写，那么guest就可以删除，如果我用force user= testuser强制建立文件的属主是testuser，同时限制create mask = 0755，这样guest就不能删除了

        wide links = yes|no # 指明是否允许共享外符号连接，比如共享资源里面有个连接指向非共享资源里面的文件或者目录，如果设置wide links = no将使该连接不可用

        max connections = 100 # 设定最大同时连接数

        delete readonly = yes|no # 指明能否删除共享资源里面已经被定义为只读的文件
```

## 三、创建samba用户

```plain
# 创建samba用户（注意，创建samba用户之前，必须先确保有一个同名的Linux用户，否则samba用户会创建失败。）
sudo smbpasswd -a smbuser
```

## 四、重启samba服务

```plain
# 重启samba服务
sudo service smbd restart
```

## 五、客户端访问测试

### 1.Linux客户端

```plain
smbclient -L //localhost/share
```

### 2.Windows客户端

主机：Ubuntu18.04

客机：Windows10

①查询主机在局域网的ip

在终端中输入`ifconfig`,inet后面的IP地址就是主机在局域网的IP。

  ![](/如何在-Ubuntu-安装-Samba-实现文件夹共享/1569231337-59cb6679e51317a02dc2696bf4455f8d.jpg)

”wlp7s0“是我的设备名，inet后面的”192.168.2.195“是主机在局域网的IP。

②选中客机的”此电脑“，右键点击”映射网络驱动器“

 ![](/如何在-Ubuntu-安装-Samba-实现文件夹共享/1569231337-39676e2fce3b0fe3e6fab003d90bcb67.jpg)

③输入`\\主机的IP\share`，点击”完成“按钮

 ![](/如何在-Ubuntu-安装-Samba-实现文件夹共享/1569231337-edc09791d530a57f20d0d0286ce99e0b.jpg)

 ![](/如何在-Ubuntu-安装-Samba-实现文件夹共享/1569231337-945ef5e8edc836a39622f72d15574b04.jpg)

如果提示”你不能访问此共享文件夹，因为你组织的安全策略阻止未经身份验证的来宾访问“，勾选上面图片中的”使用其他凭据连接“的选项，输入你的samba用户名和密码进行登录即可。

### 3.Andriod客户端

打开”ES文件浏览器“，选择”局域网“，添加网络，输入`\\主机的IP\share`进行访问，具体的操作步骤这里就不一一解释了。

## 六、挂载 Samba 共享

**安装CIFS Utils pkg**

```shell
sudo apt-get install cifs-utils
```
**创建一个挂载点**

```shell
sudo mkdir /mnt/local_share
```
**步骤3：挂载**
```shell
sudo mount -t cifs //<vpsa_ip_address>/<export_share> /mnt/<local_share>
```
**开机自动挂载**

/etc/fstab 文件里添加：
```shell
<vpsa_ip_address>/<export_share> cifs user=<user on VPSA>,pass=<passwd on VPSA> 0 0
````