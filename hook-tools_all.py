# hook-tools_all.py
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_dynamic_libs, collect_submodules

# OpenCV - Haar cascades
datas = collect_data_files('cv2', subdir='data')

# Torch и зависимости
torch_datas, torch_binaries, torch_hidden = collect_all('torch')
datas += torch_datas
binaries = torch_binaries
hiddenimports = torch_hidden

# Добавляем специфичные бинарные файлы torch
binaries += collect_dynamic_libs('torch')

# Torchvision
torchvision_datas, torchvision_binaries, torchvision_hidden = collect_all('torchvision')
datas += torchvision_datas
binaries += torchvision_binaries
hiddenimports += torchvision_hidden

# Ultralytics/YOLO
ultralytics_datas, ultralytics_binaries, ultralytics_hidden = collect_all('ultralytics')
datas += ultralytics_datas
binaries += ultralytics_binaries
hiddenimports += ultralytics_hidden

# OmegaConf
omegaconf_datas, omegaconf_binaries, omegaconf_hidden = collect_all('omegaconf')
datas += omegaconf_datas
binaries += omegaconf_binaries
hiddenimports += omegaconf_hidden

# Специфичные подмодули
hiddenimports += [
    # Torch
    'torch._dynamo', 'torch._C', 'torch._jit_internal', 'torch._ops',
    'torch._tensor', 'torch._utils', 'torch.backends.cudnn',
    'torch.backends.mps', 'torch.backends.cuda',
    
    # Ultralytics
    'ultralytics.nn.autobackend', 'ultralytics.nn.tasks',
    'ultralytics.data.augment', 'ultralytics.data.base',
    'ultralytics.data.dataset', 'ultralytics.engine.exporter',
    'ultralytics.engine.predictor', 'ultralytics.engine.trainer',
    'ultralytics.engine.validator', 'ultralytics.utils.downloads',
    'ultralytics.utils.ops', 'ultralytics.utils.plotting',
]