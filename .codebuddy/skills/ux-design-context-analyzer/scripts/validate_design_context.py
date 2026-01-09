#!/usr/bin/env python3
"""
设计上下文文档验证脚本

验证 DESIGN-CONTEXT.md 文件的完整性和质量
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class DesignContextValidator:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.issues = []
        self.warnings = []
        
    def load_file(self) -> bool:
        """加载文件内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except FileNotFoundError:
            self.issues.append(f"文件不存在: {self.file_path}")
            return False
        except Exception as e:
            self.issues.append(f"读取文件失败: {e}")
            return False
    
    def validate_structure(self) -> None:
        """验证文档结构"""
        required_sections = [
            "# 设计项目上下文",
            "## 项目概览",
            "## 设计资产架构", 
            "## 用户研究洞察",
            "## 设计决策框架",
            "## 协作与流程"
        ]
        
        for section in required_sections:
            if section not in self.content:
                self.issues.append(f"缺少必需章节: {section}")
    
    def validate_project_overview(self) -> None:
        """验证项目概览部分"""
        overview_fields = [
            "产品名称",
            "核心价值主张", 
            "目标用户群体",
            "当前阶段"
        ]
        
        for field in overview_fields:
            if f"**{field}**" not in self.content:
                self.warnings.append(f"项目概览缺少字段: {field}")
        
        # 检查是否有占位符未替换
        placeholders = re.findall(r'\[.*?\]', self.content)
        if placeholders:
            self.warnings.append(f"发现未替换的占位符: {', '.join(set(placeholders[:5]))}")
    
    def validate_user_research(self) -> None:
        """验证用户研究部分"""
        if "## 用户研究洞察" in self.content:
            # 检查是否包含具体的用户画像
            if "**基本信息**" not in self.content:
                self.warnings.append("用户研究部分缺少具体的用户画像信息")
            
            # 检查是否包含用户旅程
            if "用户旅程" not in self.content and "旅程地图" not in self.content:
                self.warnings.append("建议添加用户旅程相关信息")
    
    def validate_design_decisions(self) -> None:
        """验证设计决策部分"""
        if "## 设计决策框架" in self.content:
            # 检查是否包含设计原则
            if "设计原则" not in self.content:
                self.warnings.append("建议添加具体的设计原则")
            
            # 检查是否包含约束条件
            constraints = ["技术约束", "业务约束", "时间限制"]
            found_constraints = sum(1 for constraint in constraints if constraint in self.content)
            if found_constraints == 0:
                self.warnings.append("建议添加项目约束条件信息")
    
    def validate_collaboration(self) -> None:
        """验证协作流程部分"""
        if "## 协作与流程" in self.content:
            collab_elements = ["设计评审", "开发协作", "反馈"]
            found_elements = sum(1 for element in collab_elements if element in self.content)
            if found_elements < 2:
                self.warnings.append("协作流程部分信息不够完整")
    
    def check_content_quality(self) -> None:
        """检查内容质量"""
        # 检查文档长度
        if len(self.content) < 1000:
            self.warnings.append("文档内容较少，建议补充更多详细信息")
        
        # 检查是否包含链接
        links = re.findall(r'\[.*?\]\(.*?\)', self.content)
        if len(links) < 3:
            self.warnings.append("建议添加更多相关文档链接")
        
        # 检查更新时间
        if "最后更新" in self.content:
            if "[日期]" in self.content:
                self.warnings.append("请更新文档的最后更新时间")
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """执行完整验证"""
        if not self.load_file():
            return False, self.issues, self.warnings
        
        self.validate_structure()
        self.validate_project_overview()
        self.validate_user_research()
        self.validate_design_decisions()
        self.validate_collaboration()
        self.check_content_quality()
        
        is_valid = len(self.issues) == 0
        return is_valid, self.issues, self.warnings

def main():
    if len(sys.argv) != 2:
        print("使用方法: python validate_design_context.py <DESIGN-CONTEXT.md路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    validator = DesignContextValidator(file_path)
    
    is_valid, issues, warnings = validator.validate()
    
    print(f"验证文件: {file_path}")
    print("=" * 50)
    
    if issues:
        print("❌ 发现问题:")
        for issue in issues:
            print(f"  • {issue}")
        print()
    
    if warnings:
        print("⚠️  改进建议:")
        for warning in warnings:
            print(f"  • {warning}")
        print()
    
    if is_valid:
        if warnings:
            print("✅ 文档结构有效，但有改进空间")
        else:
            print("✅ 文档验证通过")
        sys.exit(0)
    else:
        print("❌ 文档验证失败")
        sys.exit(1)

if __name__ == "__main__":
    main()