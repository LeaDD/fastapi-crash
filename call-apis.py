"""Test routes locally"""

import requests

inspect_url = "http://localhost:8000/inspect"
transform_url = "http://localhost:8000/transform"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "secret-key-123",  # replace if your key is different
}

payload = {
    "name": "David",
    "age": 56,
    "skills": ["python", "fastapi", "bash"],
    "metadata": None,
    "profile": {"bio": "Tech lead", "active": True},
    "projects": [
        {"name": "Recommendations Engine", "status": "live"},
        {"name": "Data Pipeline", "status": None},
    ],
}


if __name__ == "__main__":
    response = requests.post(inspect_url, json=payload, headers=headers, timeout=300)
    print(response.status_code)
    print(response.json())

    response = requests.post(transform_url, json=payload, headers=headers, timeout=300)
    print(response.status_code)
    print(response.json())
