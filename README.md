---
authors:
- Lucas Mazariegos Arraiza <lmazariegos@nextdigital.es>
created_at: 2021-07-01 00:00:00
tags:
- k8s
- kubernetes
- smart
- fastapi
- python
thumbnail: 
title: Orchestrator API microservice Documentation
tldr: This post contains the documentation of the Orchestrator API microservice
updated_at: 2021-07-01 00:00:00.000000
---

# Table of Contents

1. Document Control
    1. About this document
        1. Purpose
        2. Audience
        3. Document scope
    2. Version History
2. Introduction
    1. Overview of the System, Application or Subject Area
    2. Scope of This Document
        1. In Scope
        2. Out of Scope
3. Key Points
4. Source Systems & API Endpoints
    1. SMART Database
    2. API Endpoints
    3. Sample Request/Response
5. Code Walkthrough
6. Queries
7. Kubernetes YAMLs
8. Deployment Process
    1. Build
    2. Deploy
    3. Test
    4. Load Testing
9. Troubleshooting
    1. Main contacts
    2. Error-01
    3. Error-02
    4. Error-03
    5. Error-04
    6. Error-05

# 1. Document Control

## 1.1 About this Document

### 1.1.1 Purpose

This document will be used to describe the implementation detals for the orchestrator microservice and the expected housekeeping tasks.

### 1.1.2 Audience

This document is intended for the following audience:

- Development Leads
- Data Engineers
- Support Team

### 1.1.3 Document Scope

This document serves as a specification for interfaces/APIs between the Data lake and non-BI systems.

## 1.2 Version History


| **Version & Status** |        **Author(s)**        | **Summary of Changes** |    **Date**    |
|:----------------:|:-----------------------:|:------------------:|:----------:|
| V1.0             | Lucas Mazariegos Arraiza | Initial version    | 2021-07-01 |

# 2. Introduction

## 2.1 Overview of the System, Application or Subject Area

**prio-api** is a Python microservice that performs the calculation of price and available seats of Priority Boarding for a given flight, manages the inventory of seats according to the reservations made by customers, and exposes all the above through an API REST for use by Iberia.com.

At this stage the only consumer for this API will be Iberia.com.

## 2.2 Scope of This Document

This document describes the implementation details to develop and deploy the required API.

### 2.2.1 In Scope

Project’s scope is develop and deploy the mentioned API.

### 2.2.2 Out of Scope

Although ETLs have been developed to satisfy data for this project, they are beyond the scope of this project

# 3. Key Points

Main aspect of the project:

- The API resides in a Docker container which is deployed as a pod in EKS. Connection and authentication details are deployed as **ConfigMap** and **Secrets**, respectively.

- The Docker images reside in a **ECR** registry.

- The API was developed using **FastAPI** framework (Python). Connection to AWS DynamoDB was develop with **boto3** library.

- JSON schema for the requests and responses was provided by Iberia.com

- Authentication is managed inside the container, using an API Key.

- The deployment is exposed with a Kubernetes Service, which in turn deploys an ALB.

- The ALB is exposed to Internet for Iberia.com and (potentially) other clients.

# 4. Source Systems & API Endpoints

## 4.1 DynamoDB tables:

- SBX:
    - SBX_CURRENCY_DICT
    - SBX_HAUL_DICT
    - SBX_PRIO_AIRCRAFT_DICT
    - SBX_PRIO_INVENTORY
    - SBX_PRIO_INVENTORY_RULES
    - SBX_PRIO_PRICES_RULES
    - SBX_PRIO_RESERVATION

- PRD:
    - CURRENCY_DICT
    - HAUL_DICT
    - PRIO_AIRCRAFT_DICT
    - PRIO_INVENTORY
    - PRIO_INVENTORY_RULES
    - PRIO_PRICES_RULES
    - PRIO_RESERVATION

## 4.2 API Endpoints:

- SBX: 
    - https://prio-api-sbx.iberia.accentureanalytics.com/health
    - https://prio-api-sbx.iberia.accentureanalytics.com/_lock
    - https://prio-api-sbx.iberia.accentureanalytics.com/_unlock
    - https://prio-api-sbx.iberia.accentureanalytics.com/request_priority_confirm
    - https://prio-api-sbx.iberia.accentureanalytics.com/request_priority_boarding

