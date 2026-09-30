"""Small educational Skip-gram Word2Vec with negative sampling (NumPy)."""
import csv, math, random, re, sys
from collections import Counter
from pathlib import Path
import numpy as np
csv.field_size_limit(sys.maxsize)
CORPUS = Path("Lab3/Data/source_code_corpus.csv")
OUT = Path("Lab4/Data")
SEED, DIM, WINDOW, MIN_COUNT, EPOCHS, NEGATIVES = 42, 50, 5, 2, 1, 3
MAX_RECORDS, MAX_TOKENS_PER_RECORD, MAX_VOCAB = 300, 120, 10000
PAT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+|==|!=|<=|>=|->|[^\sA-Za-z0-9_]")

def main():
    random.seed(SEED); np.random.seed(SEED)
    sequences=[]
    with CORPUS.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["source_code"].strip():
                seq=PAT.findall(row["source_code"])
                if seq: sequences.append(seq[:MAX_TOKENS_PER_RECORD])
    random.Random(SEED).shuffle(sequences)
    sequences=sequences[:MAX_RECORDS]
    freq=Counter(t for seq in sequences for t in seq)
    vocab=sorted((t for t,n in freq.items() if n >= MIN_COUNT), key=lambda t:(-freq[t],t))[:MAX_VOCAB]
    ids={t:i for i,t in enumerate(vocab)}
    seqs=[[ids[t] for t in seq if t in ids] for seq in sequences]
    dim=len(vocab); rng=np.random.default_rng(SEED)
    w_in=rng.uniform(-0.5/DIM,0.5/DIM,(dim,DIM)).astype(np.float32)
    w_out=np.zeros((dim,DIM),dtype=np.float32)
    distribution=np.array([freq[t]**0.75 for t in vocab],dtype=np.float64); distribution/=distribution.sum()
    print(f"Skip-gram negative sampling; corpus={CORPUS}; records={len(seqs)}; vocab={dim}")
    print(f"seed={SEED}, vector_size={DIM}, window={WINDOW}, min_count={MIN_COUNT}, epochs={EPOCHS}, workers=1, negatives={NEGATIVES}; sampled records={MAX_RECORDS}, token cap/record={MAX_TOKENS_PER_RECORD}, vocabulary cap={MAX_VOCAB}")
    pairs=[(s[i],s[j]) for s in seqs for i in range(len(s)) for j in range(max(0,i-WINDOW),min(len(s),i+WINDOW+1)) if i!=j]
    print(f"Training pairs={len(pairs)}")
    lr0=0.025
    for epoch in range(EPOCHS):
        random.shuffle(pairs)
        for step,(center,context) in enumerate(pairs):
            lr=lr0*(1-0.5*epoch/EPOCHS)
            targets=[(context,1.0)]+[(int(x),0.0) for x in rng.choice(dim,size=NEGATIVES,p=distribution)]
            vin=w_in[center].copy(); grad_in=np.zeros(DIM,dtype=np.float32)
            for target,label in targets:
                vout=w_out[target].copy(); z=float(np.clip(np.dot(vin,vout),-10,10)); pred=1/(1+math.exp(-z))
                g=(label-pred)*lr; grad_in += g*vout; w_out[target] += g*vin
            w_in[center] += grad_in
        print(f"Finished epoch {epoch+1}/{EPOCHS}")
    candidates=[t for t in vocab if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",t)]
    selected=random.Random(SEED).sample(candidates,min(20,len(candidates)))
    vec={t:w_in[ids[t]] for t in selected}
    pairs=[]
    for i,a in enumerate(selected):
        for b in selected[i+1:]:
            x,y=vec[a],vec[b]; den=float(np.linalg.norm(x)*np.linalg.norm(y)); sim=float(np.dot(x,y)/den) if den else 0
            pairs.append((a,b,sim))
    pairs.sort(key=lambda x:x[2],reverse=True); OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/"word2vec_embeddings.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["token"]+[f"dim_{i}" for i in range(DIM)]); w.writerows([t,*vec[t].tolist()] for t in selected)
    with (OUT/"word2vec_model.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["token"]+[f"input_{i}" for i in range(DIM)]+[f"output_{i}" for i in range(DIM)])
        w.writerows([t,*w_in[ids[t]].tolist(),*w_out[ids[t]].tolist()] for t in vocab)
    with (OUT/"word2vec_similarity.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["token_1","token_2","cosine_similarity"]); w.writerows((a,b,f"{s:.6f}") for a,b,s in pairs)
    print("Selected:",", ".join(selected)); print("Top 5:")
    for i,(a,b,s) in enumerate(pairs[:5],1): print(f"{i}. {a} <-> {b} = {s:.6f}")
    print("Saved selected embeddings, all similarities, and full input/output matrices to Lab4/Data/word2vec_model.csv")

if __name__=="__main__": main()
