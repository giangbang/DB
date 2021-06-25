from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import sys

stdout = sys.stdout
stderr = sys.stderr

log_file = open('log', 'w')
sys.stdout = log_file
sys.stderr = log_file

cxx_args = ['-std=c++14']

nvcc_args = [
    '-gencode', 'arch=compute_50,code=sm_50',
    '-gencode', 'arch=compute_52,code=sm_52',
    '-gencode', 'arch=compute_60,code=sm_60',
    '-gencode', 'arch=compute_61,code=sm_61',
    '-gencode', 'arch=compute_70,code=sm_70',
    '-gencode', 'arch=compute_70,code=compute_70'
]

setup(
    name='deform_conv',
    ext_modules=[
        CUDAExtension('deform_conv_cuda', [
            'src/deform_conv_cuda.cpp',
            'src/deform_conv_cuda_kernel.cu',
        ], extra_compile_args={'cxx': cxx_args, 'nvcc': nvcc_args}), 
        CUDAExtension('deform_pool_cuda', [
            'src/deform_pool_cuda.cpp', 'src/deform_pool_cuda_kernel.cu'
        ], extra_compile_args={'cxx': cxx_args, 'nvcc': nvcc_args}),
    ],
    cmdclass={'build_ext': BuildExtension})

# Make sure to close the log file. You could also use with to surround the setup()
# To ensure log file is closed in the event of exception.
log_file.close()

sys.stdout = stdout
sys.stderr = stderr

with open('log', 'r') as log_file:
    sys.stdout.write(log_file.read())
