# script to run to install the environement in the user directory
# DMD Oct 2020

# see update.sh  for updating an existing account

# first create user (je crois que j'ai les bonnes commandes)
# user new_user - in group newlab and euftgrp

# >> sudo addgroup newlab (par exemple)
# >> sudo adduser new_user --ingroup newlab
# >> sudo adduser new_user euftgrp

# cd to his home dir
# sudo su new_user
# then execute this script 

version="1.00"
echo "web form 2D Installation - version $version"

# clone project
git clone https://github.com/nguacon01/app.git
# create project folder
# mkdir web_form_2D
cd app
# fossil open ../web_form_2D.fossil

# create virtual environment
python3 -m venv web_form_2D 
# activate virtual environment
source web_form_2D/bin/activate

# install requirements
pip install -r requirements.txt

# link EUFT_Spike into app modules
cd casc4de
ln -s ../../../EUFT_Spike .

# Setup environment variables
export FLASK_ENV=production
export SECRET_KEY=DQCQ8585bJCcnTW085X0WHXD0NcMdU0Cv28MvVo8qo0LKBOK9k9uped32A5FqfMjeST11tkQRbNgfpPP17FF5qyegjL3dfeKODhp
export MYSQL_USER=mddo
export MYSQL_PASSWORD=dung123
export MYSQL_HOST=192.168.1.10
export MYSQL_PORT=2361
export MYSQL_DATABASE=web_form_2D


# config Gunicorn and service
sudo cp web_form_2D.service /etc/systemd/system
sudo systemctl start myproject
sudo systemctl enable myproject

# config nginx
sudo cp web_form_2D /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/web_form_2D /etc/nginx/sites-enabled/
sudo systemctl restart nginx