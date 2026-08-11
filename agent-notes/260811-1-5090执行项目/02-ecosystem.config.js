module.exports = {
    apps: [
      {
        name: "moss-subtitle-web",
        // 因为指定了 python 解释器，script 需要指向 mtd-subtitle-web 的实际 Python 脚本路径。
        // 在 conda 环境中，通过 pip install -e . 安装的命令行工具，其入口脚本通常位于环境的 bin 目录下。
        script: "/home/caiyf/miniconda3/envs/moss-trans/bin/mtd-subtitle-web", 
        interpreter: "/home/caiyf/miniconda3/envs/moss-trans/bin/python",
        args: [
          "--model", "OpenMOSS-Team/MOSS-Transcribe-Diarize",
          "--host", "0.0.0.0",
          "--port", "7860",
          "--max-new-tokens", "105536",
          "--prompt", "请将音频转写为文本，每一段需以说话人编号（[S01]、[S02]、[S03]…）开头，正文为对应的语音内容。"
        ],
        
        cwd: "/home/caiyf/document",
        env: {
          HF_ENDPOINT: "https://hf-mirror.com",
          HF_HUB_DISABLE_XET: "1"
        },
        
        autorestart: true,
        watch: false,
        
        // 日志配置
        error_file: "./logs/moss-web-error.log",
        out_file: "./logs/moss-web-out.log",
        merge_logs: true,
        time: true
      }
    ]
  };