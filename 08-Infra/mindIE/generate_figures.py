"""
MindIE 研究报告配套图表生成代码

依赖: Python 3.9+, matplotlib>=3.5, numpy>=1.21
运行: python generate_figures.py
输出: figures/ 目录下 4 张 PNG (300 dpi, APA 7.0 风格)

图表清单:
  fig1_pd_vs_mixed.png      - PD 分离 vs PD 混部 吞吐对比 (柱状)
  fig2_kv_transfer_time.png - KV Cache 传输时延 vs prompt 长度 (折线)
  fig3_mindie_vs_vllm.png   - MindIE vs vLLM-Ascend TTFT/TPOT 对比 (分组柱状)
  fig4_feature_compat.png   - 特性互斥矩阵热力图

数据来源: 论文参考文献 [2][4][6][22][32]
所有数值均可在论文中找到出处, 未虚构任何数据点。
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ---------- 全局样式: APA 7.0 风格 ----------
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "figure.dpi": 100,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# 色盲友好调色板 (Okabe-Ito)
C_BLUE = "#0072B2"
C_ORANGE = "#E69F00"
C_GREEN = "#009E73"
C_RED = "#D55E00"
C_PURPLE = "#CC79A7"
C_GRAY = "#999999"

OUT_DIR = "figures"
os.makedirs(OUT_DIR, exist_ok=True)


# ============================================================
# 图 1: PD 分离 vs PD 混部 吞吐对比
# 数据来源: 参考文献 [2] - "昇腾PD分离技术...将吞吐量提升了30%以上"
# 仅绘制相对示意 (基线=100, PD分离=130), 不主张绝对倍数
# ============================================================
def fig1_pd_vs_mixed():
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    configs = ["PD 混部\n(基线)", "PD 分离\n(+30%)"]
    # 相对吞吐 (基线=100, PD分离=130), 据 [2] 的相对提升
    relative = [100, 130]

    x = np.arange(len(configs))
    b = ax.bar(x, relative, 0.5, color=[C_BLUE, C_ORANGE])

    for bar in b:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{int(bar.get_height())}", ha="center", va="bottom", fontsize=10)

    ax.set_ylabel("相对吞吐 (基线=100)")
    ax.set_title("Fig. 1  PD 分离 vs PD 混部 相对吞吐示意\n(大规模专家并行场景, 据 [2] 相对提升归一化)")
    ax.set_xticks(x)
    ax.set_xticklabels(configs)
    ax.set_ylim(0, 150)
    ax.axhline(100, color=C_GRAY, ls=":", lw=0.8)
    ax.annotate("+30%", xy=(1, 130), xytext=(0.5, 145),
                arrowprops=dict(arrowstyle="->", color=C_RED), color=C_RED, fontsize=9)
    fig.savefig(f"{OUT_DIR}/fig1_pd_vs_mixed.png")
    plt.close(fig)


# ============================================================
# 图 2: KV Cache 传输时延 vs prompt 长度
# 数据来源: 论文 5.5 节带宽建模公式 + 参考文献 [6] (200 Gbps)
# 模型: Qwen2-72B (80层, 8 KV head, head_dim 128, fp16)
# ============================================================
def fig2_kv_transfer_time():
    L = np.array([1024, 2048, 4096, 8192, 16384, 32768, 65536])  # prompt 长度
    n_layer, n_kv_head, head_dim, dtype_bytes = 80, 8, 128, 2
    # KV Cache 体量 (GB): V = 2 * L * n_layer * n_kv_head * head_dim * dtype_bytes
    V_gb = 2 * L * n_layer * n_kv_head * head_dim * dtype_bytes / 1e9
    # 传输时延 (ms): 200 Gbps = 25 GB/s = 25e-3 GB/ms
    bw_gb_per_ms = 25e-3
    t_ms = V_gb / bw_gb_per_ms

    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(L, t_ms, marker="o", color=C_BLUE, lw=2, ms=5)
    ax.fill_between(L, t_ms * 0.8, t_ms * 1.2, color=C_BLUE, alpha=0.15,
                    label="±20% 带宽波动区间")

    # 标注关键点
    for li, ti in zip([4096, 32768, 65536], [t_ms[2], t_ms[5], t_ms[6]]):
        ax.annotate(f"{ti:.0f}ms", (li, ti), textcoords="offset points",
                    xytext=(8, 8), fontsize=8, color=C_RED)

    ax.set_xlabel("Prompt 长度 (tokens)")
    ax.set_ylabel("单请求 KV 传输时延 (ms)")
    ax.set_title("Fig. 2  P→D KV Cache 传输时延 vs Prompt 长度\n(Qwen2-72B, 200 Gbps 链路, 据 [6] 建模)")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(10, 1e5)
    ax.legend(frameon=False, loc="upper left")
    ax.grid(True, which="both", ls=":", lw=0.4, alpha=0.5)
    fig.savefig(f"{OUT_DIR}/fig2_kv_transfer_time.png")
    plt.close(fig)


# ============================================================
# 图 3: MindIE vs vLLM-Ascend 性能对比
# 数据来源: 参考文献 [32] issue#4395 实测
# Qwen3-235B-int8, 单机8卡, 16并发
# ============================================================
def fig3_mindie_vs_vllm():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8))

    # 子图 A: TTFT (秒, 越低越好)
    ax = axes[0]
    inputs = ["2K 输入", "8K 输入", "64K 输入"]
    vllm_ttft = [1.3, 3.5, 22.0]
    mindie_ttft = [2.9, 12.0, 39.0]
    x = np.arange(len(inputs))
    w = 0.36
    ax.bar(x - w/2, vllm_ttft, w, label="vLLM-Ascend", color=C_ORANGE)
    ax.bar(x + w/2, mindie_ttft, w, label="MindIE", color=C_BLUE)
    for i, (v, m) in enumerate(zip(vllm_ttft, mindie_ttft)):
        ax.text(i - w/2, v + 0.5, f"{v}", ha="center", fontsize=8)
        ax.text(i + w/2, m + 0.5, f"{m}", ha="center", fontsize=8)
    ax.set_ylabel("TTFT (秒, 越低越好)")
    ax.set_title("A. 首 Token 时延 (TTFT)")
    ax.set_xticks(x)
    ax.set_xticklabels(inputs)
    ax.legend(frameon=False)
    ax.set_ylim(0, 45)

    # 子图 B: 输出速度 (tok/s, 越高越好)
    ax = axes[1]
    vllm_tps = [14, 12, 8]      # 1000/tpot 反算
    mindie_tps = [20, 19, 9]
    ax.bar(x - w/2, vllm_tps, w, label="vLLM-Ascend", color=C_ORANGE)
    ax.bar(x + w/2, mindie_tps, w, label="MindIE", color=C_BLUE)
    for i, (v, m) in enumerate(zip(vllm_tps, mindie_tps)):
        ax.text(i - w/2, v + 0.3, f"{v}", ha="center", fontsize=8)
        ax.text(i + w/2, m + 0.3, f"{m}", ha="center", fontsize=8)
    ax.set_ylabel("输出速度 (tok/s, 越高越好)")
    ax.set_title("B. Decode 输出速度")
    ax.set_xticks(x)
    ax.set_xticklabels(inputs)
    ax.legend(frameon=False)
    ax.set_ylim(0, 24)

    fig.suptitle("Fig. 3  MindIE vs vLLM-Ascend 性能对比\n(Qwen3-235B-int8, 单机8卡, 16并发, 数据据 [32])",
                 fontsize=11, fontweight="bold", y=1.05)
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/fig3_mindie_vs_vllm.png")
    plt.close(fig)


# ============================================================
# 图 4: 特性互斥矩阵热力图
# 数据来源: 参考文献 [20] 特性总览 + 论文第 3.3/5.3/5.5 节互斥约束
# 1=兼容, 0=互斥, 0.5=部分/条件兼容
# ============================================================
def fig4_feature_compat():
    features = ["PD分离", "PrefixCache", "Multi-LoRA", "SplitFuse", "并行解码",
                "MTP", "ContextParallel", "KV int8", "稀疏量化", "FlashDecoding"]
    n = len(features)
    # 对称矩阵; 对角线 = 1 (自兼容)
    M = np.full((n, n), 1.0)
    # 互斥对 (据论文 3.3/5.5 节)
    def set_mutual(i, j, val=0.0):
        M[i, j] = val
        M[j, i] = val
    # PD分离 vs PrefixCache/MultiLoRA/SplitFuse/并行解码/稀疏量化/KVint8
    pd = 0
    for j, name in enumerate(features):
        if name in ("PrefixCache", "Multi-LoRA", "SplitFuse", "并行解码",
                    "稀疏量化", "KV int8"):
            set_mutual(pd, j)
    # MTP vs 长序列(ContextParallel 在 128K 场景) - 部分兼容
    mtp = features.index("MTP")
    cp = features.index("ContextParallel")
    set_mutual(mtp, cp, 0.5)
    # 稀疏量化 vs KV int8
    set_mutual(features.index("稀疏量化"), features.index("KV int8"))
    # 对角线
    np.fill_diagonal(M, 1.0)

    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    cmap = mpl.colors.ListedColormap([C_RED, C_ORANGE, C_GREEN])
    bounds = [-0.5, 0.5, 0.5, 1.5]  # 0 / 0.5 / 1
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="equal")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(features, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(features, fontsize=9)
    ax.set_title("Fig. 4  MindIE LLM 特性互斥矩阵\n(绿=兼容, 橙=部分/条件, 红=互斥; 据 [20] 及论文 §3.3/§5.5)")

    # 图例
    from matplotlib.patches import Patch
    legend = [Patch(facecolor=C_GREEN, label="兼容"),
              Patch(facecolor=C_ORANGE, label="部分/条件"),
              Patch(facecolor=C_RED, label="互斥")]
    ax.legend(handles=legend, loc="upper right", bbox_to_anchor=(1.0, -0.15),
              ncol=3, frameon=False)

    # 标注非对角 0 值
    for i in range(n):
        for j in range(n):
            if i != j and M[i, j] == 0:
                ax.text(j, i, "×", ha="center", va="center", color="white",
                        fontsize=11, fontweight="bold")
            elif i != j and M[i, j] == 0.5:
                ax.text(j, i, "≈", ha="center", va="center", color="white",
                        fontsize=11, fontweight="bold")

    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/fig4_feature_compat.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1_pd_vs_mixed()
    fig2_kv_transfer_time()
    fig3_mindie_vs_vllm()
    fig4_feature_compat()
    print(f"已生成 4 张图表至 {OUT_DIR}/ 目录:")
    for f in sorted(os.listdir(OUT_DIR)):
        print(f"  {OUT_DIR}/{f}")
