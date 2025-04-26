import os
import sys

os.chdir('./src')

if not os.path.exists("cfg/config.yml"):
    print(
        "Config file not found. Start initialization process..\n"
        "配置文件未找到，开始初始化流程\n\n"
    )

    file_path = input(
        "输入图片文件保存路径/Enter file save path\n"
        "默认/Default: ./file\n"
        "> ").strip()
    if not file_path:
        file_path = "./file"
    if not os.path.exists(file_path):
        print("路径不存在/Path not exists: ", file_path)
        os.makedirs(file_path, exist_ok=True)
        print("已创建路径/Created path: ", file_path)
        # exit(1)

    session_id = input("输入Pixiv PHPSESSID/Enter Pixiv PHPSESSID\n> ").strip()
    if not session_id:
        print("输入错误/Invalid input")
        exit(1)

    use_proxy = input("是否使用代理/Use proxy? (y/n)\n> ").strip()
    if use_proxy.lower() == "y":
        proxy_url = input("输入代理地址和端口/Enter proxy address(e.g. 127.0.0.1:7890)\n> ").strip()
        if not proxy_url:
            print("输入错误/Invalid input")
            exit(1)
    else:
        proxy_url = ""

    file_content = (
        f"file_path: {file_path}\n"
        f"session_id: {session_id}\n"
        f"proxy: {proxy_url}\n"
    )
    with open("cfg/config.yml", "w", encoding="utf-8") as f:
        f.write(file_content)
    print(
        "配置信息已保存，以下是配置内容/Config saved, following is the content:\n"
        "---------------\n"
        f"{file_content}\n"
        "---------------\n"
        "修改配置文件/src/cfg/config.yml可重新调整，或直接删除该文件后重新进行初始化流程\n"
        "Modify /src/cfg/config.yml to adjust the config, or delete the file and re-run this script\n\n"
    )
    run = input("是否立即运行/Run now? (y/n)\n> ").strip()
    if run.lower() != "y":
        exit()

if len(sys.argv) < 2:
    print("Usage: python main.py <artwork_id>")
    exit(1)
os.system("python3 run.py" + sys.argv[1])