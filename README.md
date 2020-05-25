# AWS-SageMaker-Docker-for-Custom-ML-Model
Now you can train and build custom ML models on AWS Sagemaker using Docker

In the container directory are all the components you need to package the sample algorithm for Amazon SageMager:

.
|-- Dockerfile
|-- build_and_push.sh
`-- linear_svm
    |-- nginx.conf
    |-- predictor.py
    |-- serve
    |-- train
    `-- wsgi.py

# Building and registering the container
The following shell code shows how to build the container image using docker build and push the container image to ECR using docker push. This code is also available as the shell script container/build-and-push.sh, which you can run as build-and-push.sh keyword-intent to build the image keyword-intent

This code looks for an ECR repository in the account you're using and the current default region (if you're using a SageMaker notebook instance, this will be the region where the notebook instance was created). If the repository doesn't exist, the script will create it.

%%sh
Steps :-
#The name of our algorithm
algorithm_name=keyword-model #you can choose any name

#your current dir should be the container folder

chmod +x linear_svm/train
chmod +x linear_svm/serve

# Get the Acc No. defined in the current configuration
account=$(aws sts get-caller-identity --query Account --output text)
# Get the region defined in the current configuration
region=$(aws configure get region)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"


# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${algorithm_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
$(aws ecr get-login --region ${region} --no-include-email)
OR
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

# Build the docker image locally with the image name and then push it to ECR with the full name.

docker build  -t ${algorithm_name} .

Run "docker run --rm -v $(pwd)/local_test/test_dir:/opt/ml algorithm_name train" --> To train your model and save weights in required folder in pickle format

docker tag ${algorithm_name} ${fullname}

# Pushing Docker image to ECR
docker push ${fullname}

