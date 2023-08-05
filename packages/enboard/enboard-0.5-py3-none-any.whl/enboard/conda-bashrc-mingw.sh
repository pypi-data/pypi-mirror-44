if [[ -f /etc/bash.bashrc ]]; then
  source /etc/bash.bashrc
fi
if [[ -f ~/.bashrc ]]; then
  source ~/.bashrc
fi
if [[ -f ~/.bash_profile ]]; then
  source ~/.bash_profile
fi

source activate ${CONDA_DEFAULT_ENV}
