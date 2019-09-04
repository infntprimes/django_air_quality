# Django Air Pollution Feature: Google Cloud Tasks (Formerly Task Queues)
### Technical Design Document

##### Author: Peter Kharlakian  
##### Last Updated: Aug 30 2019


### Objective

When a user submits a form for a new report, several steps need to be taken before the report is ready, which may take several seconds in total. In a high-traffic environment, it could potentially take minutes for reports to be generated, due to the nature of our GAE tier. 

So, when a user submits a form for a new report, we must queue the creation of a report, such that website responsiveness is not compromised.

Formerly known as task queues, google's python3 app engine environment uses '[cloud tasks](https://cloud.google.com/blog/products/application-development/announcing-cloud-tasks-a-task-queue-service-for-app-engine-flex-and-second-generation-runtimes)'. There are some [differences,](https://cloud.google.com/tasks/docs/migrating) but functionality between the two is fairly similar

 

### Overview

In order to add support for cloud tasks, an API must first be exposed, and a queue initialized. see: ([Quickstart for Cloud Tasks queue](https://cloud.google.com/tasks/docs/quickstart-appengine))

Google cloud tasks works as follows:

Our webpage interacts with googles cloud task queue, and pushes a new 'task', which contains  a payload storing the user's form data. Google's cloud tasks service then sends this request to our web application, which ultimately calls a function to generate a report for a user. 

Cloud tasks has fairly robust built-in support for handling timeouts, failures, and general network errors. ([ref](https://cloud.google.com/tasks/docs/dual-overview#terms))



![527b0fa1.png](:storage/642cad78-48e1-4f80-9d88-67c3a2c6f365/527b0fa1.png)



##### `cloud_tasks/queue_report.py`:

A function exists to take an instance of a Report model, retrieved upon the successful submission of a form from the user. 

From this Report instance, we construct a json string of zipcode, start_date, and end_date. 

We queue a new task that passes this json string to  `/tasks/generate_report/`, and returns

##### `views.py`
A modification is made to our ReportCreateView such that the submission of a successful form invokes `cloud_tasks/queue_report.py`before returning an HTTP response to the user. 

A new function is initialized, `generate_report_handler`, to receive a request from google's cloud task queue. This is ultimately what cloud tasks is queining--calls to this function for each new report that needs to be created. This function will ultimately be expanded to call several modules that run geocoding, bigquery, etc to produce a report and store it in our database.



##### `urls.py`
A new route, `/tasks/generate_report` corresponds to our `generate_report_handler` handler in views.py, that gets hit by google's cloud task call after we've successfully queued a task.

### Performance

There is a slight latency increase when submitting a form, since our ReportCreateView in `views.py` invokes `cloud_tasks/queue_report.py` before returning an HTTP response. This process is ultimately sending an rpc request via google's api to queue our task, but the latency can be well estimated to be < 10 ms, since all modules of our app engine environment are hosted in google's us-central location. 

### Security Concerns

We don't want our `/tasks/generate_report/` route to be publicly accessible, or any malicious actor could make a POST request the same way that google's cloud tasks module does. If manually generated, this request could contain non-valid data, or data that doesn't correspond to any report form's in our database, which could compromise our applications integrity. As a result, we update our app.yaml to require admin access for any `/tasks/*` routes, such that only cloud task's can make successful calls through.
