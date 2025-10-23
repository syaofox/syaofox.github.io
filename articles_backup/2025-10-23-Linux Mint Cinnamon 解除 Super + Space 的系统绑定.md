---
title: "Linux Mint Cinnamon 解除 Super + Space 的系统绑定"
created_at: "2025-10-23 10:17:49"
updated_at: "2025-10-23 10:17:49"
issue_number: 49
labels: ['tips']
url: https://github.com/syaofox/syaofox.github.io/issues/49
---

# Linux Mint Cinnamon 解除 Super + Space 的系统绑定

如果 **Linux Mint Cinnamon** 系统不允许将 **$\text{Super} + \text{Space}$** 绑定为自定义快捷键，这通常是因为该组合键已经被系统默认用于**切换输入法/键盘布局**。

在 Cinnamon 中，你需要先解除或更改这个默认的系统绑定，然后才能将其用于自定义命令（如启动 `rofi`）。

请尝试按照以下步骤操作：

### 步骤一：解除或更改默认的 $\text{Super} + \text{Space}$ 绑定

1.  **打开系统设置 (System Settings)**：

      * 菜单 $\to$ 系统设置。

2.  **进入键盘设置 (Keyboard)**：

      * 在“系统设置”中点击 **键盘 (Keyboard)**。

3.  **进入布局选项卡 (Layouts Tab)**：

      * 切换到 **布局 (Layouts)** 选项卡。

4.  **打开选项 (Options)**：

      * 点击右下角的 **选项 (Options)** 按钮。

5.  **查找切换布局的快捷键**：

      * 在弹出的“键盘布局选项”窗口中，展开 **切换到另一个布局 (Switching to another layout)**。
      * 你会看到默认的快捷键设置，其中很可能勾选了 **$\text{Super} + \text{Space}$** 或类似的组合键。

6.  **解除绑定**：

      * **取消勾选** $\text{Super} + \text{Space}$（或任何你希望用于 $\text{rofi}$ 的键）。
      * 或者，如果你需要切换布局的功能，**选择一个不同的组合键**，例如 $\text{Alt} + \text{Shift}$ 或 $\text{Ctrl} + \text{Super} + \text{Space}$。

7.  **应用更改**：

      * 关闭“键盘布局选项”窗口。

### 步骤二：重新绑定 Rofi 快捷键

在解除默认冲突后，你可以回到自定义快捷键的设置中。

1.  **回到快捷键选项卡 (Shortcuts Tab)**：

      * 在“键盘”设置窗口中，切换回 **快捷键 (Shortcuts)** 选项卡。

2.  **找到你的 Rofi 条目**：

      * 在左侧选择 **自定义快捷键 (Custom Shortcuts)**。
      * 找到你之前创建的 `启动 Rofi (drun)` 条目。

3.  **设置快捷键**：

      * 点击右侧的快捷键区域。
      * 再次按下 **$\text{Super} + \text{Space}$**。
      * 这次系统应该会接受这个组合键。

**命令回顾：**
如果你在步骤一中仍遇到问题，你可以尝试使用更健壮的命令，确保 $\text{rofi}$ 能顺利执行：

```bash
bash -c "rofi -show drun -config $HOME/dwm-mint/dotfiles/rofi.rasi"
```

