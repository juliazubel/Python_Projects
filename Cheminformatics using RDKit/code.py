import re
from rdkit import Chem
from rdkit.Chem import Draw, rdFMCS, AllChem

def SmiToPDB(smiles_str):
    MolzSmiles = Chem.MolFromSmiles(smiles_str)
    withhydro = Chem.AddHs(MolzSmiles)
    AllChem.EmbedMolecule(withhydro)
    Chem.MolToPDBFile(withhydro, 'plik.pdb')

def PDBToSmi(PDB_fn):
    pdb_mol = Chem.MolFromPDBFile(PDB_fn)
    frags = Chem.GetMolFrags(pdb_mol, asMols=True, sanitizeFrags=False)
    finalsmiles = ''
    for frag in frags:
        smiles = Chem.MolToSmiles(frag)
        if len(smiles) > len(finalsmiles):
            finalsmiles = smiles
    return finalsmiles

def SmiToPNG(smiles_str):
    MolzSmiles = Chem.MolFromSmiles(smiles_str)
    PNG = Draw.rdMolDraw2D.MolDraw2DCairo(300, 300)
    PNG.DrawMolecule(MolzSmiles)
    PNG.FinishDrawing()
    PNG.WriteDrawingText("molecule.png")

#-------------------------------------------------

def MaximumCommonSubstructure(smiles_str1, smiles_str2):
    mols = [Chem.MolFromSmiles(smiles_str1), Chem.MolFromSmiles(smiles_str2)]
    MCS = rdFMCS.FindMCS(mols)
    MolFromSmarts = Chem.MolFromSmarts(MCS.smartsString)
    MolToSmiles = Chem.MolToSmiles(MolFromSmarts)
    print(MolToSmiles)
    SmiToPNG(MolToSmiles)

#-------------------------------------------------

class Molecule:
    def __init__(self):
        self.atoms = []
        self.bonds = []
        self.angles = {}
        self.dihedrals = {}
    
    def fromPDB(self, PDB_fn):
        with open(PDB_fn, 'r') as file:
            for line in file:
                if line.startswith('HETATM'):
                    atom_name = line[12:16].strip()
                    atom_xyz = (float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip()))
                    atom_charge = float(line[78:80].strip()) if line[78:80].strip() != '' else None
                    atom = Atom(atom_name, xyz=atom_xyz, charge=atom_charge)
                    self.atoms.append(atom)

        with open(PDB_fn, 'r') as file:
            for line in file:
                if line.startswith('CONECT'):
                    atoms = line.split()[1:]
                    for i in range(1, len(atoms)):
                        bond = (int(atoms[0]), int(atoms[i]))
                        if bond not in self.bonds:
                            self.bonds.append(bond)
    
    def fromSMILES(self, smiles):
        molecule = Chem.MolFromSmiles(smiles)
        with_hydro = Chem.AddHs(molecule)
        Chem.AllChem.EmbedMolecule(with_hydro)

        for atom in with_hydro.GetAtoms():
            atom_name = atom.GetSymbol()
            atom_charge = atom.GetFormalCharge()
            atom_xyz = atom.GetPos()
            new_atom = Atom(atom_name, xyz=atom_xyz, charge=atom_charge)
            self.atoms.append(new_atom)

        for bond in with_hydro.GetBonds():
            atom1 = bond.GetBeginAtomIdx()
            atom2 = bond.GetEndAtomIdx()
            bond_tuple = (atom1, atom2)
            if bond_tuple not in self.bonds:
                self.bonds.append(bond_tuple)
    
    def getValenceAngles(self):
        angles = []
        for bond1 in self.bonds:
            for bond2 in self.bonds:
                if bond1 == bond2 or bond1[1] != bond2[0]:
                    continue
                atom1, atom2, atom3 = bond1[0], bond1[1], bond2[1]
                angle = (atom1, atom2, atom3)
                if angle not in angles:
                    angles.append(angle)
        self.angles = dict(enumerate(angles, start=1))
        return self.angles

    def getDihedrals(self):
        dihedrals = []
        for bond1 in self.bonds:
            for bond2 in self.bonds:
                if bond1 == bond2:
                    continue
                a, b = bond1
                c, d = bond2
                if b != c:
                    continue
                neighbors = set()
                for bond3 in self.bonds:
                    if bond3 == bond1 or bond3 == bond2:
                        continue
                    if a in bond3:
                        neighbors.add(bond3[0] if bond3[1] == a else bond3[1])
                    if d in bond3:
                        neighbors.add(bond3[0] if bond3[1] == d else bond3[1])
                for e in neighbors:
                    if e > b and e != c:
                        dihedrals.append((a, b, c, e))
        self.dihedrals = dict(enumerate(dihedrals, start=1))
        return self.dihedrals

class Atom:
    def __init__(self, name, **attrs):
        self.name = name
        self.index = int(re.findall(r'\d+', name)[0])
        self.element = re.match(r'[A-Z][a-z]*', name).group()
        self.charge = None
        self.xyz = None
        if 'xyz' in attrs: 
            self.xyz = attrs['xyz']
        if 'charge' in attrs:
            self.charge = attrs['charge']

class Bond:
    def __init__(self):
        self.atoms = None
        self.order = None
        self.index = None
    
    def setBond(self, bond):
        self.atoms = (bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
        self.order = bond.GetBondType()

def get_atomic_mass(element):
    atomic_masses = {
        'H': 1.01,
        'C': 12.01,
        'O': 16.00,
        'N': 14.01,
        'P': 30.97,
        'S': 32.06
    }
    return atomic_masses.get(element, 0.0)
