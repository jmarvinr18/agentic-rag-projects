variable "tags" {
  type = map(string)
}


variable "security_group_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
}

variable "profile" {
  type = string
  description = "local aws-cli profile name"
}

variable "region" {
  type = string
  description = "aws region"
}
