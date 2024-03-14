from fastapi import FastAPI, Request
import uvicorn
import httpx
import os
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.post("/v1/chat/completions")
async def ai_endpoint(request: Request):
    data = await request.body()
    return StreamingResponse(stream_data(data))


async def stream_data(data):
    azure_resource_name = os.environ['AZURE_RESOURCE_NAME']
    azure_api_version = os.environ['AZURE_API_VERSION']
    azure_api_key = os.environ['AZURE_API_KEY']
    azure_deployment_name = os.environ['AZURE_DEPLOYMENT_NAME']

    url = f'https://{azure_resource_name}.openai.azure.com/openai/deployments/{azure_deployment_name}/chat/completions?api-version={azure_api_version}'
    headers = {
        'Content-Type': 'application/json',
        'api-key': azure_api_key
    }
    async with httpx.AsyncClient(timeout=20000) as client:
        async with client.stream("POST", url, headers=headers, data=data) as r:
            async for chunk in r.aiter_bytes():
                yield chunk


if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, host="0.0.0.0", workers=4)

