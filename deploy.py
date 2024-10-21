from dotenv import load_dotenv
import subprocess

# .env 파일에서 환경 변수 로드
load_dotenv()

# 배포 명령어 실행
subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"])
subprocess.run(["twine", "upload", "dist/*"])
