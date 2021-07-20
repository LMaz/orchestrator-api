# Note this yml is templated
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prio-api-deployment
spec:
  replicas: ${REPLICAS}
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
---
apiVersion: v1
kind: Service
metadata:
  name: prio-api-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: /metrics
    prometheus.io/port: "80"
spec:
  selector:
    app: prio-api-service
  ports:
    - port: 80
      targetPort: 80
  selector:
    app: prio-api
---
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

