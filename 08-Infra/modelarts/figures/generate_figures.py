#!/usr/bin/env python3
"""ModelArts V2.0 Research Report - Figure Generation Script
APA7 Style, Okabe-Ito Colorblind-Safe Palette
Generates 7 figures for the research report.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
import os

# Okabe-Ito Colorblind-Safe Palette (APA7 compliant)
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

# APA7 Style Configuration
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
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
    """Draw a rounded rectangle with text."""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.02",
                         facecolor=color,
                         edgecolor='black',
                         linewidth=1.2,
                         alpha=alpha)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
            ha='center', va='center',
            color=text_color, fontsize=fontsize,
            fontweight='bold', wrap=True)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color='black', style='->', linewidth=1.5):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style,
                            color=color,
                            linewidth=linewidth,
                            mutation_scale=15)
    ax.add_patch(arrow)
    return arrow


def fig1_three_layer_architecture():
    """Figure 1: Three-Layer Technical Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 1. ModelArts V2.0 Three-Layer Technical Architecture',
                 fontsize=12, fontweight='bold', pad=20)

    # Toolchain Layer (Top)
    draw_box(ax, 0.5, 7.5, 9, 2,
             'Toolchain Layer / 工具链层',
             COLORS['blue'], fontsize=11)
    toolchain_items = [
        'MindSpeed-LLM', 'Megatron-Core', 'CANN 8.x',
        'torch_npu', 'MindSpore', 'MoXing API',
        'AscendCL', 'LLaMA Factory', 'vLLM-Ascend'
    ]
    for i, item in enumerate(toolchain_items):
        col = i % 3
        row = i // 3
        x = 1 + col * 3
        y = 7.8 + (1 - row) * 0.55
        draw_box(ax, x, y, 2.5, 0.45, item, COLORS['sky_blue'], text_color='black', fontsize=8)

    # Platform Layer (Middle)
    draw_box(ax, 0.5, 4.5, 9, 2.5,
             'Platform Layer / 平台层',
             COLORS['bluish_green'], fontsize=11)
    platform_items = [
        'Volcano Scheduler\n(Gang/DRF/Preempt)', 'EYWA DAG\nProvenance', 'Ascend Device Plugin',
        'ModelArts Console', 'Training Jobs', 'Notebook Development',
        'Model Management', 'Inference Services', 'Monitoring & Logging'
    ]
    for i, item in enumerate(platform_items):
        col = i % 3
        row = i // 3
        x = 1 + col * 3
        y = 4.7 + (1 - row) * 0.6
        draw_box(ax, x, y, 2.5, 0.5, item, COLORS['yellow'], text_color='black', fontsize=7)

    # Compute Layer (Bottom)
    draw_box(ax, 0.5, 1.5, 9, 2.5,
             'Compute Layer / 算力层',
             COLORS['vermillion'], fontsize=11)
    compute_items = [
        'Ascend 910B/C/D\nNPUs', 'HCCS 50GB/s\nInterconnect', 'RoCE v2\nLeaf-Spine Network',
        'Snt9b23 SuperNode\n8-Card Mesh', 'Kunpeng 920\nCPUs', 'NVMe SSD\nStorage',
        'OBS Object Storage', 'SFS Turbo\nParallel FS', 'Liquid Cooling\nInfrastructure'
    ]
    for i, item in enumerate(compute_items):
        col = i % 3
        row = i // 3
        x = 1 + col * 3
        y = 1.7 + (1 - row) * 0.6
        draw_box(ax, x, y, 2.5, 0.5, item, COLORS['orange'], text_color='black', fontsize=7)

    # Arrows between layers
    draw_arrow(ax, 5, 7.5, 5, 7.0, color=COLORS['dark_gray'], linewidth=2)
    draw_arrow(ax, 5, 4.5, 5, 4.0, color=COLORS['dark_gray'], linewidth=2)

    # Side labels
    ax.text(0.2, 8.5, 'Application\nLayer', ha='center', va='center',
            rotation=90, fontsize=9, color=COLORS['dark_gray'])
    ax.text(0.2, 5.75, 'Orchestration\nLayer', ha='center', va='center',
            rotation=90, fontsize=9, color=COLORS['dark_gray'])
    ax.text(0.2, 2.75, 'Infrastructure\nLayer', ha='center', va='center',
            rotation=90, fontsize=9, color=COLORS['dark_gray'])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_three_layer_architecture.png'), dpi=300)
    plt.close()
    print("Generated fig1_three_layer_architecture.png")


