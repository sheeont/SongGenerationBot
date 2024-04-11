import os
import logging

import torch
from omegaconf import OmegaConf

path = os.path.join(os.path.dirname(__file__), 'latest_silero_models.yml')

# try:
#     if not os.path.exists(path):
#         torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
#                                        path)
# except Exception as error:
#     logging.error(msg=error)

models = OmegaConf.load(path)
