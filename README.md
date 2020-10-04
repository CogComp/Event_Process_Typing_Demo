# Semantic Typing of Event Processes (Web Demo Purpose, Not for Release!!!)
This is the repository for the resources in CoNLL 2020 Paper "What Are You Trying Todo? Semantic Typing of Event Processes". This repository contains the source code and links to some datasets used in our paper.

Environment Setup:
    
    git clone https://github.com/CogComp/EventProcessTyping.git
    cd EventProcessTyping
    conda create --prefix ./STEP_env python=3.7
    conda activate ./STEP_env
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    conda install pytorch torchvision cudatoolkit=10.1 -c pytorch 

    
## Dataset  
./data contains the wikiHow Event Process Typing dataset contributed in this work. The same folder also contains verb and noun glosses from WordNet, and the SemCor dataset used for WSD.  
The raw file of wikiHow Event Process Typing dataset is given as data_seq.tsv, where each row records the content and types labels of a process. Specifically, each tab separated row contains a sequence of subevent contents, and the last two cell are the action and object labels.  
The binary file is a saved instance of the data.py object in utils, which has already read the process data and label glosses, and provided necessary indexing information to split, train and test.  
./process archives several programs for dataset proprocessing.  

## Run the experiment  
The program ./run_joint/jointSSmrl_roberta_bias.py runs the experiment for training and testing with excluded 10\% test split. It should execute with the following pattern  

    python jointSSmrl_roberta_bias.py <skip_training> <alpha> <margin_1> <margin_2>  
  
For example:  

    CUDA_VISIBLE_DEVICES=0 python jointSSmrl_roberta_bias.py 0 1. 0.1 0.1
  

## Console demo application  

./run_joint/console_roberta_bias.py is a console application where the user can type in event processes and obtain the multi-axis type information on-the-fly.  Simple run this program, wait until it loads a pre-trained model, and type in an event process where subevents are separated by '@'. For example, the following input   

    read papers@attend conferences@go to seminars@write a thesis
  
would receive type information such as  

    [('get', 0.6021211743354797), ('retain', 0.6217673718929291), ('absorb', 0.6397878527641296), ('pass', 0.6577234268188477), ('submit', 0.6673179864883423), ('present', 0.6688072383403778)] 
    [('doctorate', 0.5141586363315582), ('psychology', 0.5413682460784912), ('genetic', 0.5501004457473755), ('science', 0.5507515966892242), ('determinism', 0.5621879994869232), ('grade', 0.5723227560520172)]

Users can also train the model on the full wikiHow event process dataset by running ./runjoint/train_full_roberta_bias.py 


## For demo developers:
First, our running demo is here: http://dickens.seas.upenn.edu:4035/

Link to the pre-trained full models for console demo: https://drive.google.com/drive/folders/1b8peVVRNANL7r_Wnyyt4pPsyNROIlOfT?usp=sharing  
After putting the file named 

    full_model_sptoken_ep121_a1.0_m1-0.1_m2-0.1.bin
under folder ./run_joint/full_model/

you can run the backend as follows:

    cd run_joint/
    CUDA_VISIBLE_DEVICES=0 nohup python backend.py 0 > nohup.out 2>&1 &
    
After running backend.py, you can check whether backend works with:

    curl -d '{"sequence" : "dig a hole@put some seeds@fill the soil@water the soil"}' -H "Content-Type: application/json" -X POST http://dickens.seas.upenn.edu:4035/annotate/
    
Open url http://dickens.seas.upenn.edu:4035/ in the browser, then you can play with it!

 


## Reference
This work is to be published at the 24th SIGNLL Conference on Computational Natural Language Learning (CoNLL), 2020.  
Bibtex:
  
    @inproceedings{chen-etal-2020-what,
      title = {``What Are You Trying To Do?'' Semantic Typing of Event Processes},
      author = "Chen, Muhao and Zhang, Hongming and Wang, Haoyu and Roth, Dan",
      booktitle = "Proceedings of the 24th Conference on Computational Natural Language Learning (CoNLL)",
      year = "2020",
      publisher = "Association for Computational Linguistics"
    }


