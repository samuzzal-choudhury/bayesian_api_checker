import json
import pprint
import requests
import datetime
from termcolor import colored

pp = pprint.PrettyPrinter(indent=2)

f = open('ref_stacks.json','r')
data = json.loads(f.read())

cmd = 'https://recommender.api.prod-preview.openshift.io/api/v1/component-analyses'

tot_tests_run = 0
tot_tests_passed = 0
tot_tests_failed = 0

time_taken_arr = []

for elem in data["result"]["data"]:
    stack_name = elem["stk"]["sname"][0]
    eco = elem["ver"]["pecosystem"][0]
    pkg = elem["ver"]["pname"][0]
    ver = elem["ver"]["version"][0]
    
    url = '{cmd}/{eco}/{pkg}/{ver}'.format(cmd=cmd, eco=eco, pkg=pkg, ver=ver)

    tot_tests_run += 1
    try:
        r = requests.get(url)
    except:
        print ("Error running component analysis of {name}-{ver}".format(name=pkg, ver=ver))
        tot_tests_failed += 1
        continue

    time_taken = r.elapsed.total_seconds()
    time_taken_arr.append(time_taken)

    if r.status_code == 200:
        print ("{stack}: {name}-{ver} run {status}. {time_taken}s".format(stack=stack_name, name=pkg, ver=ver, status=colored('PASSED','green'), time_taken=time_taken))
        tot_tests_passed += 1
    else:
        print ("{stack}: {name}-{ver} run {status}. {time_taken}s".format(stack=stack_name, name=pkg, ver=ver, status=colored('FAILED','red'), time_taken=time_taken))
        tot_tests_failed += 1

avg_time = sum(time_taken_arr)/len(time_taken_arr)

print ("Total tests run: {}".format(tot_tests_run))
print ("Total tests passed: {}".format(tot_tests_passed))
print ("Total tests failed: {}".format(tot_tests_failed))
print ("Average time taken per request: {}".format(str(avg_time)))

