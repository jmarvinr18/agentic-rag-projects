####################################################################
##                  Retrieve or Create ECR Repo                   ##
####################################################################

module "ecr" {
  source = "git::ssh://git@github.com/jmarvinr18/infra-as-code.git//terraform/provider/aws/modules/ecr"
  repos  = var.repos
}

