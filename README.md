Dicoding Collection Dashboard Submission

<!-- Setup Environment - Anaconda -->
conda create --name main-ds python=3.9
conda init
conda activate main-ds
pip install jupyter
pip install -r requirements.txt
jupyter-notebook .

<!-- Setup Environment - Shell/Terminal -->

mkdir desti-bike-sharing-analysis
cd desti-bike-sharing-analysis
pip install pipenv
pipenv install
pipenv shell
pip install pipreqs
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

<!-- Run steamlit app -->

streamlit run dashboard.py
