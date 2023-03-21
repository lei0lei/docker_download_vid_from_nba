FROM python:3.9.16-slim

RUN apt update && apt install --no-install-recommends -y git zip htop screen libgl1-mesa-glx openssh-server


RUN mkdir /var/run/sshd
RUN chmod 0755 /var/run/sshd
RUN /usr/sbin/sshd

RUN useradd --create-home --shell /bin/bash --groups sudo boyan
RUN echo boyan:111111 | chpasswd

RUN python -m pip install --upgrade pip

RUN mkdir -p /usr/src

RUN git clone https://github.com/lei0lei/docker_download_vid_from_nba.git /usr/src

WORKDIR /usr/src

RUN pip install --no-cache -r requirements.txt 
# COPY . /usr/src

# ENV OMP_NUM_THREADS=8

# CMD ["python", "example/download_video.py"]

CMD ["/bin/bash"]
