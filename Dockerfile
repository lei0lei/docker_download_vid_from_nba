FROM python:3.9.16-slim

RUN apt update && apt install  openssh-server sudo -y
# Create a user “sshuser” and group “sshgroup”
RUN groupadd sshgroup && useradd -ms /bin/bash -g sshgroup sshuser
# Create sshuser directory in home
RUN mkdir -p /home/sshuser/.ssh
# Copy the ssh public key in the authorized_keys file. The idkey.pub below is a public key file you get from ssh-keygen. They are under ~/.ssh directory by default.
COPY idkey.pub /home/sshuser/.ssh/authorized_keys
# change ownership of the key file. 
RUN chown sshuser:sshgroup /home/sshuser/.ssh/authorized_keys && chmod 600 /home/sshuser/.ssh/authorized_keys
# Start SSH service
RUN service ssh start
# Expose docker port 22
EXPOSE 22

RUN apt update && apt install --no-install-recommends -y git zip htop screen libgl1-mesa-glx

RUN python -m pip install --upgrade pip

RUN mkdir -p /usr/src

RUN git clone https://github.com/lei0lei/docker_download_vid_from_nba.git /usr/src

WORKDIR /usr/src

RUN pip install --no-cache -r requirements.txt 
# COPY . /usr/src

# ENV OMP_NUM_THREADS=8

# CMD ["python", "example/download_video.py"]

CMD ["/usr/sbin/sshd","-D"]
CMD ["/bin/bash"]
