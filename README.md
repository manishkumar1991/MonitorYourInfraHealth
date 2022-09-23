# MonitorYourInfraHealth
This Repo maintains the code base of Linux/Windows health monitoring solution

Get started .
For making this solution works , you need to follow the steps provided below for installation and configuration .

1. You should be having one azure subscription with microsoft sentinel and one workspace enabled reporting to sentinel and some servers connected to that same workspace

### Instalation of custom logs and perf metrics to feed tha data into workbook .
1. Go to workspace settings and then go to agent management and enable all the linux performance counter.
2. Copy the provided three scripts into your server from where you want to collect the metric and schedule them using cron job .
for example : My scripts are locateded in /opt/metric/top_metric.sh
then my crob would be for every two minutes triggering
*/2 * * * * /usr/bin/sh /opt/metric/top_metric.sh >> /path/to/logfile/output.log .
3. Then use that file to enable custom log in custom logs of workspace settings .

![image](https://user-images.githubusercontent.com/97503740/191904556-8977c4cf-7f8e-44f9-a039-c7906fac2234.png)
![image](https://user-images.githubusercontent.com/97503740/191904645-a8e2a4d9-4c06-46be-98a0-388d2e95e318.png)
![image](https://user-images.githubusercontent.com/97503740/191904700-a29bb88a-bb35-4f22-b1d2-7f0acc087adf.png)


### Instalation of workbook 
Copy the workbook content from json file : ServersHealthMonitoringWorkbook.json 
1. Open the sentinel ,
2. Go to Workbooks in left blade
3. Click on Add workbook
4. Click on edit and then go to advance editor
5  Remove the Existing content and paste the content which you copied from ServersHealthMonitoringWorkbook.json in Gallery template .

![image](https://user-images.githubusercontent.com/97503740/191905184-25e917ff-a6f8-4da6-b07c-510ef5ab5ea3.png)
![image](https://user-images.githubusercontent.com/97503740/191905579-0fb24ca3-ff39-4cbb-829a-e19deebd4310.png)

That's it once data starts ingesting in 15 - 20 minutes you would be able to see the workbook getting populated
