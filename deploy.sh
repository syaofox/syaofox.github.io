#!/bin/bash
# 部署到 github pages 脚本
# 错误时终止脚本
set -e

echo '删除打包文件夹'
rm -rf public

echo '打包。diray主题'
hugo -t diary

echo 'push网站源码'
git init
git add -A

# Commit changes.
msg="modify site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

git push 