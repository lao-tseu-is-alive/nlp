python -c "from transformers import pipeline; print(pipeline('sentiment-analysis')('we love you'))"
echo "It should download a pretrained model then print something like:"
echo "[{'label': 'POSITIVE', 'score': 0.9998704791069031}]"