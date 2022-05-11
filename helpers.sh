http://178.154.210.253/cplan_ops

http://178.154.210.253/cplan


sudo mysql # MariaDB
use cplan;
SELECT * FROM results LIMIT 1;
SELECT count(*) FROM result WHERE server_state='4'; # pending jobs

bin/create_work --appname example_app --wu_name wu_nodelete --wu_template templates/example_app_in --result_template templates/example_app_out project.xml
https://boinc.berkeley.edu/trac/wiki/JobSubmission

bin/stage_file --copy workunits/stdin
bin/create_work --appname gtcl --wu_name wu_nodelete2 --wu_template templates/gtcl_in --result_template templates/gtcl_out stdin

bin/create_work --appname key_gen --wu_name wu_nodelete --wu_template templates/key_gen_in --result_template templates/key_gen_out

# WITHOUT TEMPLATES (by default it uses templates/ dir)
bin/create_work --appname key_gen --wu_name wu_nodelete15 --verbose

bin/stage_file --copy workunits_spstarter/wu_e43_6_101_13.wu
bin/create_work --appname spstarter --wu_name wu_nodeletespstarter wu_e43_6_101_13.wu

Or

./integrity/integrity_submitter.py --app spstarter --input ./workunits_spstarter/wu_e43_6_101_13.wu

# !IMPORTANT
# add public_key column for user
sudo mysql
use gtcl;
ALTER TABLE host ADD public_key blob NOT NULL DEFAULT '';
# Update public key for example
UPDATE host SET public_key=LOAD_FILE('/tmp/public.key') WHERE id=1;
# Or set it to NULL
UPDATE host SET public_key='' WHERE id=1;

# When rebuilding boinc sources you need to upgrade project
~/boinc-src/tools/upgrade ~/projects/gtcl

#!important in config.xml root dir to assign to hosts!!!
<enable_assignment>1</enable_assignment>


<daemon>
    <cmd>key_gen_assimilator -d 3 -app key_gen</cmd>
</daemon>
<daemon>
    <cmd>script_assimilator -d 3 --app key_gen --script "key_gen_assimilator"</cmd>
</daemon>
<daemon>
    <cmd>sample_bitwise_validator -d 3 --app key_gen</cmd>
</daemon>


# To add new application:
# 1. add it to apps, make version.xml there and etc
# 2. push to project.xml <app>
# 3. make input output templates
# 4. then
./bin/xadd
./bin/update_versions
