---
title: "GitHub Actions 托管 Docker 镜像"
created_at: "2025-10-14 10:00:31"
updated_at: "2025-10-14 10:00:31"
issue_number: 23
labels: ['docker']
url: https://github.com/syaofox/syaofox.github.io/issues/23
---

# GitHub Actions 托管 Docker 镜像

将 **GitHub 项目**中的 **Docker 镜像**托管在 **GitHub Container Registry (GHCR)** 上的最佳和最自动化的方法是使用 **GitHub Actions**。

以下是实现这一目标的详细步骤和示例工作流程：



## 步骤一：准备项目

1.  **编写 Dockerfile：** 确保项目根目录或指定目录中有一个有效的 `Dockerfile`，用于构建应用镜像。
    
2.  **（可选）添加 .dockerignore 文件：** 排除构建时不必要的文件（如 `.git`、`node_modules` 等），以加快构建速度并减小镜像大小。
    


## 步骤二：创建 GitHub Actions 工作流

需要创建一个 GitHub Actions 工作流文件（通常位于 `.github/workflows/` 目录下），该工作流将在代码推送到特定分支（如 `main` 或 `master`）时自动构建 Docker 镜像并将其推送到 GHCR。

### 示例工作流文件（`build-and-push-image.yml`）



```YAML
name: Docker Image CI to GHCR

# 定义触发工作流的事件
on:
  push:
    branches: [ "main" ] # 仅在推送到 main 分支时运行

# 定义权限，必须包含 packages: write 才能推送镜像到 GHCR
permissions:
  contents: read
  packages: write

jobs:
  build-and-push-image:
    runs-on: ubuntu-latest
    
    steps:
      - name: ⬇️ Checkout code
        uses: actions/checkout@v4

      - name: ⚙️ Set up QEMU (用于跨平台构建)
        uses: docker/setup-qemu-action@v3
      
      - name: 🛠️ Set up Docker Buildx (用于增强构建功能)
        uses: docker/setup-buildx-action@v3

      - name: 🔑 Login to GitHub Container Registry (GHCR)
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          # 使用内置的 ${{ github.actor }} 作为用户名
          username: ${{ github.actor }} 
          # 使用自动生成的 GITHUB_TOKEN 作为密码
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: 🏷️ Extract Docker metadata (提取镜像名和标签)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }} # 镜像格式: ghcr.io/<owner>/<repo_name>
          tags: |
            type=sha,prefix=sha-,format=long
            type=raw,value=latest,enable={{is_default_branch}} # 如果是默认分支，打 latest 标签

      - name: 🔨 Build and Push Docker image
        uses: docker/build-push-action@v5
        with:
          context: . # Dockerfile 所在的构建上下文路径 (默认为项目根目录)
          push: true # 设为 true 才会推送到注册表
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          # file: ./path/to/Dockerfile # 如果 Dockerfile 不在根目录，请取消注释并指定路径
          # cache-from: type=gha # 可选：使用 GitHub Actions 缓存加速后续构建
          # cache-to: type=gha,mode=max 
``` 


## 关键配置说明

| 配置项 | 描述 | 作用 |
| :--- | :--- | :--- |
| **permissions: packages: write** | 必须。授予工作流向 GHCR (packages) 写入（推送）镜像的权限。 | 允许推送操作成功。 |
| **uses: docker/login-action@v3** | 登录到 GHCR 注册表。 | 认证推送操作。 |
| **username: \${{ github.actor }}** | 自动使用触发工作流的 GitHub 用户名或组织名。 | 避免硬编码用户名。 |
| **password: \${{ secrets.GITHUB\_TOKEN }}** | 使用 GitHub 自动生成的临时令牌进行身份验证。 | 最安全且推荐的方式，无需创建个人访问令牌（PAT）。 |
| **uses: docker/metadata-action@v5** | 自动生成标准的 Docker 镜像名称和标签。 | 保持标签一致性和规范性。 |
| **images: ghcr.io/\${{ github.repository }}** | 设置镜像的完整名称，例如：`ghcr.io/your-username/your-repo`。 | 确定 GHCR 上的托管位置。 |
| **uses: docker/build-push-action@v5** | 核心步骤，负责构建镜像并推送到 GHCR。 | 自动化构建和托管过程。 |
| **push: true** | 确保构建成功后，镜像会被推送到已登录的注册表。 | 实际完成托管。 |


## 步骤三：查看托管的镜像

一旦工作流成功运行，就可以在 GitHub 上查看 Docker 镜像：

1.  导航到 **GitHub 仓库**。
    
2.  点击仓库主页右侧的 **Packages** 或 **Packages and Deployments** 选项卡。
    
3.  将看到推送的 Docker 镜像及其不同的标签。
    

现在，其他用户就可以使用以下命令来拉取镜像了：

```Bash
docker pull ghcr.io/<用户名或组织名>/<仓库名>:<标签>
```