def fig2_end_to_end_workflow():
    """Figure 2: End-to-End 10-Step Cluster Practice Flowchart"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 2. ModelArts V2.0 End-to-End Cluster Training 10-Step Workflow',
                 fontsize=12, fontweight='bold', pad=20)

    steps = [
        ('1. Resource\nQuota\nApplication', COLORS['blue']),
        ('2. Custom\nImage\nBuild', COLORS['sky_blue']),
        ('3. OBS\nDataset\nPreparation', COLORS['bluish_green']),
        ('4. Training\nScript\nDevelopment', COLORS['yellow']),
        ('5. Resource\nPool\nConfiguration', COLORS['orange']),
        ('6. Job\nSubmission\n(YAML/Console)', COLORS['vermillion']),
        ('7. Volcano\nScheduling &\nAllocation', COLORS['reddish_purple']),
        ('8. Distributed\nTraining\nExecution', COLORS['blue']),
        ('9. Monitoring\n& Fault\nSelf-Healing', COLORS['sky_blue']),
        ('10. Model\nExport &\nDeployment', COLORS['bluish_green']),
    ]

    box_w = 2
    box_h = 1.2
    positions = []

    # Two rows: 5 steps each
    for i, (text, color) in enumerate(steps):
        if i < 5:
            x = 0.8 + i * 2.2
            y = 7.5
        else:
            x = 0.8 + (9 - i) * 2.2
            y = 4.5
        positions.append((x, y))
        draw_box(ax, x, y, box_w, box_h, text, color, fontsize=8)

    # Arrows within rows
    for i in range(4):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        draw_arrow(ax, x1 + box_w, y1 + box_h/2, x2, y2 + box_h/2, COLORS['black'])

    for i in range(5, 9):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        draw_arrow(ax, x1 + box_w, y1 + box_h/2, x2, y2 + box_h/2, COLORS['black'])

    # Connecting arrow from step 5 to step 6 (turnaround)
    draw_arrow(ax, positions[4][0] + box_w/2, positions[4][1],
               positions[5][0] + box_w/2, positions[5][1] + box_h,
               COLORS['dark_gray'], linewidth=2)

    # Feedback loop arrow
    draw_arrow(ax, positions[8][0] + box_w/2, positions[8][1],
               positions[3][0] + box_w/2, positions[3][1] + box_h,
               COLORS['vermillion'], style='->', linewidth=1.5)
    ax.text(6, 6.2, 'Iteration /\nHyperparameter Tuning', ha='center', va='center',
            fontsize=8, color=COLORS['vermillion'], fontweight='bold',
            bbox=dict(facecolor='white', edgecolor=COLORS['vermillion'], boxstyle='round,pad=0.3'))

    # Key artifacts labels
    ax.text(11, 7, 'OBS\nModelArts\nConsole\nVolcano\nHCCL\nCANN', ha='right', va='center',
            fontsize=8, color=COLORS['dark_gray'],
            bbox=dict(facecolor=COLORS['light_gray'], alpha=0.3, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_end_to_end_workflow.png'), dpi=300)
    plt.close()
    print("Generated fig2_end_to_end_workflow.png")


def fig3_fault_recovery_statemachine():
    """Figure 3: Fault Self-Healing State Machine"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 3. ModelArts V2.0 Five-Level Fault Self-Healing State Machine',
                 fontsize=12, fontweight='bold', pad=20)

    states = [
        ('Normal\nExecution', 5, 9, COLORS['bluish_green']),
        ('Level 1\nOperator Re-execution\n<3s, Transient AICore Error', 5, 7.2, COLORS['yellow']),
        ('Level 2\nIn-Place Recovery\n<1min, HCCL Timeout', 5, 5.4, COLORS['orange']),
        ('Level 3\nTask Retry\n<5min, Process Crash', 5, 3.6, COLORS['vermillion']),
        ('Level 4\nJob Rescheduling\n<15min, Node Failure', 3, 1.8, COLORS['reddish_purple']),
        ('Level 5\nNode Isolation\n>30min, Hardware Fault', 7, 1.8, COLORS['blue']),
    ]

    circles = []
    for text, x, y, color in states:
        circle = Circle((x, y), 0.75, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='black', wrap=True)
        circles.append((x, y))

    # Normal execution loop
    ax.text(6.8, 9.3, 'Healthy / 健康运行', ha='left', va='center', fontsize=8, color=COLORS['bluish_green'])
    draw_arrow(ax, 6.8, 9.3, 5.8, 9, color=COLORS['bluish_green'], linewidth=1.5)

    # Forward arrows (escalation)
    for i in range(4):
        x1, y1 = circles[i]
        x2, y2 = circles[i + 1] if i < 3 else (3, 2.55)
        draw_arrow(ax, x1, y1 - 0.75, x2, y2 + 0.75, COLORS['vermillion'], linewidth=1.5)
        ax.text(x1 + 0.3, (y1 + y2)/2 if i < 3 else (y1 + 2.55)/2, f'Fault\nEscalation',
                ha='left', va='center', fontsize=7, color=COLORS['vermillion'])

    # Node isolation arrow
    draw_arrow(ax, 3, 1.8 - 0.75, 7, 1.8 - 0.75, COLORS['blue'], linewidth=1.5,
               connectionstyle="arc3,rad=-0.5")
    ax.text(5, 0.7, 'Fault Correlation Analysis → Bad Node Blacklist',
            ha='center', va='center', fontsize=8, color=COLORS['blue'])

    # Recovery arrows
    recovery_labels = ['Success', 'Success', 'Success', 'Success']
    for i in range(4):
        x1, y1 = circles[i + 1]
        x2, y2 = circles[i]
        if i < 3:
            draw_arrow(ax, x1 - 0.75, y1, x2 - 0.75, y2, COLORS['bluish_green'], linewidth=1.2,
                       connectionstyle="arc3,rad=0.3")
        else:
            draw_arrow(ax, 2.25, 1.8, 4.25, 8.25, COLORS['bluish_green'], linewidth=1.2,
                       connectionstyle="arc3,rad=-0.3")
        ax.text(x1 - 1.5, y1, recovery_labels[i] + '\n恢复成功', ha='right', va='center',
                fontsize=7, color=COLORS['bluish_green'])

    # Fault code examples
    fault_codes = [
        'EZ3001/EZ3002: AICore Error',
        'EZ0001-EZ0005: HCCL Timeout',
        'EZ6001-EZ6003: OOM Error',
        'EZ5001-EZ5002: Driver/NPU Fault',
        'E9999: Fatal Error (Manual)',
    ]
    for i, code in enumerate(fault_codes):
        y = 8.5 - i * 0.4
        ax.text(0.3, y, code, ha='left', va='center', fontsize=7,
                color=COLORS['dark_gray'], family='monospace')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig3_fault_recovery_statemachine.png'), dpi=300)
    plt.close()
    print("Generated fig3_fault_recovery_statemachine.png")


