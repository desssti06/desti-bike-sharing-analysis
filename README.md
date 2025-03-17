Dicoding Collection Dashboard Submission

<!-- Setup Environment - Anaconda -->

$env:Path += ";C:\Users\ASUS\Miniconda3\Scripts"
conda create --name main-ds python=3.9
conda activate main-ds
pip install jupyter
pip install -r requirements.txt
~jupyter-notebook .~

<!-- Setup Environment - Shell/Terminal -->

mkdir submission
cd submission
pip install pipenv
pipenv install
pipenv shell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

<!-- Run steamlit app -->

streamlit run dashboard.py
