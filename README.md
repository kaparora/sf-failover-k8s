
What does this script do?
1) Go through all the PVs in K8S env
2) Filter only iSCSI vols
3) Find the volumes with PVs name on SolidFire cluster
4) Remove all volume pair for these volumes
5) Change volume access type to readWrite for all volumes
6) update iqn and target portal for this PV and replace PV

Prerequisites:
1) All primary SolidFire Volumes (corresponiding to PVs in K8S) have a replicated volume on the secondary SolidFire with exactly the same name.
2) The secondary solidFire cluster already has VAGs defined and all volumes are already added to the corresponding VAGs.

Post steps:
* After the script has completed, all pods must be restarted for new iSCSI connections to establish.

Note:
* The script is limited to exactly what it says it does. 


Steps to execute :

* Clone repo
  > git clone https://github.com/kapilarora/sf-failover-k8s.git
* Change directory
  > cd sf-failover-k8s/
* Setup your profile with kubernetes and SF details. Edit file named profile (set NO_EXECUTE=true for a dry run)
* Create your virtualenv: 
  > virtualenv venv
* Activate your virtualenv: 
  > source venv/bin/activate
* Install dependencies: 
  > pip install -r requirements.txt
* Setup Env variables using profile file created in step 1 : 
  > source profile
* Execute failover script:
  > python failover.py

