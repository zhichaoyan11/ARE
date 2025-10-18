
# 🧩 Atomic Fact Decomposition Helps Attributed Question Answering

**Accepted by IEEE Transactions on Knowledge and Data Engineering (TKDE) [paper link](https://arxiv.org/abs/2410.16708)**

🚀 *Code is coming soon!*

This repository provides resources for reproducing our  **Fact Decomposition LLM** , proposed in the paper  *"Atomic Fact Decomposition Helps Attributed Question Answering"* .

## 📘 Overview

We introduce an **atomic fact decomposition** framework that improves the reasoning and attribution ability of LLMs in complex question answering tasks.

Our approach decomposes answers into minimal factual units, enhancing faithfulness and interpretability in attribution-aware QA systems.

## ⚙️ Fine-Tuning the Fact Decomposition LLM

To fine-tune the model, we recommend using [**Llama-Factory**](https://github.com/hiyouga/LLaMA-Factory).

We provide:

* ✅ Fine-tuning **settings** (`.yaml` configuration file)
* ✅ Well-constructed **dataset and metadata** (`dataset_info.json`)

You can directly use these files in Llama-Factory to reproduce the  **Fact Decomposition LLM** .

## ⚙️ Full Framework of ARE

You can directly refer the script of [RARR](https://github.com/anthonywchen/RARR) , we also plan release the whole script in few days.

## 📂 Resources

* `fact_decomposition.yaml` — Training configuration for Llama-Factory
* `dataset_info.json` — Dataset description and structure
* `data/` — Coming soon

## 🧠 Citation

If you find our work useful, please cite:


```
@ARTICLE{11159096,
  author={Yan, Zhichao and Wang, Jiapu and Chen, Jiaoyan and Li, Xiaoli and Liang, Jiye and Li, Ru and Pan, Jeff Z.},
  journal={IEEE Transactions on Knowledge and Data Engineering}, 
  title={Atomic Fact Decomposition Helps Attributed Question Answering}, 
  year={2025},
  volume={},
  number={},
  pages={1-14},
  keywords={Question answering (information retrieval);Entropy;Electronic mail;Training;Large language models;Data mining;Timing;Symbols;Search engines;Robustness;Attributed Question Answer;Information Retrieval;Large Language Models},
  doi={10.1109/TKDE.2025.3608716}}
```


## 📅 Coming Soon

* 🧾 Full framework
* 🧠 Pre-trained checkpoints
* 🔍 Evaluation benchmarks
