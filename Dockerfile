FROM jupyter/base-notebook
HEALTHCHECK NONE
# RUN apt update && apt install --no-install-recommends -y git zip htop screen libgl1-mesa-glx
# RUN apt install --no-install-recommends -y openssh-server 
# RUN mkdir /var/run/sshd
# RUN chmod 0755 /var/run/sshd
# RUN /usr/sbin/sshd

# RUN useradd -m boyan && echo "boyan:111111" | chpasswd && adduser boyan sudo

RUN python -m pip install --upgrade pip

USER root


RUN mkdir -p /usr/src

# RUN ls


WORKDIR /usr/src
COPY ./requirements.txt /usr/src
RUN pip install --no-cache -r requirements.txt 

ENTRYPOINT ["jupyter","lab","--p=8888","--NotebookApp.token=''","--allow-root"]
# CMD ["/bin/bash"]