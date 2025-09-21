import os
import subprocess
import shutil

def run_command(cmd):
    subprocess.run(cmd, capture_output=True, text=True)

def run_swift_syntax():
    target_project_dir = "./AST/SyntaxAST"
    target_name = "SyntaxAST"
    
    original_dir = os.getcwd() 
    swift_list_dir = "./swift_file_list.txt"
    swift_list_dir = os.path.join(original_dir, swift_list_dir)

    external_list_dir = "./AST/output/external_file_list.txt"
    external_list_dir = os.path.join(original_dir, external_list_dir) 

    os.chdir(target_project_dir)
    run_command(["swift", "package", "clean"])
    shutil.rmtree(".build", ignore_errors=True)

    run_command(["swift", "build"])
    run_command(["swift", "run", target_name, swift_list_dir, external_list_dir])
