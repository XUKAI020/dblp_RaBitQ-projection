import json

input_file = 'dblp.xml'
output_file = 'dblp_sample.jsonl'
target_count = 100000

print("启动纯物理层面的文本扫描 (专治 WSL 跨系统 I/O 卡顿)...")
count = 0
line_count = 0

# 核心原理解析：
# encoding='ISO-8859-1' 和 errors='ignore' 配合，直接以最底层的字节流硬读，无视任何乱码报错
with open(input_file, 'r', encoding='ISO-8859-1', errors='ignore') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    
    # for line in f_in: 是 Python 里最高效的流式读取，内存占用永远只有几 KB
    for line in f_in:
        line_count += 1
        
        # 每扫描 100 万行物理文本，必须强制汇报一次，让你知道它没死机
        if line_count % 1000000 == 0:
            print(f"底层探针：硬盘正在狂转，已扫描 {line_count} 行物理文本...")
            
        # 抛弃 XML 树，进行最原始的字符串暴力匹配
        if '<title>' in line and '</title>' in line:
            start = line.find('<title>') + 7
            end = line.find('</title>')
            clean_title = line[start:end].strip()
            
            if len(clean_title) > 20:
                f_out.write(json.dumps({'id': count, 'title': clean_title}) + '\n')
                count += 1
                
                # 每提取 1 万条，汇报一次战果
                if count % 10000 == 0:
                    print(f">>> 捷报：已成功捕获 {count} / {target_count} 条高质量文献...")
                    
                if count >= target_count:
                    break

print("第一阶段数据加工彻底完成！准备进入矩阵运算。")
