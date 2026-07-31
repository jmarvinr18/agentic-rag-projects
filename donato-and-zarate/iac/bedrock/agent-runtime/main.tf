data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["bedrock-agentcore.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ecr_permissions" {
  statement {
    actions   = ["ecr:GetAuthorizationToken"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer"
    ]
    effect    = "Allow"
    resources = ["arn:aws:ecr:ap-southeast-1:624504148254:repository/deszr-agent-api-stg"]
  }
}

resource "aws_iam_role" "example" {
  name               = "bedrock-agentcore-runtime-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "example" {
  role   = aws_iam_role.example.id
  policy = data.aws_iam_policy_document.ecr_permissions.json
}


####################################################################
##                  Retrieve or Create ECR Repo                   ##
####################################################################

module "bedrock-agent-runtime" {
  source = "git::ssh://git@github.com/jmarvinr18/infra-as-code.git//terraform/provider/aws/modules/bedrock/agent-runtime"

  agent_runtime_name = var.agent_runtime_name
  
  role_arn =  aws_iam_role.example.arn

  artifact_container_uri = var.artifact_container_uri
  
  network_mode = var.network_mode
  endpoint_name = var.endpoint_name
  endpoint_description = var.endpoint_description
}

