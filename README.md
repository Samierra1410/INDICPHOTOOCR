# BharatSTR

## Installation
Currently we need to manually create virtual environemnt.
```
conda create -n bharatocr python=3.9 -y
conda activate bharatocr
cd bharatSTR

pip install pip-tools
make clean-reqs reqs  # Regenerate all the requirements files
# Use specific platform build. Other PyTorch 2.0 options: cu118, cu121, rocm5.7
platform=cpu
# Generate requirements files for specified PyTorch platform
make torch-${platform}
# Install the project and core + train + test dependencies. Subsets: [train,test,bench,tune]
pip install -r requirements/core.${platform}.txt -e .[train,test]
pip install fire==0.6.0
pip install numpy==1.26.4
```

## Inference

## Training

## Acknowledgement 

## Contant