- PRD: 
    - https://prio-api-prd.iberia.accentureanalytics.com/health
    - https://prio-api-prd.iberia.accentureanalytics.com/_lock
    - https://prio-api-prd.iberia.accentureanalytics.com/_unlock
    - https://prio-api-prd.iberia.accentureanalytics.com​/request_priority_confirm
    - https://prio-api-prd.iberia.accentureanalytics.com/request_priority_boarding

## 4.3 Sample Request/Response:

- _lock
    - Request:
        ```json
        {
        "locator": "KLDSD",
        "arrivalAirport": "MAD",
        "departureAirport": "GVA",
        "departureDate": "2020-08-07",
        "carrier": "IB",
        "flightNumber": "3493",
        "quantity": 2
        }
        ```
    - Response:
        ```json
        [
            "OK"
        ]
        ```
- _unlock
    - Request:
        ```json
        {
        "locator": "KLDSD",
        "arrivalAirport": "MAD",
        "departureAirport": "GVA",
        "departureDate": "2020-08-07",
        "carrier": "IB",
        "flightNumber": "3493",
        "quantity": 2
        }
        ```
    - Response:
        ```json
        [
            "OK"
        ]
        ```
- request_priority_confirm
    - Request:
        ```json
        {
        "locator": "KLDSD",
        "arrivalAirport": "MAD",
        "departureAirport": "GVA",
        "departureDate": "2020-08-07",
        "carrier": "IB",
        "flightNumber": "3493",
        "quantity": 2
        }
        ```
    - Response:
        ```json
        [
            "OK"
        ]
        ```
