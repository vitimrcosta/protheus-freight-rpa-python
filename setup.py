# ============================================================================
# setup.py
# Configuração do pacote Python
# ============================================================================

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rpa-automacao-pedidos",
    version="1.0.0",
    author="Sistema RPA de Automação",
    description="Sistema de automação de processamento de pedidos com RPA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vitimrcosta/protheus-freight-rpa-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "schedule>=1.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "rpa-pedidos=src.main:main",
        ],
    },
)
