import os
import csv
from pathlib import Path


def scan_files_to_csv(root_dir: str, output_csv_path: str):
    """
        遍历目录并提取文件路径信息保存到 CSV。

        Args:
            root_dir (str): 要扫描的根目录路径
            output_csv_path (str): 保存结果的 CSV 文件路径
        """
    # 转换为 Path 对象并获取绝对路径，防止相对路径导致解析错误
    base_path = Path(root_dir).resolve()
    out_path = Path(output_csv_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"正在扫描目录: {base_path} ...")

    # 定义 CSV 表头
    headers = ['class', 'plt_name', 'type', 'plt_filepath']

    count = 0

    # os.mkdir(output_csv_path)
    # os.makedirs(output_csv_path, exist_ok=True)
    # Path(output_csv_path).mkdir(parents=True, exist_ok=True)

    # encoding='utf-8-sig' 可以让 Excel 正确识别中文乱码
    with open(output_csv_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        # rglob('*') 表示递归查找所有文件
        for file_path in base_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() == '.plt':
                try:
                    # 1. 获取完整绝对路径
                    full_path = str(file_path)

                    # 2. 获取文件名
                    file_name = file_path.name

                    # 3. 获取上级目录 (Parent)
                    # 例如: /a/b/c.txt -> b
                    parent_name = file_path.parent.name

                    # 4. 获取上上级目录 (Grandparent)
                    # 例如: /a/b/c.txt -> a
                    # 逻辑：判断路径层级深度，避免根目录报错
                    if len(file_path.parents) >= 2:
                        grandparent_name = file_path.parent.parent.name
                    else:
                        grandparent_name = "N/A"  # 已经到达系统根目录，没有上上级

                    # 写入一行
                    writer.writerow([grandparent_name, file_name, parent_name, full_path])
                    count += 1

                    # 每处理 1000 个文件打印一次进度
                    if count % 1000 == 0:
                        print(f"已处理 {count} 个文件...")

                except Exception as e:
                    print(f"处理文件出错 {file_path}: {e}")

    print(f"\n完成！共处理 {count} 个文件。")
    print(f"结果已保存至: {output_csv_path}")

def scan_files_to_csv_2(root_dir: str, output_csv_path: str):
    """
        遍历目录并提取文件路径信息保存到 CSV。
        新增功能：能处理不同层级文件，有些plt文件两层需要的父文件，有些三层

        Args:
            root_dir (str): 要扫描的根目录路径
            output_csv_path (str): 保存结果的 CSV 文件路径
        """
    # 转换为 Path 对象并获取绝对路径，防止相对路径导致解析错误
    base_path = Path(root_dir).resolve()
    out_path = Path(output_csv_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"正在扫描目录: {base_path} ...")

    # 定义 CSV 表头
    headers = ['class', 'subclass', 'sub_subclass', 'plt_name', 'type', 'plt_filepath']

    count = 0

    # os.mkdir(output_csv_path)
    # os.makedirs(output_csv_path, exist_ok=True)
    # Path(output_csv_path).mkdir(parents=True, exist_ok=True)

    # encoding='utf-8-sig' 可以让 Excel 正确识别中文乱码
    with open(output_csv_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        # rglob('*') 表示递归查找所有文件
        for file_path in base_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() == '.plt':
                try:
                    full_path = str(file_path)
                    file_name = file_path.name

                    parts = file_path.parts
                    index = parts.index('cls_data')
                    relative_path = Path(*parts[index + 1:])

                    rela_parts = relative_path.parts
                    class_file = rela_parts[0]
                    if class_file.lstrip("0123456789_") == 'sew_and_trim':
                        subclass_file = rela_parts[1]
                        type_file = rela_parts[2]
                        if len(rela_parts) == 4:
                            sub_subclass_file = ''
                        elif len(rela_parts) == 5:
                            sub_subclass_file = rela_parts[3]
                    else:
                        sub_subclass_file = ''
                        type_file = rela_parts[1]
                        if len(rela_parts) == 3:
                            subclass_file = ''
                        elif len(rela_parts) == 4:
                            subclass_file = rela_parts[2]
                        else:
                            raise ValueError("File path error.")

                    # 写入一行
                    writer.writerow([class_file, subclass_file, sub_subclass_file, file_name, type_file, full_path])
                    count += 1

                    # 每处理 1000 个文件打印一次进度
                    if count % 1000 == 0:
                        print(f"已处理 {count} 个文件...")

                except Exception as e:
                    print(f"处理文件出错 {file_path}: {e}")

    print(f"\n完成！共处理 {count} 个文件。")
    print(f"结果已保存至: {output_csv_path}")


if __name__ == "__main__":
    target_directory = "/home/cyh/Documents/T1/cls_data"
    save_file = "/home/cyh/Documents/T1/cls_data/cls_data.csv"

    # scan_files_to_csv(target_directory, save_file)
    scan_files_to_csv_2(target_directory, save_file)
