# Django Air Pollution Feature: Report Forms
### Technical Design Document

##### Author: Peter Kharlakian  
##### Last Updated: Aug 23 2019


### Objective

In order to implement bigquery for retrieving EPA records, information is required from the user, via a form. 

A user must be able to provide a timeframe and location for records to be queried. 

### Overview

In order to add a form, the following must be implemented

##### `models.py`:

a class, `Report` is made to represent our form in our database

##### `views.py`:

a class, `ReportCreateView`, uses Django's generic CreateView template to handle serving our form, validate inputs, and save it. 

##### `forms.py`:
a class,  `ReportForm` is made to expose fields for the zipcode, start date, and end date from the user.

A `clean()` function exists to ensure that the start date comes before the end date, as validating interdependent fields is traditionally not done in our `views` representation above. 

##### `urls.py`:
The new form paged is served with the `'/new'` url, so urls.py must be updated to add this new route

##### `new_report_form.html`:

A django html template must be made to render the form on the front end

### Security Considerations

Django has robust [built in security features](https://docs.djangoproject.com/en/2.2/topics/security/)

A CSRF token is used on the forms page to prevent cross-site forgery 

Validation of input fields is done on both the front end and backend, incase a manual http request is sent to the server. 


