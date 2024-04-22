# Backup Cronjob Setup Guide

This guide outlines the steps to set up a backup cronjob using Minikube and Docker containers. 

## Prerequisites

- Minikube installed and running.
- Docker installed.
- `kubectl` command-line tool installed.
- Access to the Kubernetes cluster managed by Minikube.

## Step 1: Start Minikube

Start Minikube using the following command:

```bash
minikube start
```

## Step 2: Build Docker Image

Build the Docker image for the backup container. Navigate to the container directory and execute:

```bash
cd container/
docker build -t backup .
cd ..
```

## Step 3: Save Docker Image

Save the Docker image to a TAR file:

```bash
docker image save -o backup.tar backup:latest
```

## Step 4: Load Docker Image into Minikube

Load the Docker image into Minikube:

```bash
minikube image load backup.tar
```

If it's your first time, you need to create a secret and apply PersistentVolumeClaims (PVC).

### Create Secret

Create a generic secret named `google-token` from a file:

```bash
kubectl create secret generic google-token --from-file=credentials/
```

### Apply PersistentVolumeClaims

Apply the PersistentVolumeClaims (PVC) configuration:

```bash
kubectl apply -f pvc.yaml
```

## Step 5: Apply CronJob Configuration

Apply the cronjob configuration:

```bash
kubectl apply -f cronjob.yaml
```

## Step 6: Monitor CronJob Execution

Watch the execution of the cronjob:

```bash
kubectl get pods --watch
```

## Step 7: Cleanup

After the cronjob execution is complete, clean up the resources.

### Delete CronJob

Delete the cronjob:

```bash
kubectl delete cronjob backup-cronjob
```

### Remove Docker Image

SSH into Minikube and remove the Docker image:

```bash
minikube ssh
# Inside the Minikube shell
docker rmi backup
exit
```

### Stop Minikube

Stop Minikube:

```bash
minikube stop
```

## Viewing Logs and Files

### View Logs

To view logs of a specific pod:

```bash
kubectl logs <pod_name>
```

### Access File Structure

To access the file structure of a pod while it's running:

```bash
kubectl exec -it <pod_name> -- /bin/sh
```

Within the pod, you can navigate and view files. For example, to view the log file:

```bash
cat back.log
```

## Additional Notes

- Make sure to replace `<pod_name>` with the actual name of the pod.
- Ensure paths and filenames are correctly specified according to your setup.