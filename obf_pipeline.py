import os, sys, subprocess, shutil
import time

from remove_files import remove_files
from AST.run_ast import run_ast
from Mapping.run_mapping import mapping
from ID_Obf.id_dump import make_dump_file_id
from merge_list import merge_llm_and_rule
from Opaquepredicate.run_opaque import run_opaque
from DeadCode.deadcode import deadcode
from remove_debug_symbol import remove_debug_symbol

def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    # print(result.stderr)

def obf_pipeline(original_project_dir, obf_project_dir): 
    original_dir = os.getcwd()

    # 파일 삭제
    remove_files(obf_project_dir, "")

    start = time.time()

    # 1차 룰베이스 제외 대상 식별 & 식별자 난독화
    run_ast(obf_project_dir)

    ast_end = time.time()
    print("ast: ", ast_end - start)

    # Rule & LLM 결과 병합
    merge_llm_and_rule()

    # 식별자 매핑
    mapping()
    
    mapping_end = time.time()
    print("mapping: ", mapping_end - ast_end)

    # 식별자 난독화
    swift_list_dir = "./swift_file_list.txt"
    swift_list_dir = os.path.join(original_dir, swift_list_dir) 
    mapping_result_dir = "./mapping_result_s.json"
    mapping_result_dir = os.path.join(original_dir, mapping_result_dir)    

    target_project_dir = "./ID_Obf"
    target_name = "IDOBF"

    os.chdir(target_project_dir)
    build_marker_file = ".build/build_path.txt"
    previous_build_path = ""
    if os.path.exists(build_marker_file):
        with open(build_marker_file, "r") as f:
            previous_build_path = f.read().strip()
    
    current_build_path = os.path.abspath(".build")
    if previous_build_path != current_build_path or previous_build_path == "":
        run_command(["swift", "package", "clean"])
        shutil.rmtree(".build", ignore_errors=True)
        run_command(["swift", "build"])
        with open(build_marker_file, "w") as f:
            f.write(current_build_path)
    run_command(["swift", "run", target_name, mapping_result_dir, swift_list_dir])

    # 식별자 난독화 덤프파일 생성
    os.chdir(original_dir)
    make_dump_file_id(original_project_dir, obf_project_dir)

    id_end = time.time()
    print("id-obf: ", id_end - mapping_end)

    # 제어흐름 평탄화
    cff_path = os.path.join(original_dir, "CFF")
    os.chdir(cff_path)
    build_marker_file = ".build/build_path.txt"
    previous_build_path = ""
    if os.path.exists(build_marker_file):
        with open(build_marker_file, "r") as f:
            previous_build_path = f.read().strip()
    
    current_build_path = os.path.abspath(".build")
    if previous_build_path != current_build_path or previous_build_path == "":
        run_command(["swift", "package", "clean"])
        shutil.rmtree(".build", ignore_errors=True)
        run_command(["swift", "build"])
        with open(build_marker_file, "w") as f:
            f.write(current_build_path)
    cmd = ["swift", "run", "Swingft_CFF", obf_project_dir]
    run_command(cmd)
    os.chdir(original_dir)

    cff_end = time.time()
    print("cff: ", cff_end - id_end)

    # 불투명한 술어 삽입
    run_opaque(obf_project_dir)

    opaq_end = time.time()
    print("opaq: ", opaq_end - cff_end)

    # 데드코드 삽입
    deadcode()
    
    deadcode_end = time.time()
    print("deadcode: ", deadcode_end - opaq_end)

    # 문자열 암호화
    enc_path = os.path.join(original_dir, "String_Encryption")
    os.chdir(enc_path)
    cmd = ["python3", "run_Swingft_Encryption.py", obf_project_dir, "../Swingft_config.json"]
    run_command(cmd)
    os.chdir(original_dir)

    enc_end = time.time()
    print("encryption: ", enc_end - deadcode_end)

    # 동적 함수 호출
    obf_project_dir_cfg = os.path.join(os.path.dirname(obf_project_dir), "cfg")
    shutil.copytree(obf_project_dir, obf_project_dir_cfg)

    cfg_path = os.path.join(original_dir, "CFG")
    os.chdir(cfg_path)
    cmd = ["python3", "run_pipeline.py", "--src", obf_project_dir_cfg, "--dst", obf_project_dir, 
           "--perfile-inject", "--overwrite", "--debug", "--include-packages", "--no-skip-ui"]
    run_command(cmd)
    os.chdir(original_dir)

    cfg_end = time.time()
    print("cfg: ", cfg_end - enc_end)

    # 디버깅용 코드 제거
    remove_debug_symbol(obf_project_dir)

    debug_end = time.time()
    print("debug: ", debug_end - cfg_end)

    print("total: ", debug_end - start)
    print((debug_end - start) / 60)
    
    # 파일 삭제
    remove_files(obf_project_dir, obf_project_dir_cfg)

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
  
    obf_pipeline(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
