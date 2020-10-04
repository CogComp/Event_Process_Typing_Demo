import cherrypy
import torch
print("torch.cuda.is_available(): ", torch.cuda.is_available())
from transformers import RobertaTokenizer, RobertaModel, GPT2Model, RobertaForMultipleChoice
import tqdm, sklearn
import numpy as np
import os, time, sys
import pickle
import multiprocessing
from multiprocessing import Process, Value, Manager
from itertools import chain
import scipy, random
import json
if '../utils' not in sys.path:
    sys.path.append('../utils')
    
from data import Data
from jointSSmrl_roberta_bias import torchpart

### Read parameters ###
if len(sys.argv) > 1:
    debugging = int(sys.argv[1][-1])
### Model Initialization ###
if not debugging:
    data_bin, model_bin = '../data/wikihow_process/data_subsrl_1sv_1sa_argtrim.bin', './full_model/Roberta_BI/full_model_sptoken_ep121_a1.0_m1-0.1_m2-0.1.bin'
    data = Data()

    if os.path.exists(data_bin):
        data.load(data_bin)
        print ("==ATTN== ",len(data.processes)," sequences.")
    else:
        data.load_tsv_plain(data_file)
        data.save(data_bin)

    M = torchpart()
    M.load(model_bin)
    M.serve_verb([' '], data, limit_ids=None, topk=1), M.serve_arg([' '], data, limit_ids=None, topk=1)    
    
### Function ###
def process_json(sequence):
    sequence = sequence.split('@')
    if not debugging:
        vtype, atype = M.serve_verb(sequence, data, limit_ids=None, topk=6, return_emb=False), M.serve_arg(sequence, data, limit_ids=None, topk=6, return_emb=False)
        return {"verb": vtype, "argument": atype}
    else:
        return {"verb": [["grow", 0.4532319903373718], ["bury", 0.46433889865875244], ["cultivate", 0.470214307308197], ["fertilize", 0.5433682799339294], ["propagate", 0.5759392380714417], ["pollinate", 0.5946641862392426]], "argument": [["garden", 0.3294256329536438], ["fertilizer", 0.37675970792770386], ["planting", 0.4205148220062256], ["gardening", 0.4312938451766968], ["clay", 0.4616197943687439], ["pea", 0.49375128746032715]]}

### CherryPy Class Definition ###
class MyWebService(object):
    @cherrypy.expose
    
    def index(self):
        return open('html/index.html')
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()

    def annotate(self):
        hasJSON=True
        result = {"status":"false"}
        try:
            # get input JSON
            data = cherrypy.request.json
        except:
            hasJSON=False
            result = {"error":"invalid input"}

        if hasJSON:
           # process input
           result = process_json(data["sequence"])

        # return resulting JSON
        return result

if __name__ == '__main__':
    print ("")
    print ("Starting rest service...")
    
    config = {'server.socket_host': '0.0.0.0'}
    cherrypy.config.update(config)
    
    config = {
      'global' : {
        'server.socket_host' : 'dickens.seas.upenn.edu',
        'server.socket_port' : 4035,
        'cors.expose.on': True
      },
      '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())

      },
      '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './html'
      },
      '/html' : {
        'tools.staticdir.on'    : True,
        'tools.staticdir.dir'   : './html',  
        'tools.staticdir.index' : 'index.html',
        'tools.gzip.on'         : True  
      }  
    }
    cherrypy.config.update(config)
    #cherrypy.tree.mount(MyWebService()) 
    #cherrypy.engine.start()
    #cherrypy.engine.block()
    cherrypy.quickstart(MyWebService(), '/', config)
