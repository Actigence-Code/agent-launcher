# Guide de Publication Actigence Code

**Guide complet pour créer, développer et publier un projet open source sous la marque Actigence**

---

## 📋 Table des Matières

1. [Préparation du Projet](#1-préparation-du-projet)
2. [Structure du Projet](#2-structure-du-projet)
3. [Branding Actigence](#3-branding-actigence)
4. [Configuration Git & GitHub](#4-configuration-git--github)
5. [Publication sur PyPI](#5-publication-sur-pypi)
6. [Maintenance et Mises à Jour](#6-maintenance-et-mises-à-jour)

---

## 1. Préparation du Projet

### 1.1 Créer la Structure de Base

```bash
# Créer le répertoire du projet
mkdir /home/debian/mon-projet
cd /home/debian/mon-projet

# Créer un environnement virtuel Python
python3 -m venv venv
source venv/bin/activate

# Installer les outils de build
pip install --upgrade build twine
```

### 1.2 Fichiers Obligatoires

Chaque projet Actigence doit contenir **au minimum** :

- `README.md` - Documentation principale
- `LICENSE` - Licence MIT avec copyright Actigence
- `CHANGELOG.md` - Historique des versions
- `pyproject.toml` - Configuration du package Python
- `setup.py` - Compatibilité pip (optionnel mais recommandé)
- `.gitignore` - Fichiers à ignorer
- `CONTRIBUTING.md` - Guide pour contributeurs
- `MANIFEST.in` - Fichiers à inclure dans la distribution

---

## 2. Structure du Projet

### 2.1 Organisation des Fichiers

```
mon-projet/
├── mon_script.py              # Script principal
├── README.md                  # Documentation
├── LICENSE                    # Licence MIT
├── CHANGELOG.md               # Historique
├── pyproject.toml             # Config PyPI
├── setup.py                   # Setup Python
├── MANIFEST.in                # Distribution
├── CONTRIBUTING.md            # Guide contributeurs
├── .gitignore                 # Git ignore
├── .github/
│   └── workflows/
│       ├── test.yml          # Tests CI/CD
│       └── publish.yml       # Publication auto
└── docs/
    └── PUBLISHING.md         # Guide publication
```

### 2.2 Arborescence Recommandée

```bash
# Structure pour un package plus complexe
mon-projet/
├── mon_projet/              # Package principal
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── tests/                   # Tests unitaires
│   ├── __init__.py
│   └── test_core.py
├── docs/                    # Documentation
├── examples/                # Exemples d'utilisation
└── (fichiers racine)
```

---

## 3. Branding Actigence

### 3.1 Script Principal (Python)

**En-tête obligatoire dans TOUS les scripts Python :**

```python
#!/usr/bin/env python3
"""
Nom du Projet - Description courte

English:
    Description détaillée en anglais du projet et de ses fonctionnalités.
    Expliquer le cas d'usage principal.

Français :
    Description détaillée en français du projet et de ses fonctionnalités.
    Expliquer le cas d'usage principal.

Made with ❤️ in Tervuren, Belgium
Copyright (c) 2025 Actigence Management Consulting
Website: https://actigence.eu
Contact: hello@actigence.eu
"""

__version__ = "1.0.0"
__author__ = "Actigence Management Consulting"
__email__ = "hello@actigence.eu"
__url__ = "https://actigence.eu"

# Imports et code...
```

### 3.2 README.md

**Structure obligatoire du README :**

```markdown
# Nom du Projet 🚀

**Description courte** - Une ligne qui explique le projet

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nom-projet.svg)](https://pypi.org/project/nom-projet/)

## ✨ Features

- Liste des fonctionnalités principales
- Pourquoi ce projet est utile
- Cas d'usage

## 📦 Installation

### Via pip (Recommandé)

```bash
pip install nom-projet
```

### Via GitHub

```bash
pip install git+https://github.com/Actigence-Code/nom-projet.git
```

### Depuis les sources

```bash
git clone https://github.com/Actigence-Code/nom-projet.git
cd nom-projet
pip install -e .
```

## 🚀 Quick Start

```bash
# Exemple d'utilisation basique
nom-projet --help
```

## 📚 Documentation

[Lien vers documentation complète si disponible]

## 🤝 Contributing

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

Ce projet est sous licence MIT - voir [LICENSE](LICENSE)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Actigence-Code/nom-projet/issues)
- **Email**: [hello@actigence.eu](mailto:hello@actigence.eu)
- **Website**: [actigence.eu](https://actigence.eu)

---

**Made with ❤️ in Tervuren, Belgium**

[Actigence Management Consulting](https://actigence.eu) | [hello@actigence.eu](mailto:hello@actigence.eu)
```

### 3.3 LICENSE

**Licence MIT avec copyright Actigence :**

```text
MIT License

Copyright (c) 2025 Actigence Management Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 3.4 pyproject.toml

**Configuration complète avec branding Actigence :**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "nom-projet"
version = "1.0.0"
description = "Description courte du projet"
readme = "README.md"
authors = [
    {name = "Actigence Management Consulting", email = "hello@actigence.eu"}
]
maintainers = [
    {name = "Actigence Management Consulting", email = "hello@actigence.eu"}
]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development",
    "Topic :: Utilities",
]
keywords = [
    "mot-clé-1",
    "mot-clé-2",
    "actigence",
]
requires-python = ">=3.8"
dependencies = [
    # Dépendances si nécessaires
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "flake8>=6.0",
]

[project.urls]
Homepage = "https://actigence.eu"
Documentation = "https://github.com/Actigence-Code/nom-projet#readme"
Repository = "https://github.com/Actigence-Code/nom-projet.git"
"Bug Tracker" = "https://github.com/Actigence-Code/nom-projet/issues"
Changelog = "https://github.com/Actigence-Code/nom-projet/blob/main/CHANGELOG.md"
"Source Code" = "https://github.com/Actigence-Code/nom-projet"

[project.scripts]
nom-commande = "module:fonction_main"

[tool.setuptools]
py-modules = ["nom_module"]
```

**⚠️ Points Critiques :**

1. **Homepage** DOIT être `https://actigence.eu`
2. **Authors/Maintainers** DOIVENT être "Actigence Management Consulting"
3. **Email** DOIT être `hello@actigence.eu`
4. **Repository** DOIT être sous `Actigence-Code` organization

### 3.5 CHANGELOG.md

**Format standard pour l'historique :**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-23

### Added
- Fonctionnalité 1
- Fonctionnalité 2
- Documentation complète

### Changed
- Amélioration X
- Optimisation Y

### Fixed
- Correction du bug Z

## [0.9.0] - 2025-11-20

### Added
- Version initiale
```

---

## 4. Configuration Git & GitHub

### 4.1 Initialisation Git

```bash
cd /home/debian/mon-projet

# Configurer Git avec les infos Actigence
git config --global user.email "laurent@actigence.eu"
git config --global user.name "Laurent"

# Initialiser le dépôt
git init
git branch -M main

# Créer .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
.pytest_cache/
.coverage
htmlcov/
EOF

# Premier commit
git add .
git commit -m "feat: initial commit - project setup

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 4.2 Créer le Repository GitHub

**Via l'interface web :**

1. Aller sur https://github.com/organizations/Actigence-Code/repositories/new
2. **Repository name** : `nom-projet`
3. **Description** : Description courte du projet
4. **Visibility** : Public
5. **Ne PAS** initialiser avec README (déjà créé localement)
6. Créer le repository

**Ou via GitHub CLI :**

```bash
# Installer gh si pas déjà fait
sudo apt install gh -y

# S'authentifier
gh auth login

# Créer le repo dans l'organisation
gh repo create Actigence-Code/nom-projet \
  --public \
  --description "Description du projet" \
  --source=. \
  --remote=origin \
  --push
```

### 4.3 Configurer le Repository

**Via GitHub CLI :**

```bash
# Rendre public et configurer
gh repo edit Actigence-Code/nom-projet \
  --visibility public \
  --accept-visibility-change-consequences \
  --description "🚀 Description du projet avec emoji" \
  --add-topic python \
  --add-topic cli \
  --add-topic actigence \
  --add-topic automation \
  --enable-issues \
  --enable-wiki
```

**Ou via interface web :**

1. Aller dans **Settings** du repo
2. **General** :
   - Description : Ajouter description avec emoji
   - Topics : Ajouter tags pertinents + "actigence"
   - Features : Activer Issues, Wiki, Discussions
3. **Collaborators** : Ajouter membres de l'équipe si nécessaire

### 4.4 Pousser le Code

```bash
# Ajouter le remote (si pas fait via gh)
git remote add origin git@github.com:Actigence-Code/nom-projet.git

# Configurer SSH si nécessaire
ssh-keyscan github.com >> ~/.ssh/known_hosts

# Pousser le code
git push -u origin main

# Créer le premier tag
git tag v1.0.0
git push origin v1.0.0
```

### 4.5 GitHub Actions (CI/CD)

**Créer `.github/workflows/test.yml` :**

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Run tests
      run: |
        pytest --cov=nom_projet --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.python-version == '3.11'
```

**Créer `.github/workflows/publish.yml` :**

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

---

## 5. Publication sur PyPI

### 5.1 Créer un Compte PyPI

1. Aller sur https://pypi.org/account/register/
2. Utiliser l'email : **hello@actigence.eu** (ou personnel)
3. Vérifier l'email
4. Activer 2FA (recommandé)

### 5.2 Créer un API Token

1. Aller sur https://pypi.org/manage/account/token/
2. **Token name** : `actigence-nom-projet`
3. **Scope** : "Entire account" (pour premier package)
4. Créer et **COPIER LE TOKEN IMMÉDIATEMENT**

### 5.3 Configurer le Token Localement

**Méthode sécurisée via .pypirc :**

```bash
# Créer le fichier de config
cat > ~/.pypirc << 'EOFPYPI'
[pypi]
username = __token__
password = pypi-VOTRE_TOKEN_ICI
EOFPYPI

# Sécuriser le fichier
chmod 600 ~/.pypirc
```

**Vérifier les permissions :**

```bash
ls -la ~/.pypirc
# Doit afficher : -rw------- (600)
```

### 5.4 Build et Publication

```bash
cd /home/debian/mon-projet

# Activer l'environnement virtuel
source venv/bin/activate

# Nettoyer les builds précédents
rm -rf dist build *.egg-info

# Construire le package
python -m build

# Vérifier le package
twine check dist/*

# IMPORTANT : Vérifier les fichiers avant upload
ls -lh dist/
# Doit contenir :
# - nom_projet-X.Y.Z-py3-none-any.whl
# - nom_projet-X.Y.Z.tar.gz

# Uploader sur PyPI
twine upload dist/*
```

**Output attendu :**

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading nom_projet-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uploading nom_projet-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View at:
https://pypi.org/project/nom-projet/1.0.0/
```

### 5.5 Créer une GitHub Release

**Via GitHub CLI :**

```bash
gh release create v1.0.0 \
  --title "🚀 Nom du Projet v1.0.0 - Initial Release" \
  --notes "## 🎉 First Release!

**Description du projet**

### ✨ Features

- Fonctionnalité 1
- Fonctionnalité 2
- Fonctionnalité 3

### 📦 Installation

\`\`\`bash
pip install nom-projet
\`\`\`

### 🚀 Quick Start

\`\`\`bash
nom-commande --help
\`\`\`

---

Made with ❤️ in Tervuren, Belgium by [Actigence Management Consulting](https://actigence.eu)
" \
  dist/nom_projet-1.0.0-py3-none-any.whl \
  dist/nom_projet-1.0.0.tar.gz
```

**Ou via interface web :**

1. Aller sur https://github.com/Actigence-Code/nom-projet/releases/new
2. **Tag** : v1.0.0
3. **Title** : 🚀 Nom du Projet v1.0.0 - Initial Release
4. **Description** : Copier le template ci-dessus
5. **Attach binaries** : Uploader les fichiers .whl et .tar.gz
6. Publish release

---

## 6. Maintenance et Mises à Jour

### 6.1 Workflow de Mise à Jour

**Pour chaque nouvelle version :**

```bash
# 1. Faire les modifications nécessaires
vim mon_script.py

# 2. Mettre à jour la version
# Dans pyproject.toml :
version = "1.1.0"

# Dans le script principal :
__version__ = "1.1.0"

# 3. Mettre à jour CHANGELOG.md
# Ajouter la section [1.1.0] avec les changements

# 4. Nettoyer et rebuild
rm -rf dist build *.egg-info
source venv/bin/activate
python -m build

# 5. Vérifier
twine check dist/*

# 6. Commit et tag
git add -A
git commit -m "release: version 1.1.0

- Changement 1
- Changement 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git tag v1.1.0
git push origin main
git push origin v1.1.0

# 7. Publier sur PyPI
twine upload dist/*

# 8. Créer GitHub Release
gh release create v1.1.0 \
  --title "🚀 Nom du Projet v1.1.0" \
  --notes-file RELEASE_NOTES.md \
  dist/*
```

### 6.2 Versioning Sémantique

**Format : MAJOR.MINOR.PATCH**

- **MAJOR** (1.x.x) : Changements incompatibles avec versions précédentes
- **MINOR** (x.1.x) : Nouvelles fonctionnalités compatibles
- **PATCH** (x.x.1) : Corrections de bugs

**Exemples :**

- `1.0.0` → `1.0.1` : Bug fix
- `1.0.1` → `1.1.0` : Nouvelle fonctionnalité
- `1.1.0` → `2.0.0` : Breaking change

### 6.3 Messages de Commit Standards

**Format Conventional Commits :**

```
type(scope): description courte

Description détaillée optionnelle

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types :**

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation uniquement
- `style`: Formatage, points-virgules, etc.
- `refactor`: Refactoring sans changer le comportement
- `test`: Ajout/modification de tests
- `chore`: Maintenance, config, etc.
- `release`: Nouvelle version

**Exemples :**

```bash
git commit -m "feat: add support for JSON export

Allow users to export data in JSON format using --format json flag.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git commit -m "fix: handle empty input gracefully

Previously crashed when input was empty. Now returns friendly error.

Fixes #42

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git commit -m "docs: update installation instructions

Added pip install method and troubleshooting section.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 7. Checklist de Publication

### ✅ Avant la Première Publication

- [ ] Projet créé dans `/home/debian/nom-projet`
- [ ] Environnement virtuel créé et activé
- [ ] Tous les fichiers obligatoires créés (voir section 1.2)
- [ ] Branding Actigence dans tous les fichiers (voir section 3)
- [ ] `pyproject.toml` correctement configuré
- [ ] `README.md` complet et structuré
- [ ] `LICENSE` avec copyright Actigence
- [ ] `CHANGELOG.md` initialisé
- [ ] `.gitignore` créé
- [ ] Git configuré avec `laurent@actigence.eu`
- [ ] Premier commit effectué
- [ ] Repository GitHub créé dans Actigence-Code
- [ ] Repository configuré (description, topics, etc.)
- [ ] Code poussé sur GitHub
- [ ] Tag v1.0.0 créé
- [ ] Compte PyPI créé
- [ ] Token PyPI généré et sécurisé
- [ ] Package built (`python -m build`)
- [ ] Package vérifié (`twine check`)
- [ ] Package uploadé sur PyPI
- [ ] GitHub Release créée

### ✅ Pour Chaque Nouvelle Version

- [ ] Modifications de code effectuées
- [ ] Version mise à jour dans `pyproject.toml`
- [ ] Version mise à jour dans le script principal
- [ ] `CHANGELOG.md` mis à jour
- [ ] Tests effectués (si tests disponibles)
- [ ] Build nettoyé (`rm -rf dist build *.egg-info`)
- [ ] Nouveau build créé (`python -m build`)
- [ ] Package vérifié (`twine check dist/*`)
- [ ] Commit créé avec message conventionnel
- [ ] Tag vX.Y.Z créé
- [ ] Code et tag poussés sur GitHub
- [ ] Package uploadé sur PyPI
- [ ] GitHub Release créée avec binaires

---

## 8. Troubleshooting

### Problème : Token PyPI refusé

**Solution :**

```bash
# Vérifier le format du token
cat ~/.pypirc
# username DOIT être : __token__
# password DOIT commencer par : pypi-

# Recréer le token sur PyPI si nécessaire
```

### Problème : Build échoue

**Solution :**

```bash
# Vérifier pyproject.toml
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"

# Vérifier les imports
python -c "import mon_module"

# Nettoyer et rebuilder
rm -rf dist build *.egg-info __pycache__
python -m build
```

### Problème : Git push refuse (no permission)

**Solution :**

```bash
# Vérifier SSH key
ssh -T git@github.com

# Ajouter la clé SSH sur GitHub si nécessaire
cat ~/.ssh/id_ed25519.pub
# Copier et ajouter sur : https://github.com/settings/ssh/new

# Accepter le fingerprint GitHub
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

### Problème : Package name déjà pris sur PyPI

**Solution :**

1. Choisir un nom unique (ex: `actigence-nom-projet`)
2. Mettre à jour `name` dans `pyproject.toml`
3. Mettre à jour `[project.scripts]` si nécessaire
4. Rebuild et uploader

---

## 9. Standards Actigence

### 9.1 Nommage

**Repositories GitHub :**
- Tout en minuscules
- Séparés par des tirets
- Format : `nom-descriptif`
- Exemples : `agent-launcher`, `config-manager`, `data-processor`

**Packages PyPI :**
- Tout en minuscules
- Séparés par des tirets
- Préfixe `actigence-` si nom générique
- Exemples : `agent-launcher`, `actigence-tools`

**Modules Python :**
- Tout en minuscules
- Séparés par des underscores
- Format : `nom_module`
- Exemples : `agent_launcher`, `config_manager`

### 9.2 Documentation

**Langue :**
- README principal : Bilingue (EN + FR) ou Anglais uniquement
- Docstrings : Bilingue quand possible
- Comments : Français acceptable pour code interne

**Structure README :**
1. Titre + badges
2. Description courte
3. Features
4. Installation (pip en premier)
5. Quick Start
6. Documentation détaillée (ou lien)
7. Contributing
8. License
9. Support (avec hello@actigence.eu)
10. Footer Actigence

### 9.3 Qualité du Code

**Standards :**
- Python 3.8+ minimum
- PEP 8 compliant
- Type hints quand possible
- Docstrings pour fonctions publiques
- Tests unitaires recommandés

**Outils recommandés :**

```bash
# Formatter
pip install black
black mon_script.py

# Linter
pip install flake8
flake8 mon_script.py

# Type checker
pip install mypy
mypy mon_script.py

# Tests
pip install pytest pytest-cov
pytest --cov=mon_module
```

---

## 10. Template de Projet

**Pour créer rapidement un nouveau projet :**

```bash
#!/bin/bash
# create_actigence_project.sh

PROJECT_NAME=$1
MODULE_NAME=$(echo $PROJECT_NAME | tr '-' '_')

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./create_actigence_project.sh nom-projet"
    exit 1
fi

# Créer structure
mkdir -p "$PROJECT_NAME"/{docs,.github/workflows}
cd "$PROJECT_NAME"

# Créer fichiers de base
cat > "${MODULE_NAME}.py" << 'EOF'
#!/usr/bin/env python3
"""
PROJECT_NAME - Description courte

Made with ❤️ in Tervuren, Belgium
Copyright (c) 2025 Actigence Management Consulting
Website: https://actigence.eu
Contact: hello@actigence.eu
"""

__version__ = "1.0.0"
__author__ = "Actigence Management Consulting"
__email__ = "hello@actigence.eu"
__url__ = "https://actigence.eu"

def main():
    print("Hello from PROJECT_NAME!")

if __name__ == "__main__":
    main()
EOF

# Remplacer PROJECT_NAME
sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" "${MODULE_NAME}.py"

# Créer pyproject.toml, README, etc.
# (Copier les templates des sections précédentes)

echo "✅ Projet $PROJECT_NAME créé avec succès !"
echo "📂 cd $PROJECT_NAME"
```

---

## 11. Ressources

### Documentation Officielle

- **Python Packaging** : https://packaging.python.org/
- **PyPI Help** : https://pypi.org/help/
- **GitHub Docs** : https://docs.github.com/
- **Semantic Versioning** : https://semver.org/
- **Keep a Changelog** : https://keepachangelog.com/
- **Conventional Commits** : https://www.conventionalcommits.org/

### Outils Actigence

- **Agent Launcher** : https://github.com/Actigence-Code/agent-launcher
- **Templates** : (À créer)

### Contact

- **Email** : hello@actigence.eu
- **Website** : https://actigence.eu
- **GitHub** : https://github.com/Actigence-Code

---

## 12. Historique du Document

| Version | Date       | Auteur   | Changements                    |
|---------|------------|----------|--------------------------------|
| 1.0.0   | 2025-11-23 | Laurent  | Version initiale complète      |

---

**Made with ❤️ in Tervuren, Belgium**

[Actigence Management Consulting](https://actigence.eu) | [hello@actigence.eu](mailto:hello@actigence.eu)
