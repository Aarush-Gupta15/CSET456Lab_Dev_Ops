"""Educational AST path-context representation inspired by Code2Vec.

This is not the original neural Code2Vec architecture: it counts AST ancestor
paths for identifier occurrences to make the structural signal inspectable.
"""
import ast, csv, math, random, sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)
CORPUS=Path("Lab3/Data/source_code_corpus.csv")
OUT=Path("Lab4/Data")
SEED=42

class IdentifierPaths(ast.NodeVisitor):
    def __init__(self): self.stack=[]; self.features=defaultdict(Counter)
    def generic_visit(self,node):
        self.stack.append(type(node).__name__)
        if isinstance(node,ast.Name): self.features[node.id]["/".join(self.stack[-6:])]+=1
        elif isinstance(node,(ast.arg,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            name=node.arg if isinstance(node,ast.arg) else node.name
            self.features[name]["/".join(self.stack[-6:])]+=1
        super().generic_visit(node); self.stack.pop()

def cosine(a,b):
    dot=sum(v*b.get(k,0) for k,v in a.items()); na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return dot/(na*nb) if na and nb else 0.0

def main():
    vectors=defaultdict(Counter); parsed=skipped=non_python=blank=0
    with CORPUS.open(encoding="utf-8",newline="") as f:
        for row in csv.DictReader(f):
            code=row["source_code"]
            if not code.strip(): blank+=1; continue
            if not (row["language"].lower()=="python" or row["extension"].lower()==".py"):
                non_python+=1; continue
            try: tree=ast.parse(code)
            except (SyntaxError,ValueError,TypeError): skipped+=1; continue
            parsed+=1; visitor=IdentifierPaths(); visitor.visit(tree)
            for token,features in visitor.features.items(): vectors[token].update(features)
    selected=random.Random(SEED).sample(sorted(vectors),min(20,len(vectors)))
    pairs=[]
    for i,a in enumerate(selected):
        for b in selected[i+1:]: pairs.append((a,b,cosine(vectors[a],vectors[b])))
    pairs.sort(key=lambda x:x[2],reverse=True); OUT.mkdir(parents=True,exist_ok=True)
    dims=sorted({feature for t in selected for feature in vectors[t]})
    with (OUT/"code2vec_embeddings.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["token"]+dims)
        for t in selected: w.writerow([t]+[vectors[t][d] for d in dims])
    with (OUT/"code2vec_similarity.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["token_1","token_2","cosine_similarity"]); w.writerows((a,b,f"{s:.6f}") for a,b,s in pairs)
    print("===== EDUCATIONAL CODE2VEC-INSPIRED AST PATH EXPERIMENT =====")
    print(f"Python files parsed: {parsed}; parse failures skipped: {skipped}; non-Python records skipped: {non_python}; blank records skipped: {blank}; seed: {SEED}")
    print(f"Selected {len(selected)} identifier tokens; union path-feature dimension: {len(dims)}")
    print("Selected:",", ".join(selected)); print("Top 5 cosine pairs:")
    for i,(a,b,s) in enumerate(pairs[:5],1): print(f"{i}. {a} <-> {b} = {s:.6f}")
    print("Saved Lab4/Data/code2vec_embeddings.csv and code2vec_similarity.csv")

if __name__=="__main__": main()
