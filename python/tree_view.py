import os
import math

def format_size(size_bytes):
    """
    格式化文件大小为易读形式
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024))) if size_bytes > 0 else 0
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2) if p > 0 else 0
    return f"{s}{size_name[i]}"

def display_tree(folder_path, prefix="", depth=0, max_depth=None, include_hidden=False, file_filter=None, output_lines=[]):
    """
    显示文件夹的树状结构
    :param folder_path: 文件夹路径
    :param prefix: 用于树状结构的前缀
    :param depth: 当前递归深度
    :param max_depth: 最大递归深度
    :param include_hidden: 是否包括隐藏文件
    :param file_filter: 文件类型过滤器
    :param output_lines: 用于保存输出的列表
    """
    if max_depth is not None and depth > max_depth:
        return

    try:
        entries = os.listdir(folder_path)
        entries.sort()
        entries_filtered = []
        for entry in entries:
            if not include_hidden and entry.startswith('.'):
                continue
            if file_filter and not os.path.isdir(os.path.join(folder_path, entry)):
                if not entry.endswith(file_filter):
                    continue
            entries_filtered.append(entry)

        for index, entry in enumerate(entries_filtered):
            entry_path = os.path.join(folder_path, entry)
            is_last = index == len(entries_filtered) - 1
            connector = "└── " if is_last else "├── "
            try:
                size = os.path.getsize(entry_path)
                size_formatted = format_size(size)
            except:
                size_formatted = "Unknown"
            line = f"{prefix}{connector}{entry} ({size_formatted})"
            print(line)
            output_lines.append(line)
            if os.path.isdir(entry_path):
                new_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
                display_tree(entry_path, new_prefix, depth + 1, max_depth, include_hidden, file_filter, output_lines)
    except PermissionError:
        line = f"{prefix}└── [Permission Denied]"
        print(line)
        output_lines.append(line)

def main():
    # 设置起始路径
    base_folder = input("请输入起始文件夹路径: ").strip()
    if not os.path.exists(base_folder) or not os.path.isdir(base_folder):
        print("输入的路径无效或不是文件夹！")
        return

    # 设置是否包含隐藏文件
    include_hidden = input("是否包含隐藏文件？(y/n): ").strip().lower() == 'y'

    # 设置文件类型过滤器
    file_filter = input("请输入要过滤的文件类型（例如 '.txt'，直接回车表示不过滤）: ").strip() or None

    # 设置最大递归深度
    max_depth_input = input("请输入最大递归深度（直接回车表示不限制）: ").strip()
    max_depth = int(max_depth_input) if max_depth_input.isdigit() else None

    # 是否将输出保存到文件
    save_output = input("是否将结果保存到文件？(y/n): ").strip().lower() == 'y'
    output_file = None
    if save_output:
        output_file = input("请输入输出文件的路径: ").strip()

    while True:
        # 列出所有子目录
        directories = [
            entry for entry in os.listdir(base_folder)
            if os.path.isdir(os.path.join(base_folder, entry)) and (include_hidden or not entry.startswith('.'))
        ]
        directories.sort()

        if not directories:
            print("该文件夹下没有子目录。")
            break

        print("\n可用目录列表：")
        for idx, directory in enumerate(directories):
            print(f"{idx + 1}. {directory}")

        selected_indices = input(
            "\n请选择要查看的目录（用逗号分隔多个选择，输入'q'退出）: "
        ).strip()

        if selected_indices.lower() == 'q':
            print("程序已退出。")
            break

        try:
            indices = [int(i) - 1 for i in selected_indices.split(",")]
            selected_folders = [directories[i] for i in indices if 0 <= i < len(directories)]

            if not selected_folders:
                print("没有选择有效的目录，请重试。")
                continue

            # 显示选中目录的树状结构
            for folder in selected_folders:
                print(f"\n{folder}")
                print("-" * len(folder))
                output_lines = [folder, "-" * len(folder)]
                display_tree(
                    os.path.join(base_folder, folder),
                    max_depth=max_depth,
                    include_hidden=include_hidden,
                    file_filter=file_filter,
                    output_lines=output_lines
                )
                if save_output and output_file:
                    with open(output_file, 'a', encoding='utf-8') as f:
                        f.write('\n'.join(output_lines) + '\n')
        except (ValueError, IndexError):
            print("输入无效，请输入正确的数字。")

if __name__ == "__main__":
    main()
