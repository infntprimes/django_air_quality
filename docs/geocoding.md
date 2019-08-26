# Django Air Pollution Feature: Google Geocoding Integration
### Technical Design Document

##### Author: Peter Kharlakian  
##### Last Updated: Aug 23 2019


### Objective

In order to implement bigquery for retrieving EPA records, a latitude and longitude coordinate are required. However, it's not very user friendly to enter one's location as a lat/long coordinate. 

Instead, we ask the user for a zipcode, and use the geocoding API to get approximate latitude/longitude coordinates for a given zipcode. 
 

### Overview

In order to add the geocoding api, the following must be implemented

##### `geocoding.py`:

A file exists to instantiate a googlemaps Client object, and call queries for a zipcode. The response will contain a json string that captures a latitude/longitude coordinate. Both are returned when the function is executed

When a form is submitted 

### Caching

To avoid unnecessary calls to google's Geocoding API (there are only about 42,000 unique zipcodes), a zipcode's respective latitude/longitude coordinate can be cached so duplicate calls are not made to Google's geocoding API, which saves money and reduces latency.

Unfortunately, zipcode's are subject to change. In the event of a zipcode changing, grace periods are often in place to prevent a zipcode from being reassigned to an entirely new area. A 30-day expiry period on cache presents a fair compromise between unnecessary API calls, and a realiable user experience. 





