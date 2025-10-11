---
title: "Linux 调整 Swap 文件大小指南"
created_at: "2025-10-03 07:21:17"
updated_at: "2025-10-03 07:21:17"
issue_number: 7
state: open
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/7
---

# Linux 调整 Swap 文件大小指南



## 查看当前 Swap 状态

调整前，建议先了解系统当前 swap 的使用情况。

```
sudo swapon --show        # 显示已启用的 swap 空间详细信息
free -h                   # 以人类可读格式显示内存和 swap 使用情况
```

## 调整 Swap 文件大小的步骤

以下是调整 `/swapfile` 大小的具体步骤，主要包括关闭现有交换文件、创建新大小的交换文件并重新启用。

1.  ​**​禁用当前的 swap 文件​**​：  
    调整 swap 文件前，必须先禁用它。
    
    ```
    sudo swapoff -a
    ```
    
2.  ​**​删除现有的 swap 文件​**​（通常为 `/swapfile`）：
    
    ```
    sudo rm /swapfile
    ```
    
3.  ​**​创建新的 swap 文件​**​：  
    使用 `fallocate` 命令创建指定大小的新文件（例如调整为 10G）：
    
    ```
    sudo fallocate -l 10G /swapfile
    ```
    
    ​**​替代方案​**​：如果 `fallocate` 有问题（如在某些文件系统中），可以使用 `dd` 命令，但速度较慢：
    
    ```
    sudo dd if=/dev/zero of=/swapfile bs=1G count=10
    ```
    
4.  ​**​设置正确的文件权限​**​：  
    为确保安全，swap 文件应仅限 root 访问。
    
    ```
    sudo chmod 600 /swapfile
    ```
    
5.  ​**​将文件格式化为 swap 空间​**​：
    
    ```
    sudo mkswap /swapfile
    ```
    
6.  ​**​启用新的 swap 文件​**​：
    
    ```
    sudo swapon /swapfile
    ```
    
7.  ​**​验证新的 swap 是否启用​**​：
    
    ```
    sudo swapon --show
    free -h
    ```
    
    检查输出，确认新大小的 swap 已显示并处于启用状态。
    

## 使调整永久生效

系统重启后，需要确保新的 swap 文件能自动启用。通过编辑 `/etc/fstab` 文件实现。

1.  使用文本编辑器（如 `nano` 或 `vim`）打开 `/etc/fstab` 文件：
    
    ```
    sudo nano /etc/fstab
    ```
    
2.  确保文件中包含以下行（如果已有 swapfile 条目，请修改；如果没有，请添加）：
    
    ```
    /swapfile none swap defaults 0 0
    ```
    
3.  保存并退出编辑器（在 `nano` 中按 `Ctrl+X`，然后按 `Y` 确认，最后按 `Enter`）。
    

## 重要注意事项和建议

+   ​**​操作风险​**​：调整 swap 文件大小需要​**​禁用当前的 swap​**​。如果系统正严重依赖 swap（物理内存几乎用尽），在此期间应用程序可能会因内存不足（OOM）而被终止，操作期间系统响应速度也可能下降。​**​建议在系统负载较低、已保存好所有工作的情况下进行此操作​**​。
+   ​**​磁盘空间​**​：确保你的根文件系统（或目标位置）有足够的​**​可用空间​**​来容纳新大小的 swap 文件。例如，创建 10G 的 swap 文件，就需要至少 10G 的空闲空间。
+   ​**​Swap 大小选择​**​：
    
    +   传统建议是 swap 大小为物理内存的 1 到 2 倍，但这并非绝对。
    +   对于现代拥有大容量内存的系统（如 16G 以上），如果只是为了桌面用途且希望节省磁盘空间，可以设置较小的 swap（如 4G 或更小）。
    +   如果计划使用​**​休眠（Hibernate）​**​ 到磁盘的功能，​**​swap 大小通常需要至少等于甚至大于物理内存大小​**​，以便容纳内存中的所有数据。
    
+   ​**​性能考虑​**​：Swap 位于硬盘上，速度远慢于物理内存。​**​频繁且大量地使用 swap 可能表明物理内存不足​**​，并会导致系统性能下降。如果遇到这种情况，考虑增加物理内存是更根本的解决方法。
+   ​**​SSD 磨损​**​：如果系统使用 SSD，创建 swap 文件可能会因其写入次数有限而​**​影响寿命​**​。但对于现代 SSD 来说，通常无需过度担心，但保持关注是好的做法。

## 🔧 可选后续优化：调整 Swappiness

`swappiness` 参数决定了系统使用 swap 的积极程度（范围 0-100）。值越高，内核越倾向于使用 swap；值越低，则越倾向于尽可能使用物理内存。

+   ​**​查看当前 swappiness 值​**​：
    
    ```
    cat /proc/sys/vm/swappiness
    ```
    
    Linux Mint 或 Ubuntu 的默认值通常是 `60`。
    
+   ​**​临时更改​**​（重启后失效）：
    
    ```
    sudo sysctl vm.swappiness=30
    ```
    
+   ​**​永久更改​**​：
    
    1.  编辑 `/etc/sysctl.conf` 文件：
        
        ```
        sudo nano /etc/sysctl.conf
        ```
        
    2.  在文件末尾添加或修改此行：
        
        ```
        vm.swappiness=30
        ```
        
    3.  保存退出，并使更改生效：
        
        ```
        sudo sysctl -p
        ```
        
    
+   ​**​Swappiness 值参考​**​：
    
    +   ​**​0-10​**​：非常不愿意使用 swap，适用于服务器或内存非常充足的系统。
    +   ​**​30-50​**​：对于多数桌面系统来说是一个比较平衡的值。
    +   ​**​60​**​：默认值。
    +   ​**​80-100​**​：积极使用 swap，通常不建议，除非有特定需求。

