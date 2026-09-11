import boto3
b = boto3.client("bedrock-agent", region_name="ap-southeast-1")

b.create_knowledge_base(
    name="clarvo-kb-s3v",
    roleArn="arn:aws:iam::792682046440:role/AmazonBedrockExecutionRoleForKB_lwa",
    knowledgeBaseConfiguration={
        "type": "VECTOR",
        "vectorKnowledgeBaseConfiguration": {
            "embeddingModelArn": "arn:aws:bedrock:ap-southeast-1:792682046440:inference-profile/global.cohere.embed-v4:0",
            "embeddingModelConfiguration": {
                "bedrockEmbeddingModelConfiguration": {
                    "dimensions": 1024,          # MUST equal the S3 index dimension
                    "embeddingDataType": "FLOAT32"
                }
            }
        }
    },
    storageConfiguration={
        "type": "S3_VECTORS",
        "s3VectorsConfiguration": {
            "indexArn": "arn:aws:s3vectors:ap-southeast-1:792682046440:bucket/lwa-vectors/index/lwa-kb-index"
        }
    },
)