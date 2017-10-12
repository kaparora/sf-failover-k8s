What does this script do?
1) Go through all the PVs in K8S env
2) Filter only iSCSI vols
3) Find the volume with pv name on SolidFire cluster
4) Remove volume pair for this volume
5) Change volume access type to readWrite
6) update iqn and target portal for this PV and replace PV

Steps to execute :
1) Setup your profile with kubernetes and SF details. Edit file named profile (set NO_EXECUTE=true for a dry run)
2) Create your virtualenv: #virtualenv venv
3) Activate your virtualenv: #source venv/bin/activate
4) Install dependencies: #pip install -r requirements.txt
5) Setup Env variables using profile file created in step 1 : #source profile
6) Execute failover script: python failover.py

