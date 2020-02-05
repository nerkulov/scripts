import requests
import os
from bs4 import BeautifulSoup as BS
import sys

def get_html(url):
    return requests.get(url).content

class Problem:
    
    name = None
    link = None
    inputs = None
    outputs = None
    
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.inputs = []
        self.outputs = []
        
    def find_inputs(self):
        sp = BS(get_html(self.link), "html.parser")
        sample_tests = sp.select("div.sample-tests")[0]
        inputs = sample_tests.select(".input")
        for inp in inputs:
            pre = inp.find("pre")
            self.inputs.append(pre.text)
        
    def get_inputs(self):
        if self.inputs == []:
            self.find_inputs()
        return self.inputs
        
    def find_outputs(self):
        sp = BS(get_html(self.link), "html.parser")
        sample_tests = sp.select("div.sample-tests")[0]
        outputs = sample_tests.select(".output")
        for out in outputs:
            pre = out.find("pre")
            self.outputs.append(pre.text)
        
    def get_outputs(self):
        if self.outputs == []:
            self.find_outputs()
        return self.outputs
        
        
class Contest:
    
    id = None
    problems = None
    base_url = "http://codeforces.com/contest/"
    
    def __init__(self, id):
        self.id = id
        self.problems = []
        
    def find_problems(self):
        sp = BS(get_html(self.base_url + self.id), "html.parser")
        table = sp.select("table.problems")[0]
        trs = table.select("tr")[1:]
        for tr in trs:
            td = tr.find("td")
            a = td.find("a")
            name = a.text.strip()
            link = "http://codeforces.com" + a.attrs.get("href")
            obj = Problem(a.text.strip().lower(), link)
            self.problems.append(obj)
        
    def get_problems(self):
        if self.problems == []:
            self.find_problems()
        return self.problems
        
    def make_folders(self):
        os.system("rm -rf {}".format(self.id))
        for prob in self.problems:
            os.system("mkdir -p {}/{}".format(self.id, prob.name))

    def make_tpls(self):
        from os.path import expanduser
        home = expanduser("~")
        with open("{}/tpl.cpp".format(home), "r") as tpl:
            for prob in self.problems:
                with open("{}/{}/{}.cpp".format(self.id, prob.name, prob.name), "w") as tpl_file:
                    tpl_file.write(tpl.read())
    
    def make_inputs(self):
        for prob in self.problems:
            case = 0
            for inp in prob.get_inputs():
                with open("{}/{}/in{}".format(self.id, prob.name, str(case)), "w") as wr:
                    wr.write(inp)
                    case += 1
        
    def make_outputs(self):
        for prob in self.problems:
            case = 0
            for out in prob.get_outputs():
                with open("{}/{}/out{}".format(self.id, prob.name, str(case)), "w") as wr:
                    wr.write(out)
                    case += 1
    
def start():
    contest_id = sys.argv[1]
    obj = Contest(contest_id)
    obj.find_problems()
    obj.make_folders()
    obj.make_tpls()
    obj.make_inputs()
    obj.make_outputs()

if __name__ == '__main__':
    start()
