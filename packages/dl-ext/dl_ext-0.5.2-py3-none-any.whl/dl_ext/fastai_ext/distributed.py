import os
import pickle
import time
from os import path as osp

import torch.distributed as dist
from fastai.basic_data import DatasetType, warn
from fastai.basic_train import Learner, _loss_func2activ
from fastai.distributed import DistributedDataParallel

from .basic_train import *
from ..pytorch_ext.sampler import OrderedDistributedSampler


def get_preds_distributed(learn: Learner, ds_type: DatasetType = DatasetType.Valid, with_loss: bool = False,
                          n_batch: Optional[int] = None,
                          pbar: Optional[PBar] = None):
    lf = learn.loss_func if with_loss else None
    if not dist.is_initialized():
        warn('torch.distributed has not been initialized! Drop to single gpu get_preds.')
        return get_preds(learn.model, learn.dl(ds_type), cb_handler=CallbackHandler(learn.callbacks),
                         activ=_loss_func2activ(learn.loss_func), loss_func=lf, n_batch=n_batch, pbar=pbar)
    os.makedirs('tmp', exist_ok=True)
    rank = dist.get_rank()
    world_size = dist.get_world_size()
    if ds_type != DatasetType.Valid:
        raise ValueError('currently only Valid type is supported!')
    # Train Valid Test Single Fix
    # todo: add multi type support
    # todo: implement safer multi-process mechanism
    # todo: fix break down when num_eval is small

    learn.model = DistributedDataParallel(learn.model, device_ids=[rank],
                                          output_device=rank)
    valid_sampler = OrderedDistributedSampler(learn.data.valid_dl.dataset)
    num_eval = len(learn.data.valid_dl.dataset)
    old_valid_dl = learn.data.valid_dl
    learn.data.valid_dl = learn.data.valid_dl.new(shuffle=False, sampler=valid_sampler)
    preds = get_preds(learn.model, learn.dl(ds_type), cb_handler=CallbackHandler(learn.callbacks),
                      activ=_loss_func2activ(learn.loss_func), loss_func=lf, n_batch=n_batch, pbar=pbar)
    pickle.dump(preds, open(osp.join('tmp', f'preds{rank}.pkl'), 'wb'))
    learn.model = learn.model.module
    # merge results and return
    if rank == 0:
        merged_preds = [[t] for t in preds]
        for i in range(1, world_size):
            while not osp.exists(osp.join('tmp', f'preds{i}.pkl')):
                time.sleep(1)
            # append
            next_preds = pickle.load(open(osp.join('tmp', f'preds{i}.pkl'), 'rb'))
            for j in range(len(merged_preds)):
                merged_preds[j].append(next_preds[j])
            os.remove(osp.join('tmp', f'preds{i}.pkl'))
        os.remove('tmp/preds0.pkl')
        merged_preds = [torch.cat(t, dim=0) for t in merged_preds]
        num_samples_per_gpu = valid_sampler.num_samples
        for i in range(len(merged_preds)):
            merged_preds[i] = merged_preds[i].reshape(world_size, num_samples_per_gpu, -1).transpose(0, 1).reshape(
                world_size * num_samples_per_gpu, -1).squeeze(-1)[:num_eval]
        learn.data.valid_dl = old_valid_dl
        pickle.dump(merged_preds, open(osp.join('tmp', 'preds.pkl'), 'wb'))
        return merged_preds
    else:
        while not osp.exists(osp.join('tmp', 'preds.pkl')):
            time.sleep(1)
        return pickle.load(open(osp.join('tmp', 'preds.pkl'), 'rb'))
