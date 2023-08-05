FROM quay.io/pypa/manylinux1_x86_64

WORKDIR /root

RUN /opt/python/cp37-cp37m/bin/python -m venv /root/build-env
RUN ln -s /opt/python/cp37-cp37m/include/* /root/build-env/include/

COPY build_requirements.txt /root/build_requirements.txt

RUN . /root/build-env/bin/activate && pip install -r build_requirements.txt

RUN mkdir /root/pytubes

COPY . /root/pytubes/

WORKDIR /root/pytubes

RUN . /root/build-env/bin/activate && PYTHON_CONFIG=/opt/python/cp37-cp37m/bin/python3-config make install test
#RUN . /root/build-env/bin/activate && CFLAGS='-I/root/build-env/include' make test