- request_priority_boarding
    - Request:
        ```json
        {
        "context": {
            "issueOffice": "ZRH175",
            "locator": "RHFJIT",
            "checkinFlowMode": "REGULAR",
            "slices": [
            {
                "segmentIds": [
                "IB349320200807"
                ],
                "id": "GVAMAD20200807191500"
            },
            {
                "segmentIds": [
                "IB348220200828"
                ],
                "id": "MADGVA20200828203000"
            }
            ],
            "issueCountry": "CH",
            "bookingDate": "2020-08-04 15:53",
            "segments": [
            {
                "operatingFlight": {
                "cabin": {
                    "cabinClass": {
                    "type": "ECONOMY",
                    "rbd": "O"
                    },
                    "carrier": "IB"
                },
                "flightNumber": "3493"
                },
                "arrivalDate": "2020-08-07 21:20",
                "utcArrivalDate": "2020-08-07 19:20",
                "marketingFlight": {
                "cabin": {
                    "cabinClass": {
                    "type": "ECONOMY",
                    "rbd": "O"
                    },
                    "carrier": "I2"
                },
                "flightNumber": "3493"
                },
                "flown": false,
                "arrivalAirport": "MAD",
                "departureAirport": "GVA",
                "departureDate": "2020-08-07 19:15",
                "edifact": false,
                "passengerCoupons": [
                {
                    "infantCoupon": {
                    "id": "INFANT_01",
                    "coupon": "INF",
                    "farebasis": "XDFF",
                    "numberTicket": "075000000003",
                    "ticketDesignator": null,
                    "issueDate": "2019-02-25"
                    },
                    "coupon": "1",
                    "farebasis": "ODNNANB5",
                    "franchisePieces": [
                    {
                        "subtype": "BAGGAGE_23",
                        "units": 2,
                        "description": "23Kg"
                    }
                    ],
                    "numberTicket": "0752391826332",
                    "ticketDesignator": null,
                    "seat": {
                    "row": "12",
                    "column": "A"
                    },
                    "extraPieces": [],
                    "eligible": true,
                    "issueDate": "2020-07-08T22:00:00.000Z",
                    "id": "ADULT_01",
                    "status": {
                    "message": "CHECKABLE",
                    "code": "CHECKABLE"
                    }
                },
                {
                    "infantCoupon": null,
                    "coupon": null,
                    "farebasis": "ODNNANB5",
                    "franchisePieces": [],
                    "numberTicket": null,
                    "ticketDesignator": null,
                    "seat": {
                    "row": "12",
                    "column": "A"
                    },
                    "extraPieces": [],
                    "eligible": true,
                    "issueDate": null,
                    "id": "ADULT_02",
                    "status": {
                    "message": "CHECKABLE",
                    "code": "CHECKABLE"
                    }
                }
                ],
                "pricesProvider": "TARIFICATOR",
                "utcDepartureDate": "2020-08-07 17:15",
                "time": "BKI",
                "id": "IB349320200807"
            },
            {
                "operatingFlight": {
                "cabin": {
                    "cabinClass": {
                    "type": "ECONOMY",
                    "rbd": "O"
                    },
                    "carrier": "IB"
                },
                "flightNumber": "3482"
                },
                "arrivalDate": "2020-08-28 22:25",
                "utcArrivalDate": "2020-08-28 20:25",
                "marketingFlight": null,
                "flown": false,
                "arrivalAirport": "GVA",
                "departureAirport": "MAD",
                "departureDate": "2020-08-28 20:30",
                "edifact": false,
                "passengerCoupons": [
                {
                    "infantCoupon": {
                    "id": "INFANT_01",
                    "coupon": "INF",
                    "farebasis": "XDFF",
                    "numberTicket": "075000000003",
                    "ticketDesignator": null,
                    "issueDate": "2019-02-25"
                    },
                    "coupon": null,
                    "farebasis": "ODNNANB5",
                    "franchisePieces": [],
                    "numberTicket": null,
                    "ticketDesignator": null,
                    "seat": null,
                    "extraPieces": [],
                    "eligible": true,
                    "issueDate": null,
                    "id": "ADULT_01",
                    "status": {
                    "message": "CHECKABLE",
                    "code": "CHECKABLE"
                    }
                },
                {
                    "infantCoupon": null,
                    "coupon": null,
                    "farebasis": "ODNNANB5",
                    "franchisePieces": [],
                    "numberTicket": null,
                    "ticketDesignator": null,
                    "seat": null,
                    "extraPieces": [],
                    "eligible": true,
                    "issueDate": null,
                    "id": "ADULT_02",
                    "status": {
                    "message": "CHECKABLE",
                    "code": "CHECKABLE"
                    }
                }
                ],
                "pricesProvider": "TARIFICATOR",
                "utcDepartureDate": "2020-08-28 18:30",
                "time": "BKI",
                "id": "IB348220200828"
            }
            ],
            "flownSegments": false,
            "paymentMode": "ONLINE",
            "passengers": [
            {
                "surname": "IOAS",
                "frequentFlyer": {
                "number": "72749559",
                "level": "8",
                "topTier": "CLA",
                "company": "IB"
                },
                "name": "CHARLES",
                "passengerType": "ADULT",
                "ticketPrices": [
                {
                    "currency": "CHF",
                    "number": "0752391826332",
                    "tax": 47.15,
                    "fare": 43,
                    "total": 90.15
                }
                ],
                "items": [
                "DEAF"
                ],
                "title": "MR",
                "infant": {
                "id": "INFANT_01",
                "surname": "PRUEBAS",
                "name": "BEBE",
                "ticketPrices": [
                    {
                    "currency": "EUR",
                    "number": "075000000003",
                    "tax": 32.91,
                    "fare": 25,
                    "total": 62.91
                    }
                ],
                "birthDate": "2018-12-30"
                },
                "resiberId": "2",
                "birthDate": "1980-01-02",
                "id": "ADULT_01"
            },
            {
                "surname": "GARCIAMONTOYA",
                "frequentFlyer": null,
                "name": "ERIKAPATRICIA",
                "passengerType": "ADULT",
                "ticketPrices": [
                {
                    "currency": "CHF",
                    "number": "",
                    "tax": 47.15,
                    "fare": 43,
                    "total": 90.15
                }
                ],
                "items": [],
                "title": null,
                "infant": null,
                "resiberId": "1",
                "birthDate": null,
                "id": "ADULT_02"
            }
            ],
            "issueCurrency": "CHF",
            "dynamicPricing": false
        },
        "request": {
            "currency": "EUR",
            "type": "PRIORITY_BOARDING",
            "segmentIds": [
            {
                "id": "IB349320200807",
                "passengers": [
                "ADULT_01"
                ]
            },
            {
                "id": "IB034020200808",
                "passengers": [
                "ADULT_01"
                ]
            }
            ]
        }
        }
        ```
    - Response:
        ```json
        {
            "currency": "EUR",
            "prices": [
                {
                    "segmentId": "IB000220200802",
                    "passengers": [
                        {
                            "id": "ADULT_01",
                            "amount": "12.0"
                        }
                    ],
                    "status": null
                }
            ],
            "status": {
                "reason": null,
                "code": null
            }
        }
        ```


# 5. Code Walkthrough

