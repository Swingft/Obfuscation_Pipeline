import os, shutil, subprocess

# 파일 삭제
def remove_files(obf_project_dir, obf_project_dir_cfg):
    file_path = "./AST/output/"
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    file_path = "./ID_Obfuscation/output/"
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    file_path = obf_project_dir_cfg
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    file_path = os.path.join(obf_project_dir, "_dyn_obf_scan_dumps")
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "./String_Encryption/strings.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "./String_Encryption/targets_swift_paths.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "./mapping_result.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "./type_info.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "./swift_file_list.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    file_path = "./targets_swift_paths.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            dir_path = os.path.join(root, '__pycache__')
            subprocess.run(['rm', '-rf', dir_path])
