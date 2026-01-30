#!/usr/bin/env python3
"""
快速启动脚本 - 项目一键运行
"""

import os
import sys
import subprocess

# 项目根目录
ROOT = os.path.dirname(os.path.abspath(__file__))

def print_section(title):
    """打印分隔符"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"🔄 正在执行: {description}")
    print(f"   命令: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} 成功!\n")
            return True
        else:
            print(f"❌ {description} 失败!\n")
            return False
    except Exception as e:
        print(f"❌ 执行出错: {e}\n")
        return False

def check_files():
    """检查必要的文件是否存在"""
    print_section("📋 文件检查")
    
    required_files = [
        ("data/jd_cleaned_comments.csv", "原始评论数据"),
        ("data/stopwords.txt", "停用词表"),
        ("data/transactions.txt", "事务数据库"),
        ("config/data_preprocessing.py", "数据预处理脚本"),
        ("experiments/run_by_support.py", "关联规则挖掘脚本"),
        ("requirements.txt", "依赖包列表"),
    ]
    
    all_exist = True
    for file_path, description in required_files:
        full_path = os.path.join(ROOT, file_path)
        if os.path.exists(full_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ 缺失: {description}: {file_path}")
            all_exist = False
    
    return all_exist

def main():
    """主函数"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🚀 关联规则挖掘项目 - 快速启动".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # 1. 检查文件
    if not check_files():
        print("\n❌ 缺少必要的文件，请检查项目结构!")
        sys.exit(1)
    
    # 2. 检查依赖
    print_section("📦 检查依赖包")
    print("正在检查必要的 Python 包...\n")
    
    required_packages = ['pandas', 'jieba', 'sklearn', 'mlxtend', 'matplotlib', 'tabulate']
    missing_packages = []
    
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg}")
        except ImportError:
            print(f"❌ 缺失: {pkg}")
            missing_packages.append(pkg)
    
    if missing_packages:
        print(f"\n⚠️  缺失的包: {', '.join(missing_packages)}")
        print("\n请运行以下命令安装依赖:")
        print(f"   pip install -r requirements.txt\n")
        sys.exit(1)
    
    # 3. 显示菜单
    print_section("📋 请选择要执行的任务")
    print("""
    1. 只检查文件（默认）
    2. 运行关联规则挖掘实验（按支持度对比）
    3. 运行规模对比实验
    4. 查看规则质量分析
    5. 生成性能对比图表
    6. 运行完整流程 (2+4+5)
    
    0. 退出
    """)
    
    choice = input("请输入选项 [0-6]，默认为 1: ").strip() or "1"
    
    print()
    
    if choice == "0":
        print("👋 再见!")
        sys.exit(0)
    
    elif choice == "1":
        print_section("✅ 文件检查完成")
        print("所有必要文件都已存在，可以开始运行实验!")
        print("\n📌 下一步建议:")
        print("   python quick_start.py")
        print("   选择选项 2 运行关联规则挖掘")
    
    elif choice == "2":
        print_section("运行关联规则挖掘")
        run_command(
            "python experiments/run_by_support.py",
            "关联规则挖掘（按支持度对比）"
        )
    
    elif choice == "3":
        print_section("运行规模对比实验")
        run_command(
            "python experiments/run_by_scale.py",
            "规模对比实验"
        )
    
    elif choice == "4":
        print_section("查看规则质量分析")
        run_command(
            "python analysis/analysis.py",
            "规则质量分析"
        )
    
    elif choice == "5":
        print_section("生成性能对比图表")
        run_command(
            "python analysis/plot_performance.py",
            "性能对比可视化"
        )
    
    elif choice == "6":
        print_section("运行完整流程")
        
        success = True
        success &= run_command(
            "python experiments/run_by_support.py",
            "关联规则挖掘"
        )
        success &= run_command(
            "python analysis/analysis.py",
            "规则质量分析"
        )
        success &= run_command(
            "python analysis/plot_performance.py",
            "性能对比可视化"
        )
        
        if success:
            print_section("✅ 完整流程执行成功！")
            print("📊 结果文件已保存到 results/ 目录:")
            print("   - performance_by_support.csv")
            print("   - quality_by_support.csv")
            print("   - rules_by_support.csv")
            print("   - *.png (图表文件)\n")
    
    else:
        print("❌ 无效的选项")
        sys.exit(1)
    
    print()

if __name__ == "__main__":
    main()
