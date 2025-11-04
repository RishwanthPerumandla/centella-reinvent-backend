try:
    from rdkit import Chem
    from rdkit.Chem import rdMolStandardize
    _HAS_RDKIT = True
except Exception:
    _HAS_RDKIT = False

def largest_fragment_smiles(smi: str) -> str:
    s = "".join(smi.split())
    parts = s.split(".")
    inorganic = {"Cl","Br","F","I","[Cl-]","[Br-]","[F-]","[I-]","[Na+]","[K+]","[Li+]","[Ca+2]","[Mg+2]","[Zn+2]","[NH4+]"}
    def score(p):
        try:
            m = Chem.MolFromSmiles(p, sanitize=False)
            if not m: return (-1, p)
            Chem.SanitizeMol(m, catchErrors=True)
            if p in inorganic: return (0, p)
            return (m.GetNumHeavyAtoms(), p)
        except:
            return (-1, p)
    return sorted(parts, key=score, reverse=True)[0]

def neutralize(mol):
    uncharger = rdMolStandardize.Uncharger()
    mol = uncharger.uncharge(mol)
    return rdMolStandardize.Cleanup(mol)

def clean_one(smi: str) -> str:
    core = largest_fragment_smiles(smi)
    m = Chem.MolFromSmiles(core)
    if not m:
        return ""
    m = neutralize(m)
    te = rdMolStandardize.TautomerEnumerator()
    m = te.Canonicalize(m)
    return Chem.MolToSmiles(m, canonical=True)
