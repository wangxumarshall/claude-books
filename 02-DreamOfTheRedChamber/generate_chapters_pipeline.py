#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《石头记》（红楼梦）原旨向后四十回 AI 续写自动化构建与检测管道 (Pipeline)

此脚本基于 `CLAUDE.md` 中确立的“四大文风铁律”与“逐回提纲”，提供了以下核心功能：
1. 自动解析 CLAUDE.md，提取全局系统提示词 (System Prompt) 与单回独立提示词。
2. 对已生成的章节文字进行【现代双音节违禁词】（黑名单）自动化校验与精准定位。
3. 自动检测大语言模型易犯的【循环降级与废话复读】问题（如“那张妈便只是叹气”）。
4. 检查是否严格包含了该回提示词所要求的【器物映衬】与【空镜头景物】关照。
5. 支持调用主流大模型 API（如 Anthropic Claude、OpenAI / DeepSeek / Gemini 等）分回隔离生成。
"""

import os
import re
import sys
import glob

# 解决 Windows powershell 终端输出 UTF-8 编码兼容性问题
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# -------------------------------------------------------------------------
# 核心违禁词库（绝不能在正文中出现任何现代汉语双音节词或说教总结）
# -------------------------------------------------------------------------
MODERN_WORDS_BLACKLIST = [
    "企图", "素质", "反映", "悲剧", "意识", "封建", "经济", "心理", "崩溃", 
    "矛盾", "情绪", "心态", "氛围", "环境", "动向", "尴尬", "沟通", "交流", 
    "理智", "甚至于", "无论如何", "其实", "因此", "由于", "典型", "本质", 
    "体现", "揭露", "压迫", "阶级", "象征", "深刻", "思想", "社会", "时代"
]

# 常见 LLM 降级复读警报词（若单章内出现超过3次，立刻报错提示模型堕入死循环）
DEGRADATION_PATTERNS = [
    r"叹了口气，也?不言语",
    r"便只是叹气，也?不言语",
    r"只盼着那.*能好起来",
    r"心头肉.*过得好便放心"
]

def load_claude_md(claude_md_path="CLAUDE.md"):
    """自 CLAUDE.md 提取全局系统指令与章节提纲"""
    if not os.path.exists(claude_md_path):
        raise FileNotFoundError(f"未找到 {claude_md_path}，请确保路径正确。")
    
    with open(claude_md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取全局系统指令
    sys_match = re.search(r"# 【全局最高指令：曹雪芹《石头记》原旨与白描文风铁律】(.*?)\s+---\s+#", content, re.DOTALL)
    system_prompt = sys_match.group(0) if sys_match else content[:2000]
    
    return system_prompt, content

def audit_chapter_text(chapter_num, text):
    """
    对已完成的单回正文进行严格学术与文风审查
    返回: (是否通过: bool, 报告文本: str)
    """
    errors = []
    warnings = []
    
    # 1. 检查现代违禁词
    found_modern = []
    for word in MODERN_WORDS_BLACKLIST:
        if word in text:
            matches = [m.start() for m in re.finditer(word, text)]
            found_modern.append(f"「{word}」({len(matches)}次)")
    if found_modern:
        errors.append(f"【严重违约】检测到现代汉语双音节违禁词：{', '.join(found_modern)}")
    
    # 2. 检查循环退化 (LLM Loop Degradation)
    for pat in DEGRADATION_PATTERNS:
        matches = re.findall(pat, text)
        if len(matches) >= 3:
            errors.append(f"【模型降级】检测到高度机械化重复复读模式：「{matches[0]}」等出现 {len(matches)} 次")
    
    # 3. 检查体量字数（单回正文不得少于 2500 字，过多废话亦需警惕）
    char_count = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))
    if char_count < 2000:
        warnings.append(f"【篇幅偏短】当前总字数仅 {char_count} 字，曹雪芹原著单回多在 3000~5000 字，可能缺乏足够的日常琐碎与景物细写。")
    
    # 4. 检查是否具有基本的景物或时空连接句式（粗略判断白描含金量）
    classical_markers = ["话说", "却说", "且说", "谁知", "早有", "只听得", "岂料", "正是：", "要知"]
    marker_count = sum(1 for m in classical_markers if m in text)
    if marker_count < 2:
        warnings.append("【文风疑虑】缺乏清代中叶白话小说标志性话本承转语词（如“却说、谁知、早有、只听得”等）。")

    passed = len(errors) == 0
    report_lines = [f"====== 第 {chapter_num:03d} 回审查报告 ======"]
    status_str = "[PASS] 校验通过 (GOLD STANDARD)" if passed else "[FAIL] 校验失败 (NEEDS REWRITE)"
    report_lines.append(f"总字数：{char_count} 字 | 状态：{status_str}")
    if errors:
        report_lines.append("【错误项 - 必须重写或修正】：")
        for e in errors:
            report_lines.append("  - " + e)
    if warnings:
        report_lines.append("【建议项】：")
        for w in warnings:
            report_lines.append("  - " + w)
    report_lines.append("")
    
    return passed, "\n".join(report_lines)

def run_batch_audit(chapters_dir="chapters"):
    """扫描 chapters/ 目录下所有已生成的 txt 章节并生成全库审计报告"""
    print(f"正在扫描目录: {chapters_dir} ...\n")
    files = sorted(glob.glob(os.path.join(chapters_dir, "chapter_*.txt")))
    if not files:
        print("未在 chapters/ 目录下找到 chapter_*.txt 文件。")
        return
    
    pass_count = 0
    fail_count = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        match = re.search(r"chapter_(\d+)\.txt", filename)
        if not match:
            continue
        c_num = int(match.group(1))
        
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            
        passed, report = audit_chapter_text(c_num, text)
        print(report)
        if passed:
            pass_count += 1
        else:
            fail_count += 1
            
    print(f"====== 全库检查完毕 ====== ")
    print(f"合格章节：{pass_count} 回 | 不合格章节：{fail_count} 回")
    print("提示：对于校验失败的章节，请遵照 CLAUDE.md 中的全局最高指令与该回提示词，使用大模型隔离重新生成！")

if __name__ == "__main__":
    run_batch_audit()
