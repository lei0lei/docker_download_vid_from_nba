FROM python:3.9.16-slim
# RUN rm -rf /opt/pytorch  # remove 1.2GB dir

RUN apt update && apt install --no-install-recommends -y git zip htop screen libgl1-mesa-glx

# COPY requirements.txt .
RUN python -m pip install --upgrade pip

# RUN pip install --no-cache -r requirements.txt #albumentations wandb gsutil notebook Pillow>=9.1.0 
#torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113

RUN mkdir -p /usr/src
RUN ls
RUN ls
RUN git clone https://github.com/lei0lei/docker_download_vid_from_nba.git /usr/src

WORKDIR /usr/src

RUN pip install --no-cache -r requirements.txt 
# COPY . /usr/src

ENV OMP_NUM_THREADS=8

CMD ["/bin/bash"]

# CMD ["uvicorn", "app.apitest.testwatermark:app", "--host", "0.0.0.0", "--port", "8000"]