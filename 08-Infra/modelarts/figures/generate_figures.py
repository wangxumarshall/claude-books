#!/usr/bin/env python3
"""ModelArts V2.0 Research Report - Figure Generation Script
APA7 Style, Okabe-Ito Colorblind-Safe Palette
Generates 7 figures for the research report (English-only labels for font compatibility).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
import os

COLORS = {
    'black': '#000000',
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'bluish_green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'reddish_purple': '#CC79A7',
    'light_gray': '#CCCCCC',
    'dark_gray': '#666666'
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Liberation Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
})

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_box(ax, x, y, width, height, text, color, text_color='white', fontsize=9, alpha=1.0):
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.02",
                         facecolor=color, edgecolor='black',
                         linewidth=1.2, alpha=alpha)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
            ha='center', va='center', color=text_color,
            fontsize=fontsize, fontweight='bold', wrap=True)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color='black', style='->', linewidth=1.5, connectionstyle=None):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style, color=color,
                            linewidth=linewidth, mutation_scale=15,
                            connectionstyle=connectionstyle)
    ax.add_patch(arrow)
    return arrow


def fig1_three_layer_architecture():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 1. ModelArts V2.0 Three-Layer Technical Architecture',
                 fontsize=12, fontweight='bold', pad=20)

    draw_box(ax, 0.5, 7.5, 9, 2, 'Toolchain Layer', COLORS['blue'], fontsize=11)
    toolchain_items = [
        'MindSpeed-LLM', 'MindSpeed-MM', 'CANN 9.x',
        'torch_npu', 'MindSpore', 'vLLM-Ascend',
        'AscendCL', 'MoXing API', 'ATB Boost'
    ]
    for i, item in enumerate(toolchain_items):
        col = i % 3
        row = i // 3
        x = 1 + col * 3
        y = 7.8 + (1 - row) * 0.55
        draw_box(ax, x, y, 2.5, 0.45, item, COLORS['sky_blue'], text_color='black', fontsize=8)

    draw_box(ax, 0.5, 4.5, 9, 2.5, 'Platform Layer', COLORS['bluish_green'], fontsize=11)
    platform_items = [
        'Volcano Scheduler\n(Gang/DRF/Preempt)', 'EYWA DAG\nProvenance', 'Ascend Device Plugin',
        'ModelArts Console', 'Training Jobs', 'Notebook Dev',
        'Model Registry', 'Inference Services', 'Monitoring & Logging'
    ]
    for i, item in enumerate(platform_items):
        col = i % 3
        row = i // 3
        x = 1 + col * 3
        y = 4.7 + (1 - row) * 0.6
        draw_box(ax, x, y, 2.5, 0.5, item, COLORS['yellow'], text_color='black', fontsize=7)

    draw_box(ax, 0.5, 1.5, 9, 2.5, 'Compute Layer', COLORS['vermillion'], fontsize=11)
    compute_items = [
        'Ascend 910B/C/D\nNPUs', 'HCCS 50GB/s\nInterconnect', 'RoCE v2 400GE\nLeaf-Spine',
        'CloudMatrix 384\nSuperNode', 'Kunpeng 920\nCPUs', 'NVMe SSD\nStorage',
        'OBS Object Store', 'SFS Turbo\nParallel FS', 'Liquid Cooling'
    ]
    for i, item in enumerate(compute_items):
        col = i % 3
        row = i // 3
        x = 1 + col * 3
        y = 1.7 + (1 - row) * 0.6
        draw_box(ax, x, y, 2.5, 0.5, item, COLORS['orange'], text_color='black', fontsize=7)

    draw_arrow(ax, 5, 7.5, 5, 7.0, color=COLORS['dark_gray'], linewidth=2)
    draw_arrow(ax, 5, 4.5, 5, 4.0, color=COLORS['dark_gray'], linewidth=2)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_three_layer_architecture.png'), dpi=300)
    plt.close()
    print("Generated fig1_three_layer_architecture.png")


def fig2_end_to_end_workflow():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 2. ModelArts V2.0 End-to-End 10-Step Cluster Workflow',
                 fontsize=12, fontweight='bold', pad=20)

    steps = [
        ('1. Resource\nPreparation', COLORS['blue']),
        ('2. Custom\nImage Build', COLORS['sky_blue']),
        ('3. OBS Dataset\nPreparation', COLORS['bluish_green']),
        ('4. Training\nScript Dev', COLORS['yellow']),
        ('5. Resource\nPool Config', COLORS['orange']),
        ('6. Job Submission\n(YAML/Console)', COLORS['vermillion']),
        ('7. Volcano\nScheduling', COLORS['reddish_purple']),
        ('8. Distributed\nTraining', COLORS['blue']),
        ('9. Monitoring\n& Self-Healing', COLORS['sky_blue']),
        ('10. Model Export\n& Deployment', COLORS['bluish_green']),
    ]

    box_w = 2
    box_h = 1.2
    positions = []
    for i, (text, color) in enumerate(steps):
        if i < 5:
            x = 0.8 + i * 2.2
            y = 7.5
        else:
            x = 0.8 + (9 - i) * 2.2
            y = 4.5
        positions.append((x, y))
        draw_box(ax, x, y, box_w, box_h, text, color, fontsize=8)

    for i in range(4):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        draw_arrow(ax, x1 + box_w, y1 + box_h/2, x2, y2 + box_h/2, COLORS['black'])
    for i in range(5, 9):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        draw_arrow(ax, x1 + box_w, y1 + box_h/2, x2, y2 + box_h/2, COLORS['black'])

    draw_arrow(ax, positions[4][0] + box_w/2, positions[4][1],
               positions[5][0] + box_w/2, positions[5][1] + box_h,
               COLORS['dark_gray'], linewidth=2)
    draw_arrow(ax, positions[8][0] + box_w/2, positions[8][1],
               positions[3][0] + box_w/2, positions[3][1] + box_h,
               COLORS['vermillion'], style='->', linewidth=1.5)

    ax.text(6, 6.2, 'Iteration /\nHyperparameter Tuning', ha='center', va='center',
            fontsize=8, color=COLORS['vermillion'], fontweight='bold',
            bbox=dict(facecolor='white', edgecolor=COLORS['vermillion'], boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_end_to_end_workflow.png'), dpi=300)
    plt.close()
    print("Generated fig2_end_to_end_workflow.png")


def fig3_fault_recovery_statemachine():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 3. ModelArts V2.0 Five-Level Fault Recovery State Machine',
                 fontsize=12, fontweight='bold', pad=20)

    states = [
        ('Normal\nExecution', 5, 9, COLORS['bluish_green']),
        ('L1: Op Re-exec\n<3s, Link Flap', 5, 7.2, COLORS['yellow']),
        ('L2: In-Place Recovery\n<5min, HCCL Timeout', 5, 5.4, COLORS['orange']),
        ('L3: Task Retry\n<10min, Process Crash', 5, 3.6, COLORS['vermillion']),
        ('L4: Job Resched\n<30min, Node Failure', 3, 1.8, COLORS['reddish_purple']),
        ('L5: Node Isolation\n>30min, HW Fault', 7, 1.8, COLORS['blue']),
    ]

    circles = []
    for text, x, y, color in states:
        circle = Circle((x, y), 0.75, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=7,
                fontweight='bold', color='black', wrap=True)
        circles.append((x, y))

    ax.text(6.8, 9.3, 'Healthy', ha='left', va='center', fontsize=8, color=COLORS['bluish_green'])
    draw_arrow(ax, 6.8, 9.3, 5.8, 9, color=COLORS['bluish_green'], linewidth=1.5)

    for i in range(4):
        x1, y1 = circles[i]
        if i < 3:
            x2, y2 = circles[i + 1]
            draw_arrow(ax, x1, y1 - 0.75, x2, y2 + 0.75, COLORS['vermillion'], linewidth=1.5)
        else:
            draw_arrow(ax, x1, y1 - 0.75, 3, 2.55, COLORS['vermillion'], linewidth=1.5)
        ax.text(x1 + 0.3, (y1 + (circles[i+1][1] if i < 3 else 2.55))/2, 'Fault\nEscalation',
                ha='left', va='center', fontsize=7, color=COLORS['vermillion'])

    draw_arrow(ax, 3.75, 1.05, 6.25, 1.05, COLORS['blue'], linewidth=1.5)
    ax.text(5, 0.5, 'Bad Node Blacklist / Correlation Analysis',
            ha='center', va='center', fontsize=8, color=COLORS['blue'])

    for i in range(4):
        x1, y1 = circles[i + 1]
        x2, y2 = circles[i]
        if i < 3:
            draw_arrow(ax, x1 - 0.75, y1, x2 - 0.75, y2, COLORS['bluish_green'], linewidth=1.2,
                       connectionstyle="arc3,rad=0.3")
        else:
            draw_arrow(ax, 2.25, 1.8, 4.25, 8.25, COLORS['bluish_green'], linewidth=1.2,
                       connectionstyle="arc3,rad=-0.3")
        ax.text(x1 - 1.5, y1, 'Recovered', ha='right', va='center',
                fontsize=7, color=COLORS['bluish_green'])

    fault_codes = [
        'EZ0001-EZ0005: HCCL Timeout',
        'EZ3001/EZ3002: AICore Error',
        'EZ6001-EZ6003: OOM Error',
        'EZ5001-EZ5002: Driver/NPU Fault',
        'E9999: Fatal Error',
    ]
    for i, code in enumerate(fault_codes):
        ax.text(0.3, 8.5 - i * 0.4, code, ha='left', va='center', fontsize=7,
                color=COLORS['dark_gray'], family='monospace')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig3_fault_recovery_statemachine.png'), dpi=300)
    plt.close()
    print("Generated fig3_fault_recovery_statemachine.png")


def fig4_improvement_priority_matrix():
    fig, ax = plt.subplots(figsize=(10, 8))

    improvements = [
        ('MoE Comm Overlap', 4.5, 2, 800, COLORS['vermillion'], 'M1'),
        ('Attn/MoE Decouple', 4, 2.5, 700, COLORS['orange'], 'M2'),
        ('Dynamic Bubble', 3.5, 3, 500, COLORS['yellow'], 'M3'),
        ('FP8 Training', 5, 3.5, 900, COLORS['bluish_green'], 'M4'),
        ('Ulysses Long-Ctx', 4, 4, 600, COLORS['sky_blue'], 'M5'),
        ('AutoML Parallel', 3, 4.5, 400, COLORS['blue'], 'M6'),
        ('Ecosystem Open', 2.5, 5, 300, COLORS['reddish_purple'], 'M7'),
    ]

    for name, impact, effort, size, color, short in improvements:
        ax.scatter(effort, impact, s=size, c=color, alpha=0.7, edgecolors='black', linewidth=1.5, zorder=5)
        ax.annotate(short, (effort, impact), ha='center', va='center',
                    fontsize=9, fontweight='bold', zorder=6)

    ax.axhline(y=3.5, color=COLORS['dark_gray'], linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=3, color=COLORS['dark_gray'], linestyle='--', linewidth=1, alpha=0.7)

    ax.text(1.5, 4.75, 'Quick Wins\n(High Impact, Low Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['bluish_green'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['bluish_green'], alpha=0.1, boxstyle='round,pad=0.5'))
    ax.text(4.5, 4.75, 'Strategic Projects\n(High Impact, High Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['vermillion'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['vermillion'], alpha=0.1, boxstyle='round,pad=0.5'))
    ax.text(1.5, 2, 'Fill-Ins\n(Low Impact, Low Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['yellow'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['yellow'], alpha=0.1, boxstyle='round,pad=0.5'))
    ax.text(4.5, 2, 'Avoid\n(Low Impact, High Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['dark_gray'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['dark_gray'], alpha=0.1, boxstyle='round,pad=0.5'))

    for size, label in [(300, 'Low'), (600, 'Medium'), (900, 'High')]:
        ax.scatter([], [], s=size, c=COLORS['light_gray'], edgecolors='black', label=label)
    ax.legend(loc='lower left', title='Implementation Value', title_fontsize=9, fontsize=8)

    legend_text = '\n'.join([f'{short}: {name}' for name, _, _, _, _, short in improvements])
    ax.text(0.02, 0.02, legend_text, transform=ax.transAxes, fontsize=7,
            verticalalignment='bottom', family='monospace',
            bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.5'))

    ax.set_xlabel('Implementation Effort (1-5, Low->High)', fontweight='bold')
    ax.set_ylabel('Performance Impact (1-5, Low->High)', fontweight='bold')
    ax.set_title('Figure 4. Improvement Priority Matrix (Bubble Size = User Value)',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xlim(1, 5.5)
    ax.set_ylim(1, 5.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig4_improvement_priority_matrix.png'), dpi=300)
    plt.close()
    print("Generated fig4_improvement_priority_matrix.png")


def fig5_volcano_scheduler():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Figure 5. Volcano Scheduler Pipeline in ModelArts',
                 fontsize=12, fontweight='bold', pad=20)

    components = [
        ('User\n(Console/CLI/YAML)', 0.8, 6.5, COLORS['blue']),
        ('ModelArts\nAPI Server', 2.8, 6.5, COLORS['sky_blue']),
        ('Volcano Job\nController', 4.8, 6.5, COLORS['bluish_green']),
        ('Volcano\nScheduler', 6.8, 6.5, COLORS['yellow']),
        ('Kubernetes\nAPI Server', 8.8, 6.5, COLORS['orange']),
        ('Ascend Plugin\n+ Kubelet', 10.8, 6.5, COLORS['vermillion']),
    ]

    box_w = 1.5
    box_h = 1.2
    for name, x, y, color in components:
        draw_box(ax, x - box_w/2, y - box_h/2, box_w, box_h, name, color, fontsize=8)

    for i in range(len(components) - 1):
        x1 = components[i][1] + box_w/2 - 0.1
        x2 = components[i+1][1] - box_w/2 + 0.1
        y = components[i][2]
        draw_arrow(ax, x1, y, x2, y, COLORS['black'], linewidth=2)

    plugins = [
        ('Gang Scheduling\n(all-or-nothing)', 2.5, 3.5),
        ('DRF\n(Fairness)', 4.5, 3.5),
        ('Preemption\n(Priority)', 6.5, 3.5),
        ('Binpack\n(Capacity Opt)', 8.5, 3.5),
        ('NPU Topology-Aware\n(Ranktable)', 10.5, 3.5),
    ]
    for name, x, y in plugins:
        draw_box(ax, x - 1.1, y - 0.5, 2.2, 1, name, COLORS['light_gray'],
                 text_color='black', fontsize=7)

    for _, x, y in plugins:
        draw_arrow(ax, x, 6.5 - box_h/2, x, y + 0.5, COLORS['dark_gray'], linewidth=1.2)
        draw_arrow(ax, x, y + 0.5, x, 6.5 - box_h/2, COLORS['bluish_green'], linewidth=1.2)

    ax.text(6, 2.2, 'Scheduling Plugins', ha='center', va='center',
            fontsize=10, fontweight='bold', color=COLORS['dark_gray'],
            bbox=dict(facecolor='white', edgecolor=COLORS['dark_gray'], boxstyle='round,pad=0.3'))

    k8s_resources = ('Pods / NPU Claims / ConfigMaps / PVCs', 6.8, 1)
    draw_box(ax, 4, k8s_resources[2] - 0.3, 5.6, 0.6, k8s_resources[0],
             COLORS['light_gray'], text_color='black', fontsize=8)
    draw_arrow(ax, k8s_resources[1], 3.5 - 0.5, k8s_resources[1], k8s_resources[2] + 0.3,
               COLORS['dark_gray'], linewidth=1.2)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig5_volcano_scheduler.png'), dpi=300)
    plt.close()
    print("Generated fig5_volcano_scheduler.png")


def fig6_snt9b23_topology():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    ax1.set_xlim(0, 7)
    ax1.set_ylim(0, 7)
    ax1.axis('off')
    ax1.set_title('(a) Snt9b23 SuperNode 8-Card Mesh Topology',
                  fontsize=11, fontweight='bold', pad=15)

    npu_positions = []
    for row in range(2):
        for col in range(4):
            x = 1.2 + col * 1.3
            y = 5 - row * 2
            npu_positions.append((x, y))
            circle = Circle((x, y), 0.45, facecolor=COLORS['orange'],
                            edgecolor='black', linewidth=1.5)
            ax1.add_patch(circle)
            ax1.text(x, y, f'NPU\n{row*4+col}', ha='center', va='center',
                     fontsize=8, fontweight='bold')

    for i in range(4):
        for j in range(i + 1, 4):
            x1, y1 = npu_positions[i]
            x2, y2 = npu_positions[j]
            ax1.plot([x1, x2], [y1, y2], color=COLORS['vermillion'], linewidth=1.5, alpha=0.6)
            x1, y1 = npu_positions[i + 4]
            x2, y2 = npu_positions[j + 4]
            ax1.plot([x1, x2], [y1, y2], color=COLORS['vermillion'], linewidth=1.5, alpha=0.6)

    for i in range(4):
        x1, y1 = npu_positions[i]
        x2, y2 = npu_positions[i + 4]
        ax1.plot([x1, x2], [y1, y2], color=COLORS['bluish_green'], linewidth=2, alpha=0.8)

    hccs_patch = mpatches.Patch(color=COLORS['vermillion'], alpha=0.6, label='HCCS 50GB/s (Intra-Row Mesh)')
    cross_patch = mpatches.Patch(color=COLORS['bluish_green'], alpha=0.8, label='HCCS (Inter-Row)')
    ax1.legend(handles=[hccs_patch, cross_patch], loc='lower center', fontsize=8)

    ax1.text(3.5, 0.5, 'RoCE v2 400Gbps (Inter-Node)', ha='center', va='center',
             fontsize=9, color=COLORS['blue'], fontweight='bold',
             bbox=dict(facecolor=COLORS['sky_blue'], alpha=0.2, boxstyle='round,pad=0.3'))

    ax2.set_xlim(0, 7)
    ax2.set_ylim(0, 7)
    ax2.axis('off')
    ax2.set_title('(b) HCCL Communication Algorithms',
                  fontsize=11, fontweight='bold', pad=15)

    ax2.text(1.75, 6.2, 'Ring AllReduce', ha='center', va='center',
             fontsize=9, fontweight='bold', color=COLORS['blue'])
    ring_pos = [(1, 5), (2.5, 5.3), (3.2, 4.3), (2.2, 3.5), (0.8, 4)]
    for i, (x, y) in enumerate(ring_pos):
        circle = Circle((x, y), 0.3, facecolor=COLORS['sky_blue'], edgecolor='black')
        ax2.add_patch(circle)
        ax2.text(x, y, str(i), ha='center', va='center', fontsize=8, fontweight='bold')
    for i in range(len(ring_pos)):
        x1, y1 = ring_pos[i]
        x2, y2 = ring_pos[(i + 1) % len(ring_pos)]
        draw_arrow(ax2, x1, y1, x2, y2, COLORS['blue'], linewidth=1.2)
    ax2.text(1.75, 2.8, 'Bandwidth Optimal\nLatency: 2(N-1) steps', ha='center', va='center',
             fontsize=7, color=COLORS['dark_gray'])

    ax2.text(5.25, 6.2, 'Tree AllReduce (Recursive Halving/Doubling)', ha='center', va='center',
             fontsize=9, fontweight='bold', color=COLORS['vermillion'])
    tree_pos = {
        'root': (5.25, 5.2),
        'l1': (4, 4.2), 'r1': (6.5, 4.2),
        'l2l': (3.2, 3.2), 'l2r': (4.8, 3.2), 'r2l': (5.7, 3.2), 'r2r': (7.3, 3.2)
    }
    all_nodes = list(tree_pos.values())
    labels = ['R', '0', '1', '00', '01', '10', '11']
    colors_list = [COLORS['vermillion']] + [COLORS['orange']] * 2 + [COLORS['yellow']] * 4
    for i, (pos, label, color) in enumerate(zip(all_nodes, labels, colors_list)):
        circle = Circle(pos, 0.25, facecolor=color, edgecolor='black')
        ax2.add_patch(circle)
        ax2.text(pos[0], pos[1], label, ha='center', va='center', fontsize=7, fontweight='bold')

    edges = [('root', 'l1'), ('root', 'r1'), ('l1', 'l2l'), ('l1', 'l2r'), ('r1', 'r2l'), ('r1', 'r2r')]
    for parent, child in edges:
        draw_arrow(ax2, tree_pos[parent][0], tree_pos[parent][1] - 0.25,
                   tree_pos[child][0], tree_pos[child][1] + 0.25, COLORS['vermillion'], linewidth=1.2)
    ax2.text(5.25, 2.5, 'Latency Optimal\nLatency: 2log(N) steps', ha='center', va='center',
             fontsize=7, color=COLORS['dark_gray'])

    ax2.text(3.5, 1.5, 'Hierarchical Ring-Tree Hybrid\n(Intra-Node: Ring, Inter-Node: Tree/Ring)',
             ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLORS['bluish_green'],
             bbox=dict(facecolor=COLORS['bluish_green'], alpha=0.1, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig6_snt9b23_topology.png'), dpi=300)
    plt.close()
    print("Generated fig6_snt9b23_topology.png")


def fig7_mindspeed_vs_megatron():
    fig, ax = plt.subplots(figsize=(12, 7))

    categories = [
        'Training\nThroughput',
        'NPU\nUtilization',
        'CKPT Save\nSpeed',
        'Startup\nTime',
        'Fault MTTR',
        'Ecosystem\nCompat',
        'Operator\nCoverage',
        'FP8 Support'
    ]

    mindspeed_scores = [9.2, 8.8, 3.5, 4.8, 3.2, 6.5, 8.5, 9.0]
    megatron_scores = [6.5, 6.0, 6.8, 7.2, 7.5, 9.5, 7.0, 5.5]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, mindspeed_scores, width, label='MindSpeed-LLM (Ascend)',
                   color=COLORS['vermillion'], edgecolor='black', linewidth=1, alpha=0.85)
    bars2 = ax.bar(x + width/2, megatron_scores, width, label='Megatron-Core (Reference)',
                   color=COLORS['blue'], edgecolor='black', linewidth=1, alpha=0.85)

    ax.set_ylabel('Normalized Score (1-10)', fontweight='bold')
    ax.set_title('Figure 7. MindSpeed-LLM vs Megatron-Core on Ascend 910B',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.legend(fontsize=10, loc='upper right')
    ax.set_ylim(0, 11)
    ax.grid(axis='y', alpha=0.3)

    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.text(0.02, 0.98, '* Lower-is-better metrics (CKPT/Startup/MTTR) inverted for comparison\n* Qwen2-72B, 32 nodes 256x910B, seq_len=4096 (illustrative scores)',
            transform=ax.transAxes, fontsize=7.5, va='top',
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig7_mindspeed_vs_megatron.png'), dpi=300)
    plt.close()
    print("Generated fig7_mindspeed_vs_megatron.png")


def main():
    print("Generating ModelArts V2.0 Research Report Figures...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 60)

    fig1_three_layer_architecture()
    fig2_end_to_end_workflow()
    fig3_fault_recovery_statemachine()
    fig4_improvement_priority_matrix()
    fig5_volcano_scheduler()
    fig6_snt9b23_topology()
    fig7_mindspeed_vs_megatron()

    print("-" * 60)
    print("All 7 figures generated successfully!")
    print("\nFigure summary:")
    for i, name in enumerate([
        'three_layer_architecture',
        'end_to_end_workflow',
        'fault_recovery_statemachine',
        'improvement_priority_matrix',
        'volcano_scheduler',
        'snt9b23_topology',
        'mindspeed_vs_megatron'
    ], 1):
        print(f"  fig{i}_{name}.png")


if __name__ == '__main__':
    main()
