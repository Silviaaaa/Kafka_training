# Setup

1. Setup Docker and VSCode
2. Mac install environment
    - install kebernetes cmd `brew install minikube`
    - test minikube cmd `minikube`
    - see minikube nodes `kubectl get nodes`
    - install helm to deploy kubernetes services cmd `brew install helm`
    - test helm cmd `helm`
    - helm templates reference: https://github.com/bitnami/charts
        - templates set yaml
        - values.yml set pods
    - install k9s to manage kubernetes `brew install k9s`
3. build environment
    - check Docker resource cpus 4 & Memory 8G
    - download image cmd `minikube start --cpus 4 --memory 4096`
4. install Kafka
    - reference: https://github.com/bitnami/charts/tree/main/bitnami/kafka
    - check helm repo `helm repo list`
    - Add specific repo to helm `helm repo add bitnami https://charts.bitnami.com/bitnami`
    - Deploy kafka cluster
        - Deploy with default setting with one node `helm install kafka-cluster bitnami/kafka`
        - Deploy with two nodes `helm install bitnami --set replicaCount=2 bitnami/kafka`
        - check `helm list`
        - delete `helm uninstall kafka-cluster`
    - check install status `kubectl get pods`
5. uninstall kafka
    - delete `helm delete kafka-cluster`


# Create a simple Kafka service

1. Create Kafka clients

```
kubectl run bitnami-kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.4.0-debian-11-r6 --namespace default --command -- sleep infinity
```

2. cmd `helm get notes kafka-cluster`, to see the instructions of creating a pod to connect to your kafka brokers

3. Create a terminal window and execute Kafka client as producer

```
kubectl exec --tty -i bitnami-kafka-client --namespace default -- bash
kafka-console-producer.sh \
            --broker-list kafka-cluster-0.kafka-cluster-headless.default.svc.cluster.local:9092 \
            --topic iectest
```

4. Create another terminal window and execute Kafka client as consumer

```
kubectl exec --tty -i bitnami-kafka-client --namespace default -- bash
kafka-console-consumer.sh \
            --bootstrap-server kafka-cluster.default.svc.cluster.local:9092 \
            --topic iectest \
            --from-beginning
```

5. Type message and try it!
6. To stop the service, use ^C. To exit kafka client, cmd `exit`


# Create Kafka service with external code

1. uninstall above service `helm uninstall kafka-cluster`
2. install service with config

```
helm install kafka-cluster \
  --set replicaCount=1 \
  --set externalAccess.enabled=true \
  --set externalAccess.service.type=LoadBalancer \
  --set externalAccess.autoDiscovery.enabled=true \
  --set serviceAccount.create=true \
  --set rbac.create=true \
  bitnami/kafka
```

3. execute `minikube tunnel`
4. Create Producer and Consumer python file
    - (optional) open another shell and create conda environment

    ```
    conda create --name kafka-dev python=3.9
    conda activate kafka-dev
    ```

    - install kafka python package `pip install kafka-python`
    - open another shell and execute kafka_consumer.py

    ```
    conda activate kafka-dev
    python3 Kafka_training/kafka_consumer.py
    ```

    - open another shell and execute kafka_producer.py
    
    ```
    conda activate kafka-dev
    python3 Kafka_training/kafka_producer.py
    ```
