# Background Workers

For our background workers, we'll be creating simple scripts and telling Kubernbetes to run them periodically. This means that the "tasks" will be a basic Python (or another language) script rather than a full fledged server with schedulers. The steps to create a background worker is listed below:

1. Create a script
2. Containerize that script and push the image into a registory
3. Config kubernetes to run the script (it's image) on a scheduled basis

## More info/examples

- [Running Automated Tasks with a CronJob](https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/)
- [Database Backup with Kubernetes Cron Job](https://omegion.dev/2021/02/database-backup-with-kubernetes-cron-job/)
- [What Are Kubernetes Jobs and Cronjobs? (Video)](https://www.youtube.com/watch?v=OZAhYSDkhsI)
- [Explained K8's Cronjob in 15 Mins with Hand-On Python Script! (Video)](https://www.youtube.com/watch?v=zSgEVE-R4f8)