This chapter will do a code walkthrough over the main parts of the API.

This block performs the FastAPI initialization and activates GZip compression and Prometheus monitoring:

```python
app = FastAPI(
    title="'Orchestrator REST API",
    description="'Orchestrator REST API endpoints",
    version="0.0.1"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)
```

Authentication is performed with this code block:

```python
def get_api_key(x_api_key: str = Depends(X_API_KEY)):
    """ validates the x-api-key and raises a 401 if invalid """
    if x_api_key == os.environ['X_API_KEY']:
        return
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )
```

Health check is tested every 60 seconds with this block:

```python
@router.get("/health",
            summary='Health check.',
            tags=["HEALTH"]
            )
def health():
    return {"UP"}
```

## **There are 4 main endpoints, which we will see below**
## _lock

Main function:
```python
@router.post("/_lock/{id_session}",
             summary='Lock request for priority sitting.',
             tags=["LOCK"],
             responses={
                 400: {"model": Message, "description": "There was an error parsing the body"},
                 401: {"model": Message, "description": "Auth error"},
             }
             )
def _lock(prio_boarding_lock: PrioBoardingLock, id_session, ign=Depends(get_api_key)):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

    response = writeItemToReservationsTableDynamodb(dynamodb, id_session, prio_boarding_lock.flight_number, prio_boarding_lock.departure_date,
                                                    prio_boarding_lock.quantity)
    response_code = response.get('ResponseMetadata', '').get('HTTPStatusCode', '')
    if response_code == 200:
        return {"OK"}
    else:
        return {"LOCK FAILED WRITING RESERVATIONS TABLE: ", response}
```

# 7. Kubernetes YAMLs:

Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: prio-api-service
spec:
  selector:
    app: prio-api-service
  ports:
    - port: 80
      targetPort: 80
  selector:
    app: prio-api
---
```

Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prio-api-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: prio-api
  template:
    metadata:
      labels:
        app: prio-api
    spec:
      containers:
        - name: prio-api
          image: 077156906314.dkr.ecr.eu-west-1.amazonaws.com/prio-api:${VERSION}
          imagePullPolicy: Always
          env:
            - name: DYNAMODB_PRIO_RULES_TABLE
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_PRIO_RULES_TABLE
            - name: DYNAMODB_PRIO_INVENTORY
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_PRIO_INVENTORY
            - name: DYNAMODB_PRIO_INVENTORY_RULES
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_PRIO_INVENTORY_RULES
            - name: DYNAMODB_PRIO_RESERVATIONS
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_PRIO_RESERVATIONS
            - name: DYNAMODB_HAUL_DICT_TABLE
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_HAUL_DICT_TABLE
            - name: DYNAMODB_CURRENCY_DICT_TABLE
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_CURRENCY_DICT_TABLE
            - name: DYNAMODB_PRIO_AIRCRAFT_DICT
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: DYNAMODB_PRIO_AIRCRAFT_DICT
            - name: REQUEST_KINESIS_FIREHOSE_STREAM
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: REQUEST_KINESIS_FIREHOSE_STREAM
            - name: RESPONSE_KINESIS_FIREHOSE_STREAM
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: RESPONSE_KINESIS_FIREHOSE_STREAM
            - name: REQUEST_CONFIRM_KINESIS_FIREHOSE_STREAM
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: REQUEST_CONFIRM_KINESIS_FIREHOSE_STREAM
            - name: RESPONSE_CONFIRM_KINESIS_FIREHOSE_STREAM
              valueFrom:
                configMapKeyRef:
                  name: prio-api-configmap
                  key: RESPONSE_CONFIRM_KINESIS_FIREHOSE_STREAM
            - name: X_API_KEY
              valueFrom:
                secretKeyRef:
                  name: prio-api-secrets
                  key: X_API_KEY
          ports:
            - name: http
              containerPort: 80
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 60
            timeoutSeconds: 3
            failureThreshold: 2
            periodSeconds: 60
```

Ingress:
```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: prio-api-ingress
spec:
  rules:
  - host: prio-api-${ENV}.iberia.accentureanalytics.com
    http:
      paths:
      - path: /
        backend:
          serviceName: prio-api-service
          servicePort: 80
```
## 8. Deployment Process

A set of bash scripts where developed as part of this project to ease the deployment of this microservice.

Build and deployment process is as follows:

### 8.1 Build

The following command will build the image, tag it with :prd tag and push to ECR.
```bash
./build.sh prd
```

