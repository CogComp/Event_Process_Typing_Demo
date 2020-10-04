# Semantic Typing of Event Processes (Web Demo Purpose, Not for Release!!!)
This is the repository for the demo backend of CoNLL 2020 Paper "What Are You Trying Todo? Semantic Typing of Event Processes". The opensource git repository (not including the demo backend) is https://github.com/CogComp/Event_Process_Typing  

Environment Setup:
    
    git clone https://github.com/CogComp/EventProcessTyping.git
    cd EventProcessTyping
    conda create --prefix ./STEP_env python=3.7
    conda activate ./STEP_env
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    conda install pytorch torchvision cudatoolkit=10.1 -c pytorch 

    


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

 


