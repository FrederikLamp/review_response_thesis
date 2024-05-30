This repository holds example python code from the scripts used to fine-tune pretrained transformer models for both text 
classification and text generation tasks based on Danish review data collected from Trustpilot.

The TP_scrape.py and concatenate_reviews.py was used in data collection, and the notebooks were used in the text classification, 
text generation, and dataset descriptive statistics tasks, respectively.


Packages & versions I have used during this project:

Python 3.10.6     
transformers 4.41.0.dev0 (source)    
torch 2.2.2    

requests 2.31.0   
Scrapy 2.11.1   

pandas 1.5.3    
scikit-learn 1.2.1    
nltk         3.8.1     
accelerate   0.30.1    
matplotlib   3.6.0    



For transparency regarding fine-tuning of text-generation model, the following terminal prompt was used to 
initiate fine-tuning through terminal:

python3 run_clm.py \
    --model_name_or_path KennethTM/gpt2-small-danish-review-response \
    --train_file  corpus_train_final.txt \
    --validation_file corpus_val_final.txt \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 16 \
    --weight_decay 0.01 \
    --run_name gen_model_r\
    --do_train \
    --do_eval \
    --output_dir gen_model\
    --gradient_checkpointing \
    --num_train_epochs 10 \
    --block_size 256 \
    --logging_dir gen_model_logs \
    --eval_strategy epoch \
    --save_strategy epoch \
    --load_best_model_at_end True \
    --warmup_steps 10 
