# Pygame 安装指南

由于网络问题，直接使用 `pip install pygame` 可能会失败。以下是几种替代安装方法：

## 方法 1: 使用国内镜像源安装
```bash
pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 方法 2: 下载预编译的wheel文件
1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
2. 根据你的Python版本和系统架构下载对应的 .whl 文件
3. 使用以下命令安装：
```bash
pip install 下载的文件名.whl
```

## 方法 3: 使用 Conda (如果已安装 Anaconda 或 Miniconda)
```bash
conda install pygame
```

## 方法 4: 离线安装依赖包
如果以上方法都失败，你可能需要下载所有必要的依赖：
- Python (确保版本兼容)
- Microsoft C++ Build Tools (Windows)
- SDL2 库文件

## 安装成功后运行游戏
```bash
cd D:\AI\Qwen\Tetris
python tetris_game.py
```

## 游戏控制说明
- 方向键 ← → : 左右移动
- 方向键 ↑ : 旋转方块
- 方向键 ↓ : 软降 (加速下落)
- 空格键 : 硬降 (立即到底)
- P 键 : 暂停/继续
- R 键 : 重新开始

游戏包含所有经典俄罗斯方块功能：7种方块类型、消行、计分系统、关卡递增、下落速度加快等。