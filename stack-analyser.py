import json
import pprint
import requests
import datetime
import glob
import os
from termcolor import colored

pp = pprint.PrettyPrinter(indent=2)
req_id_arr = []

def run_test(pom, release):
    url = 'https://recommender.api.openshift.io/api/v1/stack-analyses'
    auth = 'Authorization:Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwbEwwdlhzOVlSVnFaTW93eXc4dU5MUl95cjBpRmFvemRRazlyenEyT1ZVIn0.eyJqdGkiOiJjYTE5ZWRlYy01NDNmLTQwMDQtYWExZi02Mzk3YjFjYTZjN2IiLCJleHAiOjE0OTkzMjM0NDMsIm5iZiI6MCwiaWF0IjoxNDk2NzMxNDQzLCJpc3MiOiJodHRwczovL3Nzby5vcGVuc2hpZnQuaW8vYXV0aC9yZWFsbXMvZmFicmljOCIsImF1ZCI6ImZhYnJpYzgtb25saW5lLXBsYXRmb3JtIiwic3ViIjoiNTAyOTI4ZDAtNmQ1My00YmRlLWJjMjItNWY0ODUxNjBiYjViIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZmFicmljOC1vbmxpbmUtcGxhdGZvcm0iLCJhdXRoX3RpbWUiOjE0OTY3MzE0NDEsInNlc3Npb25fc3RhdGUiOiI1YTg5Y2I3YS1kNDliLTRiYTUtYjczYy00NGJiOTYyYWYzZTkiLCJhY3IiOiIxIiwiY2xpZW50X3Nlc3Npb24iOiIyMWJkZTkxNC1mOGZiLTRhMjQtYTBhOS1lM2MwNjcyZTllZjYiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJicm9rZXIiOnsicm9sZXMiOlsicmVhZC10b2tlbiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwibmFtZSI6IlNhbXV6emFsIENob3VkaHVyeSIsImNvbXBhbnkiOiJSZWQgSGF0IEluZGlhIFB2dCBMdGQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzYW11enphbCIsImdpdmVuX25hbWUiOiJTYW11enphbCIsImZhbWlseV9uYW1lIjoiQ2hvdWRodXJ5IiwiZW1haWwiOiJzYW11enphbEByZWRoYXQuY29tIn0.IlebUwiIiZO13SPbu5VkMrLMXrnuXTxGNBzALH22e6EBe6Es4gtIHc6wG3lUS-hHBZnV3wFsCiJIGcRQzraPnsQWb-O-6IRA39w418M2DaK22lC8qlQrocX11tGAb2pyyQldo4xqPv8QinkSR4k9tnmwA9ue8gO8T198ifkHOP73nLxY_3gQGIUkTI3TAMTnBFqTOUzXKm0bG-FgzKfsvRGjBZFHtztBy7q8nigcN75vWyd4-OPHfKcNil46XdGD1NHVGnmLLya0HNBV8nYIOdgDRFC5GmubD_HRaDLnTWHM6D8lq17yXmVPbk8XU7QO-vLgglAblLcNJOAIJQbjIA'
    f = open('pom.xml','w')
    f.write (pom)
    f.close()

    cmd = 'curl -s -H"{}" -F"manifest[]=@./pom.xml" {}'.format(auth, url)
    try:
        out = os.popen(cmd).read()
        json_out = json.loads(out)
        req_id_arr.append(json_out['id'])
        print ("Stack Analysis request ID for {}: {}".format(release, json_out['id']))
    except:
        print ('command failure for {}'.format(release))

def create_poms():
    f = open('./manifests/pom.xml.template','r')
    pom_template = str(f.read())#.replace("\"","'")
    #print (pom_template)
    dependency_template = "<dependency> <groupId>{group_id}</groupId> <artifactId>{artifact_id}</artifactId> <version>{version}</version> </dependency>"
    file_list = []
    list_maven = glob.glob('manifests/ref_stacks/maven*.json')
    list_springboot = glob.glob('manifests/ref_stacks/springboot*.json')
    file_list.extend(list_maven)
    file_list.extend(list_springboot)

    for filename in file_list:
        dep_list = []
        f = open(filename,'r')
        content = json.loads(f.read())
        release = "{}-{}-{}".format(content['ecosystem'], content['name'], content['version'])
        for key,val in content['dependencies'].items():
            split_key = key.split(":")
            dep = dependency_template.format(group_id=split_key[0], artifact_id=split_key[1], version=val)
            dep_list.append(dep)
        dependencies = ''.join(map(str,dep_list))

        data ={'deps': str(dependencies)}
        pom = pom_template%data
        run_test (pom, release)

create_poms()

tot_tests_run = 0
tot_tests_passed = 0
tot_tests_failed = 0

time_taken_arr = []

