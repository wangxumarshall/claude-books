#!/usr/bin/env python3
"""
ModelArts 研究报告配图生成脚本
生成 4 张出版级配图（matplotlib + APA 7.0 风格、色盲安全调色板）。
依赖: pip install matplotlib numpy
运行: python figures/generate_figures.py
输出: figures/fig1_architecture.png, fig2_e2e_flow.png, fig3_fault_recovery.png, fig4_improvement_priority.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# APA 7.0 风格 + 色盲安全调色板（Okabe-Ito）
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 11,
    'axes.titleweight': 'bold',
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})
OKABE_ITO = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#F0E442', '#56B4E9', '#E69F00']
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- 图 1: ModelArts 三层架构 ----------
def fig1_architecture():
    fig, ax = plt.subplots(figsize=(10, 6))
    layers = [
        ('AI Gallery / 开发者社区\n(模型/API/数据集/案例共享与交易)', OKABE_ITO[4], 0.85),
        ('AI 开发工具链层\nMindSpeed-LLM · MindSpeed · CANN · torch_npu · ATB · HCCL', OKABE_ITO[2], 0.65),
        ('AI 平台层\n数据管理 | 开发环境 | 模型训练 | 推理部署 | 资源管理 | 运维运营\n(公共/专属资源池 · Lite Server/Cluster · Volcano · EYWA)', OKABE_ITO[0], 0.45),
        ('算力层\nAtlas 800T A2 · Ascend 910B/C · 超节点 Snt9b23 · RoCE 200GE\nAtlas 900 A2 PoD/PoDc · CloudMatrix 384 超节点', OKABE_ITO[1], 0.25),
    ]
    for i, (text, color, y) in enumerate(layers):
        box = FancyBboxPatch((0.05, y), 0.9, 0.15, boxstyle="round,pad=0.01",
                             facecolor=color, alpha=0.75, edgecolor='black', linewidth=1.2)
        ax.add_patch(box)
        ax.text(0.5, y + 0.075, text, ha='center', va='center', fontsize=9, weight='bold')
        if i < len(layers) - 1:
            ax.annotate('', xy=(0.5, y), xytext=(0.5, y + 0.15),
                        arrowprops=dict(arrowstyle='<->', lw=1.5, color='gray'))
    ax.set_xlim(0, 1); ax.set_ylim(0.15, 1.05)
    ax.axis('off')
    ax.set_title('Figure 1. ModelArts 三层架构（算力层 → 平台层 → 工具链层 → 开发者社区）', pad=10)
    plt.savefig(f'{DIR}/fig1_architecture.png'); plt.close()

# ---------- 图 2: 端到端训练作业流程 ----------
def fig2_e2e_flow():
    fig, ax = plt.subplots(figsize=(11, 4.5))
    steps = ['资源准备\nVPC/SFS/OBS\n/SWR/资源池', '镜像构建\n基于预置\nARM+Ascend', '数据上传OBS\n算法上传SFS',
             'Notebook\n单机→多机\n调试', '创建训练作业\n亲和组+重启\n+算子重执行', 'DDP启动\nRANK_TABLE\n/torchrun',
             'ranktable路由\n+超节点亲和', '训练运行\nHCCL通信\n+CKPT持久化', '故障恢复\n原地/重调度\n/算子重执行',
             '模型注册→\n推理部署\nvLLM/PD弹性']
    x = np.arange(len(steps))
    colors = [OKABE_ITO[i % len(OKABE_ITO)] for i in range(len(steps))]
    for i, (s, c) in enumerate(zip(steps, colors)):
        box = FancyBboxPatch((i - 0.42, 0.25), 0.84, 0.5, boxstyle="round,pad=0.02",
                             facecolor=c, alpha=0.8, edgecolor='black', lw=1)
        ax.add_patch(box)
        ax.text(i, 0.5, s, ha='center', va='center', fontsize=7.5, weight='bold')
        if i < len(steps) - 1:
            ax.annotate('', xy=(i + 0.42, 0.5), xytext=(i + 0.58, 0.5),
                        arrowprops=dict(arrowstyle='->', lw=1.5, color='#333'))
    ax.set_xlim(-0.6, len(steps) - 0.4); ax.set_ylim(0.1, 0.9)
    ax.axis('off')
    ax.set_title('Figure 2. ModelArts 多机多卡大模型训练作业端到端流程（10 步）', pad=10)
    plt.savefig(f'{DIR}/fig2_e2e_flow.png'); plt.close()

# ---------- 图 3: 故障恢复决策树 ----------
def fig3_fault_recovery():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    nodes = {
        'root': ('故障发生', 0.5, 0.9, OKABE_ITO[5]),
        'link': ('通信链路闪断\n→ 算子重执行\n(秒级, ~95%)', 0.15, 0.55, OKABE_ITO[2]),
        'chip': ('NPU芯片可自愈\n→ 原地恢复\n(分钟级)', 0.5, 0.55, OKABE_ITO[0]),
        'hang': ('作业卡死\n→ 卡死重启\n(保留容器)', 0.85, 0.55, OKABE_ITO[3]),
        'exit': ('异常退出码非0\n→ 无条件Job重调度', 0.85, 0.2, OKABE_ITO[1]),
        'ok': ('自愈成功\n→ 继续', 0.35, 0.2, OKABE_ITO[2]),
        'fail': ('自愈失败/24h×3\n→ 隔离式Job重调度\n(10-30min)', 0.65, 0.2, OKABE_ITO[1]),
    }
    for k, (t, x, y, c) in nodes.items():
        box = FancyBboxPatch((x - 0.13, y - 0.08), 0.26, 0.16, boxstyle="round,pad=0.01",
                             facecolor=c, alpha=0.75, edgecolor='black', lw=1)
        ax.add_patch(box)
        ax.text(x, y, t, ha='center', va='center', fontsize=7.5, weight='bold')
    edges = [('root', 'link'), ('root', 'chip'), ('root', 'hang'), ('root', 'exit'),
             ('chip', 'ok'), ('chip', 'fail')]
    for a, b in edges:
        _, xa, ya, _ = nodes[a]; _, xb, yb, _ = nodes[b]
        ax.annotate('', xy=(xb, yb + 0.08), xytext=(xa, ya - 0.08),
                    arrowprops=dict(arrowstyle='->', lw=1.2, color='#333'))
    ax.set_xlim(0, 1); ax.set_ylim(0.05, 1.0)
    ax.axis('off')
    ax.set_title('Figure 3. ModelArts 多级故障恢复决策树', pad=10)
    plt.savefig(f'{DIR}/fig3_fault_recovery.png'); plt.close()

# ---------- 图 4: 改进方向优先级矩阵（气泡图） ----------
def fig4_improvement_priority():
    fig, ax = plt.subplots(figsize=(9, 6))
    # (名称, 工程投入 1-5, 预期收益 1-5, 战略必要性 1-5, 优先级)
    items = [
        ('§7.1 MoE细粒度重叠', 4.5, 4.5, 4.5, 'P0'),
        ('§7.2 Attention/MoE解耦', 3.0, 3.8, 4.5, 'P0'),
        ('§7.3 动态气泡填充', 4.5, 3.5, 3.0, 'P1'),
        ('§7.4 FP8+跨平台内核', 4.5, 4.5, 4.5, 'P1*'),
        ('§7.5 Ulysses+内存优化', 3.0, 3.8, 3.5, 'P1'),
        ('§7.6 系统级AutoML', 3.0, 2.5, 4.5, 'P2'),
        ('§7.7 生态开放性', 1.5, 2.5, 4.5, 'P0'),
    ]
    pcolors = {'P0': OKABE_ITO[1], 'P1': OKABE_ITO[4], 'P1*': OKABE_ITO[3], 'P2': OKABE_ITO[5]}
    for name, cost, gain, strat, pri in items:
        size = strat * 60
        ax.scatter(cost, gain, s=size, c=pcolors[pri], alpha=0.7, edgecolors='black', linewidth=1)
        ax.annotate(f'{name}\n[{pri}]', (cost, gain), xytext=(8, 8),
                    textcoords='offset points', fontsize=8)
    ax.set_xlabel('工程投入 (1=低, 5=高)')
    ax.set_ylabel('预期吞吐收益 (1=低, 5=高)')
    ax.set_xlim(0.8, 5.2); ax.set_ylim(2.0, 5.2)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=3.5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=3.5, color='gray', linestyle='--', alpha=0.5)
    ax.text(1.0, 5.0, '低投入高收益\n(优先投入区)', fontsize=8, color='green', alpha=0.7)
    ax.text(4.0, 2.2, '高投入低收益\n(谨慎评估)', fontsize=8, color='red', alpha=0.7)
    handles = [mpatches.Patch(color=c, label=f'优先级 {k}') for k, c in pcolors.items()]
    ax.legend(handles=handles, loc='lower right', fontsize=8)
    ax.set_title('Figure 4. ModelArts 改进方向优先级矩阵\n(气泡大小=战略必要性; P1*=受910D量产节奏约束)', pad=10)
    plt.savefig(f'{DIR}/fig4_improvement_priority.png'); plt.close()

if __name__ == '__main__':
    fig1_architecture()
    fig2_e2e_flow()
    fig3_fault_recovery()
    fig4_improvement_priority()
    print("4 figures generated in:", DIR)