Note the image itself is the same for every env, only the tag changes.

Also note you'll need an AWS account to push into ECR

### 8.2 Deploy

The following force a deployment with the latest changes:

```bash
./deploy.sh prd
```

This also reapplies all the .yml files and re-creates the ConfigMaps and Secrets. You can disable the latter by commenting out the relevant lines in the script.

Note you need a **kubectl** client with a conigured Kubeconfig.

### 8.3 Test

You can test if the API is accepting requests by doing this:

```bash
./test.sh prd
```

In addition, you can export the following json **(PRIO-API.postman_collection.json)** to the Postman application to make several predefined posts and test their responses.


### 8.4 Load Testing

You can test the performance of your latest (local) changes by issuing the following:

```bash
./loadtest.sh local
```

## 9. Troubleshooting 

### 9.1 Main contacts:

- TODO

### 9.2 Error-01

 **Error:** Service Down

 **Error Description:** Service Down

 **Tools needed to solve this error:** N/A

 **How to detect the error:** There is a health check executing every 60s, so in case the service is down the deployment should be constantly stopping and starting. The **test.sh** script will be failing also. You should receive Cloudwatch alerts regarding bad requests (HTTP 500).

 **How to correct the error:** Deployment will be re-initiated until correct functionality is achieved. 
 If the error persists, check logs with ```kubectl get logs <pod-id>``` to see the specific error.

 **How to evaluate the error has been solved:** The **test.sh** script works as expected.
 

### 9.3 Error-02

 **Error:** LOCK FAILED WRITING RESERVATIONS TABLE

 **Error Description:** The endpoint _lock, could not write in the DynamoDB RESERVATIONS table.

 **Tools needed to solve this error:** AWS Credentials

 **How to detect the error:** When using the endpoint _lock, it returns the error `LOCK FAILED WRITING RESERVATIONS TABLE`

 **How to correct the error:** Check the status of the table via the Amazon Web Service client. This may be because the table has been removed.

 **How to evaluate the error has been solved:** _lock endpoint works as expected.
 

 ### 9.4 Error-03

 **Error:** UNLOCK FAILED DELETING FROM RESERVATIONS TABLE

 **Error Description:** An attempt has been made to remove an item from the RESERVATIONS table, but this item did not exist.

 **Tools needed to solve this error:** N/A

 **How to detect the error:** When using the endpoint _unlock, it returns the error `UNLOCK FAILED DELETING FROM RESERVATIONS TABLE`.

 **How to correct the error:** An attempt has been made to remove an item, which no longer exists. This is an error in data entry, when trying to delete an item that was not created previously (with _lock endpoint). Nothing needs to be done to fix it

 **How to evaluate the error has been solved:** Create an item in the table using _lock endpoint, and then delete it using _unlock endpoint making sure that it is the same item that has been created.
 


### 9.5 Error-04

 **Error:** CONFIRM FAILED UPDATING RESERVATIONS TABLE, THERE ISN'T ITEM TO UPDATE

 **Error Description:** An attempt has been made to update an item from the RESERVATIONS table, but this item did not exist.

 **Tools needed to solve this error:** N/A

 **How to detect the error:** When using the endpoint request_priority_confirm/{id_session}, it returns the error `CONFIRM FAILED UPDATING RESERVATIONS TABLE, THERE ISN'T ITEM TO UPDATE`.

 **How to correct the error:** An attempt has been made to update an item, which no longer exists. This is an error in data entry, when trying to update an item that was not created previously (with _lock endpoint). Nothing needs to be done to fix it.

 **How to evaluate the error has been solved:** Create an item in the table using _lock endpoint, and then delete it using request_priority_confirm/{id_session} endpoint making sure that it is the same item that has been created.
 

### 9.6 Error-05

 **Error:** Field Required

 **Error Description:** An attempt has been made to post to the API without a required input parameter.

 **Tools needed to solve this error:** N/A

 **How to detect the error:** An error will be returned with a list of items containing one another, the last item of which is mandatory. Example:
 ```json
    {
    "loc": [
        "body",
        "context",
        "segments",
        0,
        "departureDate"
    ],
    "msg": "field required",
    "type": "value_error.missing"
    }
 ```
 In this case, the mandatory param is departureDate.

 **How to correct the error:** By redoing the action against the API with the required fields.

 **How to evaluate the error has been solved:** The endpoint works as expected.
 


