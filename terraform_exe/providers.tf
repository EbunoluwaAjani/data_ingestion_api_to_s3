terraform {
  required_version = "~>1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.0.0, <=6.0.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket = "statefilebucket-terraform-exercise"
    key    = "state.tfstate"
   
    region = "eu-central-1"
  }

}

provider "aws" {
  region = "eu-west-1"

}





