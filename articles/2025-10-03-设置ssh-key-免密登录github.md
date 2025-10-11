---
title: "设置ssh-key-免密登录github"
created_at: "2025-10-03 07:10:19"
updated_at: "2025-10-03 07:10:19"
issue_number: 6
state: open
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/6
---

# 设置ssh-key-免密登录github



如何在 **Linux Mint** 系统上设置 **SSH 密钥**，以便安全、免密地登录 **GitHub** 



## 步骤一：检查现有 SSH 密钥

首先，检查您的系统上是否已经存在 SSH 密钥。

1.  **打开终端**（Terminal）。
2.  输入以下命令：
    ```bash
    ls -al ~/.ssh
    ```
      * 如果看到名为 `id_rsa.pub`、`id_ecdsa.pub` 或 `id_ed25519.pub` 的文件，说明您可能已有密钥。您可以选择使用它，或者按照下一步生成新密钥。
      * 如果**没有**看到这些文件，或该目录不存在，请进行下一步生成新密钥。



## 步骤二：生成新的 SSH 密钥对

如果您没有现有的密钥，或者想为 GitHub 创建一个专用的密钥，请执行以下操作：

1.  在终端中输入以下命令生成一个 **Ed25519** 算法的密钥对（这是目前推荐的安全算法）：
    ```bash
    ssh-keygen -t ed25519 -C "您的GitHub邮箱地址"
    ```
      * 将 `"您的GitHub邮箱地址"` 替换为您在 GitHub 上使用的邮箱地址。
2.  系统会提示您选择密钥的保存位置：
    ```bash
    Enter file in which to save the key (/home/youruser/.ssh/id_ed25519): 
    ```
      * **直接按 Enter 键** 接受默认路径（推荐）。
3.  系统会提示您设置一个**密码**（passphrase）：
    ```bash
    Enter passphrase (empty for no passphrase): 
    ```
      * **建议设置一个强密码**。每次使用 SSH 密钥进行操作时都需要输入此密码。如果您不想每次都输入密码，可以直接按 Enter 键留空，但这会降低安全性。

完成这些步骤后，您的密钥对就生成好了：

  * **私钥**（Private Key）：`~/.ssh/id_ed25519` (必须保密)
  * **公钥**（Public Key）：`~/.ssh/id_ed25519.pub` (需要上传到 GitHub)


## 步骤三：将 SSH 公钥添加到 GitHub

现在，您需要将生成的公钥内容复制并粘贴到您的 GitHub 账户设置中。

### 3.1 复制公钥内容

在终端中运行以下命令，将公钥内容复制到剪贴板：

```bash
cat ~/.ssh/id_ed25519.pub
```

  * **⚠️ 注意：** 复制终端输出的**完整**内容，它通常以 `ssh-ed25519` 开头，以您的邮箱地址结尾。

### 3.2 登录 GitHub 添加公钥

1.  打开浏览器，登录 **GitHub**。
2.  点击右上角的**头像** -\> 选择 **Settings**（设置）。
3.  在左侧导航栏中，选择 **SSH and GPG keys**。
4.  点击 **New SSH key** 或 **Add SSH key** 按钮。
5.  在 **Title** 字段，输入一个容易识别的名称，例如 `Linux Mint Home PC`。
6.  在 **Key** 字段，粘贴您在 **3.1 步**中复制的**完整公钥内容**。
7.  点击 **Add SSH key** 按钮。系统可能会要求您再次输入 GitHub 密码进行确认。


## 步骤四：将私钥添加到 SSH 代理 (ssh-agent)

为了让系统自动管理您的私钥（特别是如果您设置了密码），您需要启动 `ssh-agent` 并将私钥添加到其中。

1.  **启动 ssh-agent：** (Linux Mint 通常在会话启动时自动运行，但可以手动检查)
    ```bash
    eval "$(ssh-agent -s)"
    ```
2.  **添加私钥：**
    ```bash
    ssh-add ~/.ssh/id_ed25519
    ```
      * 如果设置了密码，系统会提示您输入密码。输入后，该私钥将在您的当前会话中被记住。

-----

## 步骤五：测试 SSH 连接

最后一步是测试您的 SSH 连接是否设置成功。

在终端中输入以下命令：

```bash
ssh -T git@github.com
```

  * 如果这是您第一次连接，系统可能会提示您确认连接：
    ```
    The authenticity of host 'github.com (IP地址)' can't be established.
    Are you sure you want to continue connecting (yes/no/[fingerprint])? 
    ```
    输入 `yes` 并按 Enter 确认。
  * 如果连接成功，您会看到类似如下的欢迎信息：
    ```
    Hi *您的GitHub用户名*! You've successfully authenticated, but GitHub does not provide shell access.
    ```

-----

## 完成

现在，您的 Linux Mint 系统就可以使用 SSH 密钥免密（或只需输入一次密码）安全地与 GitHub 进行交互了。您可以使用 SSH URL 来克隆仓库：

```bash
git clone git@github.com:用户名/仓库名.git
```

如果您在克隆时使用的是 HTTPS URL，请确保将其更改为 SSH URL。

