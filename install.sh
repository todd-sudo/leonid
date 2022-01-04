cd
mkdir leonid_bot
cd leonid_bot
git clone https://github.com/todd-sudo/leonid.git
cd leonid
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py