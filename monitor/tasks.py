from api.models import Url, Warning
import requests
from celery import shared_task

@shared_task(name="url_monitor")
def monitor_urls():
    # Get all urls
    urls = Url.objects.all()
    failed = True
    for url in urls:
        # Check if we can get a response from the url
        result_code = 0
        try:
            response = requests.head(url.url)
            if response.status_code // 100 != 2:
                # if the response is not 2xx then increase the failed times
                url.failed_times += 1
                url.save()
                result_code = response.status_code
            else:
                failed = False
        except:
            # if we can't get a response then increase the failed times and create a warning with result_code -1
            url.failed_times += 1
            url.save()
            result_code = -1
        
        if not failed:
            continue
        
        if url.url.failed_times > url.threshold:
            # if the failed times is greater than the threshold then create a warning with result_code 0
            Warning.objects.create(url=url, result_code=result_code)
        

