
import kubiya

# ActionStore is a singleton that stores all the actions in the application

store = kubiya.ActionStore("aws", "0.1.0")

from .actions import ec2_actions, iam_actions, ecr_actions, ecs_actions, cloudwatch_actions, eks_actions,workspaces_actions, lambda_actions, health_check, s3_actions, rds_actions, sqs_actions