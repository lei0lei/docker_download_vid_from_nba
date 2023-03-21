# docker_download_vid_from_nba
download videos from nba.com using download link csv

# 使用预编译镜像

使用下列命令:
```sh
docker pull lei0lei/nba:latest
```

# docker编译流程

git clone https://github.com/lei0lei/docker_download_vid_from_nba.git

切换到项目目录下，运行
```sh
docker build -t nba .
```

# 其他
编译成功后，如要进入docker环境，在命令行输入以下命令，自动进入docker中的项目目录:
```sh
docker run --rm -it --entrypoint /bin/bash nba
```

另一个方式是[docker exec](https://stackoverflow.com/questions/30172605/how-do-i-get-into-a-docker-containers-shell)

在宿主机及docker环境下共享目录，参考:
[bind mount](https://docs.docker.com/get-started/06_bind_mounts/)

如docker启动后自动运行python程序，在dockerfile中补充CMD命令。

原则上不应为docker镜像提供任何远程连接方式，尤其是ssh命令，但是本仓库仍然提供了这一功能。