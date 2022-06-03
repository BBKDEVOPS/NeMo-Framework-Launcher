HYDRA_FULL_ERROR=1 python3 main.py \
    +ci_test=True \
    data_preparation=download_gpt3_pile \
    run_data_preparation=True \
    run_training=False \
    run_conversion=False \
    run_finetuning=False \
    run_evaluation=False \
    bignlp_path=${GIT_CLONE_PATH} \
    data_dir=${BASE_RESULTS_DIR}/data \
    base_results_dir=${BASE_RESULTS_DIR} \
    "container='${BUILD_IMAGE_NAME_SRUN}'" \
    cluster.partition=${SLURM_PARTITION} \
    cluster.account=${SLURM_ACCOUNT} \
    cluster.gpus_per_task=null \
    cluster.gpus_per_node=null \
    cluster.job_name_prefix="${SLURM_ACCOUNT}-bignlp_ci:" \
    data_preparation.log_dir=${RESULTS_DIR} \
    data_preparation.file_numbers="0" \
    data_preparation.preprocess_data=False \
    data_preparation.nodes=1 \
    data_preparation.time_limit="4:00:00"
