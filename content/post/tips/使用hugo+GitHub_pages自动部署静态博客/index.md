---
title: "使用hugo+GitHub pages自动部署静态博客"
date: 2021-12-19T18:00:54+08:00
draft: false
categories:
    - Tips
tags:
    - hugo
    - github
---

### 准备好环境
- 安装hugo
- 安装Git
### 创建GitHub仓库
仓库名命名为：USERNAME.github.io
### 设置本地hugo站
    
1. 创建新的站点
    ```bash
    hugo new site --force .
    ```
2. 安装主题
    ```bash
    git submodule add https://github.com/CaiJimmy/hugo-theme-stack/ themes/hugo-theme-stack
    ```
3. 设置主题
   
   参考主题说明网站

   
4. 推送到GitHub
   ```bash
   git add .
   git commit -m "初始化博客网站"
   git push origin
   ```
5. 设置GitHub actions
    创建文件夹
   ```bash
   mkdir -p .github/workflows

   ```
   在文件夹下面创建文件cd.yml

   ```yml
    name: Build and Deploy Site

    on:
        push:
            branches:
            - main
        pull_request:
            branches:
            - main

    jobs:
        build-and-deploy-site:
            runs-on: ubuntu-latest
            steps:
            - name: Checkout repo
                uses: actions/checkout@v2
                with:
                submodules: true
                fetch-depth: 0

            - name: Setup Hugo
                uses: peaceiris/actions-hugo@v2
                with:
                hugo-version: 'latest'
                extended: true

            - name: Build site with Hugo
                run: hugo --minify

            - name: Check HTML
                uses: chabad360/htmlproofer@master
                with:
                directory: "./public"
                arguments: --only-4xx --check-favicon --check-html --assume-extension --empty-alt-ignore --disable-external
                continue-on-error: true

            - name: Deploy to GitHub Pages
                if: github.event_name == 'push' && github.ref == 'refs/heads/main'
                uses: peaceiris/actions-gh-pages@v3
                with:
                github_token: ${{ secrets.GITHUB_TOKEN }}
                publish_dir: ./public

   ```
6. 设置GitHub pages
   仓库设定pages目录为新的分支
