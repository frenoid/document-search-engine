from crontab import CronTab

def cronJob(username: str) -> None:
    with CronTab(user=username) as cron:
        job = cron.new(command='python3 gcp_to_s3_loader.py')
        
        # Run the job daily
        job.hour.every(24)
    print('cron.write() was just executed')

if __name__ == '__main__':
    print("Starting cron job: GCP_TO_S3_LOADER")
    #placeholder for user
    cronJob("")