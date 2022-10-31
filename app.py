
from flask import Flask 
 
app = Flask(__name__)


@app.route('/')
def main():
    # install a custom handler to prevent following of redirects automatically.
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return headers
opener = urllib2.build_opener(SmartRedirectHandler())
urllib2.install_opener(opener)

parameters = {
    'seqdb':'pdb',
    'seq':'>Seq\nKLRVLGYHNGEWCEAQTKNGQGWVPSNYITPVNSLENSIDKHSWYHGPVSRNAAEY'
}
enc_params = urllib.urlencode(parameters)

#post the seqrch request to the server
request = urllib2.Request('https://www.ebi.ac.uk/Tools/hmmer/search/phmmer',enc_params)

#get the url where the results can be fetched from
results_url = urllib2.urlopen(request).getheader('location')

# modify the range, format and presence of alignments in your results here
res_params = {
    'output': 'json',
    'range': '1,10'
}

# add the parameters to your request for the results
enc_res_params = urllib.urlencode(res_params)
modified_res_url = results_url + '?' + enc_res_params

# send a GET request to the server
results_request = urllib2.Request(modified_res_url)
data = urllib2.urlopen(results_request)

# print out the results
return data.read()
     





if(__name__ == "__main__"):
    app.run(debug=True)
