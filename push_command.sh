aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 187768779388.dkr.ecr.ap-northeast-2.amazonaws.com
docker build -t focusmate_report_auto .
docker tag focusmate_report_auto:latest 187768779388.dkr.ecr.ap-northeast-2.amazonaws.com/focusmate_report_auto:latest
docker push 187768779388.dkr.ecr.ap-northeast-2.amazonaws.com/focusmate_report_auto:latest