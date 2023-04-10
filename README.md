# docker_download_vid_from_nba
download videos from nba.com using download link csv

# 使用预编译镜像

使用下列命令:
```sh
docker pull lei0lei/nba:latest
```

# docker编译流程
```
git clone https://github.com/lei0lei/docker_download_vid_from_nba.git
```
切换到项目目录下，运行
```sh
docker build -t nba .
```
如果需要添加python包，写入requirements后重新编译docker


# 其他
编译成功后，如要进入docker环境，在命令行输入以下命令，自动进入docker中的项目目录:
```sh
docker run --user root -p 8888:8888 nba
```