def fig4_improvement_priority_matrix():
    """Figure 4: Improvement Priority Matrix (Bubble Chart)"""
    fig, ax = plt.subplots(figsize=(10, 8))

    improvements = [
        # (name, impact, effort, size, color, short_name)
        ('MoE Communication Overlap', 4.5, 2, 800, COLORS['vermillion'], 'M1'),
        ('Attention/MoE Decoupling', 4, 2.5, 700, COLORS['orange'], 'M2'),
        ('Dynamic Bubble Filling', 3.5, 3, 500, COLORS['yellow'], 'M3'),
        ('FP8 Training Support', 5, 3.5, 900, COLORS['bluish_green'], 'M4'),
        ('Ulysses Context Parallel', 4, 4, 600, COLORS['sky_blue'], 'M5'),
        ('AutoML Parallel Search', 3, 4.5, 400, COLORS['blue'], 'M6'),
        ('Ecosystem Openness', 2.5, 5, 300, COLORS['reddish_purple'], 'M7'),
    ]

    for name, impact, effort, size, color, short in improvements:
        ax.scatter(effort, impact, s=size, c=color, alpha=0.7, edgecolors='black', linewidth=1.5, zorder=5)
        ax.annotate(short, (effort, impact), ha='center', va='center',
                    fontsize=9, fontweight='bold', zorder=6)

    # Quadrant lines
    ax.axhline(y=3.5, color=COLORS['dark_gray'], linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=3, color=COLORS['dark_gray'], linestyle='--', linewidth=1, alpha=0.7)

    # Quadrant labels
    ax.text(1.5, 4.75, 'Quick Wins\n快速收益区\n(High Impact, Low Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['bluish_green'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['bluish_green'], alpha=0.1, boxstyle='round,pad=0.5'))
    ax.text(4.5, 4.75, 'Strategic Projects\n战略项目区\n(High Impact, High Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['vermillion'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['vermillion'], alpha=0.1, boxstyle='round,pad=0.5'))
    ax.text(1.5, 2, 'Fill-Ins\n补充优化区\n(Low Impact, Low Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['yellow'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['yellow'], alpha=0.1, boxstyle='round,pad=0.5'))
    ax.text(4.5, 2, 'Avoid\n低优先级区\n(Low Impact, High Effort)',
            ha='center', va='center', fontsize=10, color=COLORS['dark_gray'],
            fontweight='bold', alpha=0.8,
            bbox=dict(facecolor=COLORS['dark_gray'], alpha=0.1, boxstyle='round,pad=0.5'))

    # Legend for bubble sizes
    for size, label in [(300, 'Low Value'), (600, 'Medium Value'), (900, 'High Value')]:
        ax.scatter([], [], s=size, c=COLORS['light_gray'], edgecolors='black', label=label)
    ax.legend(loc='lower left', title='Implementation Value', title_fontsize=9, fontsize=8)

    # Legend for labels
    legend_text = '\n'.join([f'{short}: {name}' for name, _, _, _, _, short in improvements])
    ax.text(0.02, 0.02, legend_text, transform=ax.transAxes, fontsize=7,
            verticalalignment='bottom', family='monospace',
            bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.5'))

    ax.set_xlabel('Implementation Effort (1-5, Low→High)', fontweight='bold')
    ax.set_ylabel('Performance Impact (1-5, Low→High)', fontweight='bold')
    ax.set_title('Figure 4. Improvement Path Priority Matrix (Bubble Size = User Value)',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xlim(1, 5.5)
    ax.set_ylim(1, 5.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig4_improvement_priority_matrix.png'), dpi=300)
    plt.close()
    print("Generated fig4_improvement_priority_matrix.png")


def fig5_volcano_scheduler():
    """Figure 5: Volcano Scheduler Workflow Chain"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Figure 5. Volcano Scheduler Working Pipeline in ModelArts',
                 fontsize=12, fontweight='bold', pad=20)

    components = [
        ('User\n(Console/CLI/YAML)', 0.8, 6.5, COLORS['blue']),
        ('ModelArts\nAPI Server', 2.8, 6.5, COLORS['sky_blue']),
        ('Volcano Job\nController', 4.8, 6.5, COLORS['bluish_green']),
        ('Volcano\nScheduler', 6.8, 6.5, COLORS['yellow']),
        ('Kubernetes\nAPI Server', 8.8, 6.5, COLORS['orange']),
        ('Ascend Device\nPlugin + Kubelet', 10.8, 6.5, COLORS['vermillion']),
    ]

    box_w = 1.5
    box_h = 1.2

    for name, x, y, color in components:
        draw_box(ax, x - box_w/2, y - box_h/2, box_w, box_h, name, color, fontsize=8)

    # Main flow arrows (top)
    for i in range(len(components) - 1):
        x1 = components[i][1] + box_w/2 - 0.1
        x2 = components[i+1][1] - box_w/2 + 0.1
        y = components[i][2]
        draw_arrow(ax, x1, y, x2, y, COLORS['black'], linewidth=2)

    # Scheduler plugins below
    plugins = [
        ('Gang Scheduling\n(all-or-nothing)', 2.5, 3.5),
        ('DRF\n(Dominant Resource Fairness)', 4.5, 3.5),
        ('Preemption & Priority\n(抢占调度)', 6.5, 3.5),
        ('Binpack\n(Capacity Optimization)', 8.5, 3.5),
        ('NPU Topology-Aware\n(拓扑感知)', 10.5, 3.5),
    ]

    for name, x, y in plugins:
        draw_box(ax, x - 1.1, y - 0.5, 2.2, 1, name, COLORS['light_gray'],
                 text_color='black', fontsize=7)

    # Down arrows from scheduler to plugins
    for _, x, y in plugins:
        draw_arrow(ax, x, 6.5 - box_h/2, x, y + 0.5, COLORS['dark_gray'], linewidth=1.2)

    # Up arrows from plugins to scheduler
    for _, x, y in plugins:
        draw_arrow(ax, x, y + 0.5, x, 6.5 - box_h/2, COLORS['bluish_green'], linewidth=1.2)

    # Labels
    ax.text(6, 2.2, 'Scheduling Plugins / 调度插件', ha='center', va='center',
            fontsize=10, fontweight='bold', color=COLORS['dark_gray'],
            bbox=dict(facecolor='white', edgecolor=COLORS['dark_gray'], boxstyle='round,pad=0.3'))

    # Kubernetes resources
    k8s_resources = ('Pods / NPU Claims / ConfigMaps / PVCs', 6.8, 1)
    draw_box(ax, 4, k8s_resources[2] - 0.3, 5.6, 0.6, k8s_resources[0],
             COLORS['light_gray'], text_color='black', fontsize=8)
    draw_arrow(ax, k8s_resources[1], 3.5 - 0.5, k8s_resources[1], k8s_resources[2] + 0.3,
               COLORS['dark_gray'], linewidth=1.2)

    # Data flow labels
    ax.text(1.8, 7, 'Submit', fontsize=7, ha='center', color=COLORS['dark_gray'])
    ax.text(3.8, 7, 'Create', fontsize=7, ha='center', color=COLORS['dark_gray'])
    ax.text(5.8, 7, 'Enqueue', fontsize=7, ha='center', color=COLORS['dark_gray'])
    ax.text(7.8, 7, 'Schedule', fontsize=7, ha='center', color=COLORS['dark_gray'])
    ax.text(9.8, 7, 'Bind', fontsize=7, ha='center', color=COLORS['dark_gray'])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig5_volcano_scheduler.png'), dpi=300)
    plt.close()
    print("Generated fig5_volcano_scheduler.png")


def fig6_snt9b23_topology():
    """Figure 6: Snt9b23 SuperNode NPU Topology + HCCL Algorithms"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Left: Topology
    ax1.set_xlim(0, 7)
    ax1.set_ylim(0, 7)
    ax1.axis('off')
    ax1.set_title('(a) Snt9b23 SuperNode 8-Card Mesh Topology',
                  fontsize=11, fontweight='bold', pad=15)

    # Draw 8 NPUs in 2x4 grid
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

    # Draw HCCS connections (mesh - full interconnect within same row)
    for i in range(4):
        for j in range(i + 1, 4):
            x1, y1 = npu_positions[i]
            x2, y2 = npu_positions[j]
            ax1.plot([x1, x2], [y1, y2], color=COLORS['vermillion'], linewidth=1.5, alpha=0.6)
            x1, y1 = npu_positions[i + 4]
            x2, y2 = npu_positions[j + 4]
            ax1.plot([x1, x2], [y1, y2], color=COLORS['vermillion'], linewidth=1.5, alpha=0.6)

    # Cross-row connections
    for i in range(4):
        x1, y1 = npu_positions[i]
        x2, y2 = npu_positions[i + 4]
        ax1.plot([x1, x2], [y1, y2], color=COLORS['bluish_green'], linewidth=2, alpha=0.8)

    # Legend
    hccs_patch = mpatches.Patch(color=COLORS['vermillion'], alpha=0.6, label='HCCS 50GB/s (Intra-Row Mesh)')
    cross_patch = mpatches.Patch(color=COLORS['bluish_green'], alpha=0.8, label='HCCS (Inter-Row)')
    ax1.legend(handles=[hccs_patch, cross_patch], loc='lower center', fontsize=8)

    # RoCE label
    ax1.text(3.5, 0.5, 'RoCE v2 200Gbps (Inter-Node)', ha='center', va='center',
             fontsize=9, color=COLORS['blue'], fontweight='bold',
             bbox=dict(facecolor=COLORS['sky_blue'], alpha=0.2, boxstyle='round,pad=0.3'))

    # Right: HCCL Communication Algorithms
    ax2.set_xlim(0, 7)
    ax2.set_ylim(0, 7)
    ax2.axis('off')
    ax2.set_title('(b) HCCL Communication Algorithms',
                  fontsize=11, fontweight='bold', pad=15)

    # Ring algorithm
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

    # Tree algorithm
    ax2.text(5.25, 6.2, 'Tree AllReduce (Recursive Halving/Doubling)', ha='center', va='center',
             fontsize=9, fontweight='bold', color=COLORS['vermillion'])
    # Draw binary tree
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

    # Tree edges
    edges = [('root', 'l1'), ('root', 'r1'), ('l1', 'l2l'), ('l1', 'l2r'), ('r1', 'r2l'), ('r1', 'r2r')]
    for parent, child in edges:
        draw_arrow(ax2, tree_pos[parent][0], tree_pos[parent][1] - 0.25,
                   tree_pos[child][0], tree_pos[child][1] + 0.25, COLORS['vermillion'], linewidth=1.2)
    ax2.text(5.25, 2.5, 'Latency Optimal\nLatency: 2log(N) steps', ha='center', va='center',
             fontsize=7, color=COLORS['dark_gray'])

    # Hierarchical (for multi-node)
    ax2.text(3.5, 1.5, 'Hierarchical Ring-Tree Hybrid\n(Intra-Node: Ring, Inter-Node: Tree/Ring)',
             ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLORS['bluish_green'],
             bbox=dict(facecolor=COLORS['bluish_green'], alpha=0.1, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig6_snt9b23_topology.png'), dpi=300)
    plt.close()
    print("Generated fig6_snt9b23_topology.png")


def fig7_mindspeed_vs_megatron():
    """Figure 7: MindSpeed-LLM vs Megatron-Core Comparison Bar Chart"""
    fig, ax = plt.subplots(figsize=(12, 7))

    categories = [
        'Training\nThroughput\n(Seq/s)',
        'NPU\nUtilization\n(%)',
        'Checkpoint\nSave Time\n(s, lower=better)',
        'Startup\nTime\n(s, lower=better)',
        'Fault MTTR\n(s, lower=better)',
        'Ecosystem\nCompatibility\n(0-10)',
        'Operator\nCoverage\n(%)',
        'FP8 Support\n(0-10)'
    ]

    # Normalized scores (1-10, except where noted; inverted for lower-is-better)
    mindspeed_scores = [9.2, 8.8, 3.5, 4.8, 3.2, 6.5, 8.5, 9.0]
    megatron_scores = [6.5, 6.0, 6.8, 7.2, 7.5, 9.5, 7.0, 5.5]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, mindspeed_scores, width, label='MindSpeed-LLM (Ascend Optimized)',
                   color=COLORS['vermillion'], edgecolor='black', linewidth=1, alpha=0.85)
    bars2 = ax.bar(x + width/2, megatron_scores, width, label='Megatron-Core (Reference)',
                   color=COLORS['blue'], edgecolor='black', linewidth=1, alpha=0.85)

    ax.set_ylabel('Normalized Score (1-10)', fontweight='bold')
    ax.set_title('Figure 7. MindSpeed-LLM vs Megatron-Core Performance Comparison on Ascend 910B',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.legend(fontsize=10, loc='upper right')
    ax.set_ylim(0, 11)
    ax.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Add note about inverted metrics
    ax.text(0.02, 0.98, '* Lower-is-better metrics (Checkpoint/Startup/MTTR) inverted for comparison\n* Qwen2-72B, 32 nodes 256x910B, sequence length 4096',
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
    print("  fig1_three_layer_architecture.png - Three-layer technical architecture")
    print("  fig2_end_to_end_workflow.png - 10-step cluster practice workflow")
    print("  fig3_fault_recovery_statemachine.png - 5-level fault self-healing state machine")
    print("  fig4_improvement_priority_matrix.png - Improvement priority bubble matrix")
    print("  fig5_volcano_scheduler.png - Volcano scheduler working pipeline")
    print("  fig6_snt9b23_topology.png - Snt9b23 supernode topology + HCCL algorithms")
    print("  fig7_mindspeed_vs_megatron.png - MindSpeed-LLM vs Megatron-Core comparison")


if __name__ == '__main__':
    main()
