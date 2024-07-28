# Fairth
_Fairth_ literally meaning _A Picture Taken By Magical Means On A Shingle Of Slate_ (in Ancient Language) is a method to generate photographs using magic in Christopher Paolini's Inheritance Cycle.


## Intro
A tool to query [IPinfo.io](https://ipinfo.io/)'s public APIs with bulk IP addresses and receive Geolocation data for said IPs. Currently tested with their free plan which includes the geolocation information for an IP address and basic ASN details with an additional field in case IP is anycast/bogon.

In addition, it generates a heatmap/visual overview of those IPs with following criteria [No API credits required]:
1. Location,
2. IP types and privacy statutes,
3. Top ASNs and companies they belong to,
4. Top countries, and cities. 

### Sample output
```json
{
  "ip": "1.1.1.1",
  "hostname": "one.one.one.one",
  "anycast": true,
  "city": "Brisbane",
  "region": "Queensland",
  "country": "AU",
  "loc": "-27.4820,153.0136",
  "org": "AS13335 Cloudflare, Inc.",
  "postal": "4101",
  "timezone": "Australia/Brisbane",
}
```

## Installation
Since an additional package (_ipinfo_) is required from PyPI which in turn installs several other packages, use of Virtual Environment is recommended to prevent system libraries from breaking.

```bash
git clone https://github.com/wand3rlust/Fairth.git
cd Fairth
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Usage
The script is very simple and just needs executable permissions or being called with Python 3 binary. Tested on Python 3.11.

Input file should have IPs one per line as shown below
```bash
1.1.1.1
1.0.0.1
```

### Execution

`./fairth.py` [only with executable permissions]

OR

`python3 fairth.py`


## Contributing
I have created this for my personal research purposes and hoping to turn it into a Threat Intel(ish) tool at some point in future. 


Contributions are most welcome if they can increase the functionality or fix some bugs. 

To contribute simply fork this repo, make changes and create a pull request.

## Support

If you like this tool please consider giving a :star:.
