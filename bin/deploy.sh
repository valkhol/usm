
docker build -t kolesnik705/usm-api:latest -t kolesnik705/usm-api:"${GIT_SHA}" -f Dockerfile .
docker build -t kolesnik705/usm-worker:latest -t kolesnik705/usm-worker:"${GIT_SHA}" -f Dockerfile-worker .

docker push kolesnik705/usm-api:latest
docker push kolesnik705/usm-api:"${GIT_SHA}"

docker push kolesnik705/usm-worker:latest
docker push kolesnik705/usm-worker:"${GIT_SHA}"

kubectl apply -f k8s

kubectl set image deployments/api-deployment api=kolesnik705/usm-api:"${GIT_SHA}"
kubectl set image deployments/worker-deployment worker=kolesnik705/usm-worker:"${GIT_SHA}"

