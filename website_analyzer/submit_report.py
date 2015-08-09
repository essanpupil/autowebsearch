import requests


def report_worpdress(hp_id):
    "function to submit website to wordpress, based-on: 9-agu-205"
    report_url = "https://wordpress.com/abuse/"
    report_data = {
            'report_email': "pupil@linuxemergency.com",
            'report_url': 'https://pemenangtelkomselpoin2015.wordpress.com/',
            'confirm-spam': "This websites is a scam, the original site is http://www.telkomsel.com/",
            'type': 'copyright'}
    r = requests.get("report_url", report_data)
    with open("request_results.html", "w") as f:
        f.write(r.content)
